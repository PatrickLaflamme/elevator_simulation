from typing import Protocol, List

from elevator_controller.model.elevator import Elevator


class ElevatorSystemPersistenceStrategy(Protocol):
    def persist(self, elevators: List[Elevator]):
        ...