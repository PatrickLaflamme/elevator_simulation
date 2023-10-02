import math
import sys
from typing import Protocol, List, Optional

from elevator_controller.model.elevator import Elevator
from elevator_controller.model.passenger import Passenger


class ElevatorAssignmentStrategy(Protocol):
    def assign_elevator(self, passenger: Passenger, elevators: List[Elevator]) -> Optional[Elevator]:
        ...


class ClosestEmptyStrategy:
    def assign_elevator(self, passenger: Passenger, elevators: List[Elevator]) -> Optional[Elevator]:
        closest_elevator = None
        closest_distance = float('inf')
        for elevator in elevators:
            if elevator.is_empty() and elevator.can_accommodate():
                distance = abs(elevator.current_floor - passenger.source_floor)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_elevator = elevator
        return closest_elevator


class DirectionalStrategy:
    def assign_elevator(self, passenger: Passenger, elevators: List[Elevator]) -> Optional[Elevator]:
        min_distance = sys.maxsize
        assigned_elevator = None
        for elevator in elevators:
            passenger_dir = round(math.copysign(1, passenger.source_floor - elevator.current_floor))
            passenger_in_same_dir_as_elevator_dir = elevator.direction.value == passenger_dir
            if not passenger_in_same_dir_as_elevator_dir and not elevator.is_idle():
                continue
            elevator_distance = passenger.source_floor - elevator.current_floor
            if elevator.can_accommodate() and elevator_distance < min_distance:
                min_distance = elevator_distance
                assigned_elevator = elevator
        return assigned_elevator
