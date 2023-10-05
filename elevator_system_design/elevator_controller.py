from typing import List, Set, Iterator

from elevator_system_design.log import logger
from elevator_system_design.model.elevator import Elevator
from elevator_system_design.model.passenger import Passenger
from elevator_system_design.model.system_summary import SystemSummary
from elevator_system_design.strategies.assignment import ElevatorAssignmentStrategy
from elevator_system_design.strategies.elevator_controller_persistence import ElevatorControllerPersistenceStrategy, \
    NoopPersistenceStrategy
from elevator_system_design.strategies.idle import ElevatorIdleStrategy


class ElevatorController:
    elevators: List[Elevator]
    assignment_strategy: ElevatorAssignmentStrategy
    idle_strategy: ElevatorIdleStrategy
    state_persistence_strategy: ElevatorControllerPersistenceStrategy
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
                 assignment_strategy: ElevatorAssignmentStrategy,
                 idle_strategy: ElevatorIdleStrategy,
                 stop_time: int = 0,
                 persistence_strategy: ElevatorControllerPersistenceStrategy = NoopPersistenceStrategy()):
        """
        The function initializes an elevator controller with a specified number of elevators, floors, maximum elevator
        capacity, assignment strategy, idle strategy, stop time, and persistence strategy.

        :param n_elevators: The number of elevators in the system
        :type n_elevators: int
        :param n_floors: The number of floors in the building
        :type n_floors: int
        :param max_elevator_capacity: The `max_elevator_capacity` parameter represents the maximum number of passengers that
        can be accommodated in each elevator
        :type max_elevator_capacity: int
        :param assignment_strategy: The `assignment_strategy` parameter is an instance of the `ElevatorAssignmentStrategy`
        class. It determines how the elevators are assigned to handle passenger requests. This strategy can vary depending
        on factors such as the current state of the elevators, the location of the passengers, and the desired destination
        floors
        :type assignment_strategy: ElevatorAssignmentStrategy
        :param idle_strategy: The `idle_strategy` parameter is an instance of the `ElevatorIdleStrategy` class. It
        determines how idle elevators are positioned within the building. The `position_idle_elevators` method of the
        `idle_strategy` is called to set up the initial distribution of elevators across the floors
        :type idle_strategy: ElevatorIdleStrategy
        :param stop_time: The `stop_time` parameter is an optional parameter that specifies the time (in seconds) that an
        elevator should wait at each floor before closing its doors and moving to the next floor. If no value is provided,
        the default value is 0, indicating that the elevator should not wait at each floor, defaults to 0
        :type stop_time: int (optional)
        :param persistence_strategy: The `persistence_strategy` parameter is an instance of the
        `ElevatorControllerPersistenceStrategy` class. It is used to define the strategy for persisting the state of the
        elevator controller. The `ElevatorControllerPersistenceStrategy` class is an abstract base class that provides
        methods for saving and loading the
        :type persistence_strategy: ElevatorControllerPersistenceStrategy
        """
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
        """
        The function requests an elevator for a passenger and assigns the passenger to the elevator if available, otherwise
        adds the passenger to the pending list.

        :param passenger: The `passenger` parameter represents an instance of the `Passenger` class. It is an object that
        contains information about the passenger, such as their source floor and destination floor
        :type passenger: Passenger
        :return: nothing (None).
        """
        elevator_index = self.assignment_strategy.assign_elevator(passenger, elevators=self.elevators)
        if elevator_index is None:
            self.pending_passengers.add(passenger)
            return
        if passenger in self.pending_passengers:
            self.pending_passengers.remove(passenger)
        assert self.elevators[elevator_index].assign(passenger)
        self.waiting_passengers[elevator_index][passenger.source_floor - 1].append(passenger)

    def step(self):
        """
        The function iterates through each elevator, disembarks passengers on the current floor, embarks waiting passengers,
        moves the elevator, and updates the time.
        """
        self.idle_strategy.position_idle_elevators(self.elevators)
        for i in range(len(self.elevators)):
            elevator = self.elevators[i]
            while len(self.embarked_passengers[i][elevator.current_floor - 1]):
                p = self.embarked_passengers[i][elevator.current_floor - 1].pop()
                elevator.disembark(p)
                logger.debug(f"elevator {i} dropped off {p.id} on floor {elevator.current_floor} after {self.time - p.request_time} steps. direction: {elevator.direction} remaining targets: {elevator.targets}")
                self.total_time_summary.include(self.time - p.request_time)
            while len(self.waiting_passengers[i][elevator.current_floor - 1]):
                p = self.waiting_passengers[i][elevator.current_floor - 1].pop()
                if elevator.embark(p):
                    logger.debug(f"elevator {i} picked up {p.id} on floor {elevator.current_floor} after {self.time - p.request_time} steps heading {elevator.direction} to {p.destination_floor}")
                    self.embarked_passengers[i][p.destination_floor - 1].append(p)
                    self.wait_time_summary.include(self.time - p.request_time)
                else:
                    self.pending_passengers.add(p)
            elevator.move()
        for pending_passenger in sorted(self.pending_passengers, key=lambda p: p.request_time):
            self.request_elevator(pending_passenger)
        self.time += 1
        self.state_persistence_strategy.persist(self.time, self.elevators)

    def handle_passenger_requests(self, passenger_request_source: Iterator[List[Passenger]]):
        """
        The function handles passenger requests by processing each batch of requests, assigning elevators to passengers, and
        delivering passengers to their destinations.

        :param passenger_request_source: The `passenger_request_source` parameter is an iterator that yields batches of
        passenger requests. Each batch is a list of `Passenger` objects
        :type passenger_request_source: Iterator[List[Passenger]]
        """
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
        logger.info(f"all {total_passengers} passengers acknowledged at step {self.time}")
        while len(self.pending_passengers):
            self.step()
        logger.info(f"all {total_passengers} passengers assigned to an elevator at step {self.time}")
        while self.total_time_summary.n < total_passengers:
            self.step()
        logger.info(f"all {total_passengers} passengers delivered to their destinations at step {self.time}")

    def get_stats(self):
        """
        The function `get_stats` returns a dictionary containing the wait time and total time summaries.
        :return: a dictionary with two keys: 'wait_time' and 'total_time'. The values associated with these keys are the
        dictionaries returned by the `__dict__()` method called on the `wait_time_summary` and `total_time_summary` objects.
        """
        return {
            'wait_time': self.wait_time_summary.__dict__(),
            'total_time': self.total_time_summary.__dict__()
        }

    def print_stats(self):
        """
        The `print_stats` function prints a summary of wait time and total time using the tabulate library.
        :return: the tabulated statistics for wait time and total time.
        """
        try:
            # This try-catch exists to avoid making tabulate a hard dependency of this tool.
            from tabulate import tabulate
        except ImportError:
            print("The tabulate library is required to run this function. run `pip install tabulate` to install it.")
            return
        print(tabulate([
            {"time_period": "wait time", **self.wait_time_summary.__dict__()},
            {"time_period": "total time", **self.total_time_summary.__dict__()},
        ], headers='keys'))
