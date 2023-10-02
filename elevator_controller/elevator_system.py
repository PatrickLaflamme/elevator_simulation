from typing import List, Set, Iterator

from elevator_controller.log import logger
from elevator_controller.model.elevator import Elevator
from elevator_controller.model.passenger import Passenger
from elevator_controller.model.system_summary import SystemSummary
from elevator_controller.strategies.assignment import ElevatorAssignmentStrategy, DirectionalStrategy
from elevator_controller.strategies.elevator_system_persistence import ElevatorSystemPersistenceStrategy
from elevator_controller.strategies.idle import ElevatorIdleStrategy, EqualSpreadIdleStrategy


class ElevatorSystem:
    elevators: List[Elevator]
    assignment_strategy: ElevatorAssignmentStrategy
    idle_strategy: ElevatorIdleStrategy
    state_persistence_strategy: ElevatorSystemPersistenceStrategy
    num_floors: int
    pending_passengers: Set[Passenger] = set()
    time: int = 0

    def __init__(self,
                 n_elevators: int,
                 n_floors: int,
                 max_elevator_capacity: int,
                 persistence_strategy: ElevatorSystemPersistenceStrategy,
                 assignment_strategy: ElevatorAssignmentStrategy = DirectionalStrategy(),
                 idle_strategy: ElevatorIdleStrategy = EqualSpreadIdleStrategy()):
        self.elevators = [Elevator(top_floor=n_floors, max_passengers=max_elevator_capacity) for _ in range(n_elevators)]
        self.state_persistence_strategy = persistence_strategy
        self.assignment_strategy = assignment_strategy
        self.idle_strategy = idle_strategy

    def request_elevator(self, passenger: Passenger):
        elevator = self.assignment_strategy.assign_elevator(passenger, elevators=self.elevators)
        if not elevator:
            self.pending_passengers.add(passenger)
            return
        if passenger in self.pending_passengers:
            self.pending_passengers.remove(passenger)
        elevator.request_pickup(passenger)

    def step(self):
        self.idle_strategy.position_idle_elevators(self.elevators)
        for elevator in self.elevators:
            elevator.move(self.time)
        for pending_passenger in list(self.pending_passengers):
            self.request_elevator(pending_passenger)
        self.time += 1

    def handle_passenger_requests(self, passenger_request_source: Iterator[List[Passenger]]):
        self.state_persistence_strategy.persist(self.time, self.elevators)
        for passenger_batch in passenger_request_source:
            for passenger in passenger_batch:
                self.request_elevator(passenger)
            self.step()
            self.state_persistence_strategy.persist(self.time, self.elevators)
        print(f"all passengers onboarded at step {self.time}")
        while any([not e.is_empty() for e in self.elevators]):
            print([len(e.pending_passengers) for e in self.elevators])
            self.step()
            self.state_persistence_strategy.persist(self.time, self.elevators)
        print(f"all passengers delivered to their destinations at step {self.time}")

    def get_stats(self):
        aggregate_wait_time_summary = sum([e.wait_time_summary for e in self.elevators], SystemSummary())
        aggregate_total_time_summary = sum([e.total_time_summary for e in self.elevators], SystemSummary())
        return {
            'wait_time': aggregate_wait_time_summary.__dict__(),
            'total_time': aggregate_total_time_summary.__dict__()
        }
