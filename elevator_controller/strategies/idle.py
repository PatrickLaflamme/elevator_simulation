from typing import Protocol, List

from elevator_controller.model.elevator import Elevator


class ElevatorIdleStrategy(Protocol):
    def position_idle_elevators(self, elevators: List[Elevator]):
        ...


class MiddleFloorIdleStrategy:
    def position_idle_elevators(self, elevators: List[Elevator]):
        for elevator in elevators:
            middle_floor = elevator.top_floor // 2
            elevator.idle_target = middle_floor


class EqualSpreadIdleStrategy:
    def position_idle_elevators(self, elevators: List[Elevator]):
        assert len(elevators) > 0
        assert len(set([e.top_floor for e in elevators])) == 1
        top_floor = elevators[0].top_floor
        idle_elevators = [e for e in elevators if e.is_empty()]
        for i in range(len(idle_elevators)):
            elevator = idle_elevators[i]
            target_floor = (i + 1) * top_floor // (len(idle_elevators) + 1)
            elevator.idle_target = target_floor
