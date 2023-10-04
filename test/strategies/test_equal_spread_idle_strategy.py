from elevator_system_design.model.elevator import Elevator
from elevator_system_design.strategies.idle import EqualSpreadIdleStrategy


def test_equal_spread_idle_strategy():
    elevators = [Elevator(num_floors=10, max_capacity=10) for _ in range(5)]
    strategy = EqualSpreadIdleStrategy()
    strategy.position_idle_elevators(elevators)

    assert [e.idle_target for e in elevators] == [1, 3, 5, 7, 9]


def test_equal_spread_idle_strategy_uneven():
    elevators = [Elevator(num_floors=23, max_capacity=10) for _ in range(5)]
    strategy = EqualSpreadIdleStrategy()
    strategy.position_idle_elevators(elevators)

    assert [e.idle_target for e in elevators] == [2, 7, 12, 16, 21]
