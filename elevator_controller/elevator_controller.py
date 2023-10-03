from typing import List, Set, Iterator

from elevator_controller.log import logger
from elevator_controller.model.elevator import Elevator
from elevator_controller.model.passenger import Passenger
from elevator_controller.model.system_summary import SystemSummary
from elevator_controller.strategies.assignment import ElevatorAssignmentStrategy
from elevator_controller.strategies.elevator_system_persistence import ElevatorSystemPersistenceStrategy
from elevator_controller.strategies.idle import ElevatorIdleStrategy


class ElevatorController:
    elevators: List[Elevator]
    assignment_strategy: ElevatorAssignmentStrategy
    idle_strategy: ElevatorIdleStrategy
    state_persistence_strategy: ElevatorSystemPersistenceStrategy
    waiting_passengers: List[List[List[Passenger]]]
    embarked_passengers: List[List[List[Passenger]]]
    num_floors: int
    pending_passengers: Set[Passenger] = set()
    time: int = 0
    wait_time_summary: SystemSummary
    total_time_summary: SystemSummary

    def __init__(self,
                 n_elevators: int,
                 n_floors: int,
                 max_elevator_capacity: int,
                 persistence_strategy: ElevatorSystemPersistenceStrategy,
                 assignment_strategy: ElevatorAssignmentStrategy,
                 idle_strategy: ElevatorIdleStrategy,
                 stop_time: int = 0,):
        self.elevators = [Elevator(num_floors=n_floors, max_capacity=max_elevator_capacity, stop_time=stop_time) for _ in range(n_elevators)]
        self.state_persistence_strategy = persistence_strategy
        self.assignment_strategy = assignment_strategy
        self.idle_strategy = idle_strategy
        self.waiting_passengers = [[[] for _ in range(n_floors)] for _ in range(n_elevators)]
        self.embarked_passengers = [[[] for _ in range(n_floors)] for _ in range(n_elevators)]
        self.wait_time_summary = SystemSummary()
        self.total_time_summary = SystemSummary()

        # set up the initial elevator distribution across the floors.
        self.idle_strategy.position_idle_elevators(self.elevators)
        for e in self.elevators:
            e.current_floor = e.idle_target

    def request_elevator(self, passenger: Passenger):
        elevator_index = self.assignment_strategy.assign_elevator(passenger, elevators=self.elevators)
        if elevator_index is None:
            self.pending_passengers.add(passenger)
            return
        if passenger in self.pending_passengers:
            self.pending_passengers.remove(passenger)
        assert self.elevators[elevator_index].assign(passenger)
        self.waiting_passengers[elevator_index][passenger.source_floor - 1].append(passenger)

    def step(self):
        self.idle_strategy.position_idle_elevators(self.elevators)
        for i in range(len(self.elevators)):
            elevator = self.elevators[i]
            while len(self.embarked_passengers[i][elevator.current_floor - 1]):
                p = self.embarked_passengers[i][elevator.current_floor - 1].pop()
                assert elevator.disembark(p)
                logger.debug(f"elevator {i} dropped off {p.id} on floor {elevator.current_floor} after {self.time - p.request_time} steps. direction: {elevator.direction} remaining targets: {elevator.targets}")
                self.total_time_summary.include(self.time - p.request_time)
            while len(self.waiting_passengers[i][elevator.current_floor - 1]) and elevator.passenger_count < elevator.max_capacity:
                p = self.waiting_passengers[i][elevator.current_floor - 1].pop()
                if elevator.embark(p):
                    logger.debug(f"elevator {i} picked up {p.id} on floor {elevator.current_floor} after {self.time - p.request_time} steps heading {elevator.direction} to {p.destination_floor}")
                    self.embarked_passengers[i][p.destination_floor - 1].append(p)
                    self.wait_time_summary.include(self.time - p.request_time)
                else:
                    self.request_elevator(p)
            elevator.move()
        for pending_passenger in list(self.pending_passengers):
            self.request_elevator(pending_passenger)
        self.time += 1

    def handle_passenger_requests(self, passenger_request_source: Iterator[List[Passenger]]):
        self.state_persistence_strategy.persist(self.time, self.elevators)
        total_passengers = 0
        for passenger_batch in passenger_request_source:
            total_passengers += len(passenger_batch)
            for passenger in passenger_batch:
                if passenger.source_floor == passenger.destination_floor:
                    logger.warn(f"Passenger with id {passenger.id} has the same source and destination floors! "
                                f"Nothing to do.")
                    self.wait_time_summary.no_action()
                    self.total_time_summary.no_action()
                    continue
                self.request_elevator(passenger)
            self.step()
            self.state_persistence_strategy.persist(self.time, self.elevators)
        logger.info(f"all {total_passengers} passengers acknowledged at step {self.time}")
        while len(self.pending_passengers):
            self.step()
        logger.info(f"all {total_passengers} passengers assigned to an elevator at step {self.time}")
        while any([not e.is_empty() for e in self.elevators]):
            self.step()
            self.state_persistence_strategy.persist(self.time, self.elevators)
        logger.info(f"all {total_passengers} passengers delivered to their destinations at step {self.time}")

    def get_stats(self):
        return {
            'wait_time': self.wait_time_summary.__dict__(),
            'total_time': self.total_time_summary.__dict__()
        }

    def print_stats(self):
        from tabulate import tabulate
        print(tabulate([
            {"time_period": "wait time", **self.wait_time_summary.__dict__()},
            {"time_period": "total time", **self.total_time_summary.__dict__()},
        ], headers='keys'))
