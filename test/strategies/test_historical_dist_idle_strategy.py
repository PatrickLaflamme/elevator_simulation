from elevator_system_design.model.elevator import Elevator
from elevator_system_design.strategies.idle import EqualSpreadIdleStrategy, HistoricalDistributionIdleStrategy


def test_historical_dist_idle_strategy_is_same_as_equal_dist_if_dist_is_uniform():
    equal_spread_elevators = [Elevator(num_floors=10, max_capacity=10) for _ in range(5)]
    strategy = EqualSpreadIdleStrategy()
    strategy.position_idle_elevators(equal_spread_elevators)


    hist_dist_elevators = [Elevator(num_floors=10, max_capacity=10) for _ in range(5)]
    strategy = HistoricalDistributionIdleStrategy(historical_counts=[100 for _ in range(hist_dist_elevators[-1].num_floors)])
    strategy.position_idle_elevators(hist_dist_elevators)

    assert [e.idle_target for e in equal_spread_elevators] == [e.idle_target for e in hist_dist_elevators]


def test_historical_dist_idle_strategy_assign_all_to_same_floor_if_only_one_floor_nonzero():
    hist_dist_elevators = [Elevator(num_floors=10, max_capacity=10) for _ in range(5)]
    strategy = HistoricalDistributionIdleStrategy(historical_counts=[100 if i == 4 else 0 for i in range(hist_dist_elevators[-1].num_floors)])
    strategy.position_idle_elevators(hist_dist_elevators)

    assert [5 for _ in hist_dist_elevators] == [e.idle_target for e in hist_dist_elevators]


def test_historical_dist_idle_strategy_arbitrary_historical_dist():
    historical = [2, 5, 3, 5, 7, 8, 20, 12, 4, 5, 7, 3, 12]
    hist_dist_elevators = [Elevator(num_floors=len(historical), max_capacity=10) for _ in range(5)]
    strategy = HistoricalDistributionIdleStrategy(historical_counts=historical)
    strategy.position_idle_elevators(hist_dist_elevators)

    assert [3, 6, 7, 9, 13] == [e.idle_target for e in hist_dist_elevators]

