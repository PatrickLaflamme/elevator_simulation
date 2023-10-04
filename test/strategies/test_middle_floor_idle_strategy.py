from elevator_system_design.model.elevator import Elevator
from elevator_system_design.strategies.idle import MiddleFloorIdleStrategy


def test_middle_floor_idle_strategy():
    elevators = [Elevator(num_floors=10, max_capacity=10) for i in range(5)]
    strategy = MiddleFloorIdleStrategy()
    strategy.position_idle_elevators(elevators)

    for elevator in elevators:
        assert elevator.idle_target == 5


def test_middle_floor_idle_strategy_uneven_floors():
    elevators = [Elevator(num_floors=11, max_capacity=10) for i in range(5)]
    strategy = MiddleFloorIdleStrategy()
    strategy.position_idle_elevators(elevators)

    for elevator in elevators:
        assert elevator.idle_target == 5
