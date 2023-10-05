import math
import sys
from typing import Protocol, List, Optional

from elevator_system_design.model.elevator import Elevator
from elevator_system_design.model.passenger import Passenger


class ElevatorAssignmentStrategy(Protocol):
    def assign_elevator(self, passenger: Passenger, elevators: List[Elevator]) -> Optional[int]:
        """
        The function assigns a passenger to an elevator from a list of available elevators.

        :param passenger: The passenger parameter is an instance of the Passenger class. It represents the passenger who
        needs to be assigned to an elevator
        :type passenger: Passenger
        :param elevators: The `elevators` parameter is a list of `Elevator` objects
        :type elevators: List[Elevator]
        """
        ...


class ClosestEmptyStrategy:
    def assign_elevator(self, passenger: Passenger, elevators: List[Elevator]) -> Optional[int]:
        """
        The function assigns a passenger to the closest available elevator based on the distance between the elevator's
        current floor and the passenger's source floor. Only empty elevators are considered.

        :param passenger: The `passenger` parameter represents the passenger who needs to be assigned an elevator. It is of
        type `Passenger`
        :type passenger: Passenger
        :param elevators: The `elevators` parameter is a list of `Elevator` objects
        :type elevators: List[Elevator]
        :return: the index of the closest elevator that is currently empty.
        """
        closest_elevator = None
        closest_distance = float('inf')
        for i in range(len(elevators)):
            elevator = elevators[i]
            if elevator.is_empty():
                distance = abs(elevator.current_floor - passenger.source_floor)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_elevator = i
        return closest_elevator


class DirectionalStrategy:
    def assign_elevator(self, passenger: Passenger, elevators: List[Elevator]) -> Optional[int]:
        """
        The function assigns a passenger to an elevator based on their source floor and the current state of the elevators.

        :param passenger: The `passenger` parameter represents the passenger who needs to be assigned to an elevator. It is
        of type `Passenger`
        :type passenger: Passenger
        :param elevators: The `elevators` parameter is a list of `Elevator` objects. Each `Elevator` object represents an
        elevator in a building
        :type elevators: List[Elevator]
        :return: the index of the assigned elevator as an integer, or None if no elevator is assigned.
        """
        min_distance = sys.maxsize
        assigned_elevator: Optional[int] = None
        for elevator_idx in range(len(elevators)):
            elevator = elevators[elevator_idx]
            passenger_dir = round(math.copysign(1, passenger.source_floor - elevator.current_floor))
            if passenger.source_floor == elevator.current_floor:
                passenger_dir = passenger.direction.value
            passenger_in_same_dir_as_elevator_dir = elevator.direction.value == passenger_dir
            if not passenger_in_same_dir_as_elevator_dir and not elevator.is_idle():
                continue
            elevator_distance = abs(passenger.source_floor - elevator.current_floor)
            if elevator.can_accommodate() and elevator_distance < min_distance:
                min_distance = elevator_distance
                assigned_elevator = elevator_idx
        return assigned_elevator
