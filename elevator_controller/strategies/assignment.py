from typing import Protocol, List, Optional

from elevator_controller.model.elevator import Elevator
from elevator_controller.model.passenger import Passenger


class ElevatorAssignmentStrategy(Protocol):
    def assign_elevator(self, passenger: Passenger, elevators: List[Elevator]) -> Optional[Elevator]:
        ...
