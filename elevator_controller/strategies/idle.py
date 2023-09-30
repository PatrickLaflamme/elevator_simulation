from typing import Protocol

from elevator_controller.model.elevator import Elevator


class ElevatorIdleStrategy(Protocol):
    def position_idle_elevator(self, elevator: Elevator):
        ...
