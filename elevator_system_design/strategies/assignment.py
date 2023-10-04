import math
import sys
from typing import Protocol, List, Optional

from elevator_system_design.model.elevator import Elevator
from elevator_system_design.model.passenger import Passenger


class ElevatorAssignmentStrategy(Protocol):
    def assign_elevator(self, passenger: Passenger, elevators: List[Elevator]) -> Optional[int]:
        ...


class ClosestEmptyStrategy:
    def assign_elevator(self, passenger: Passenger, elevators: List[Elevator]) -> Optional[int]:
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
