from elevator_system_design.model.elevator import Elevator
from elevator_system_design.model.passenger import Passenger
from elevator_system_design.strategies.assignment import ClosestEmptyStrategy


def test_closest_empty_strategy_assigns_empty_elevator_thats_closest():
    passenger = Passenger(id="", source_floor=1, destination_floor=10, request_time=0)
    elevators = [Elevator(num_floors=10, max_capacity=1) for _ in range(10)]
    for i, e in enumerate(elevators):
        e.current_floor = 10 - i
    strategy = ClosestEmptyStrategy()

    result = strategy.assign_elevator(passenger, elevators)

    assert result == 9


def test_closest_empty_strategy_assigns_only_empty_elevators():
    passenger = Passenger(id="", source_floor=1, destination_floor=10, request_time=0)
    existing_passenger = Passenger(id="", source_floor=10, destination_floor=1, request_time=0)
    elevators = [Elevator(num_floors=10, max_capacity=1) for _ in range(10)]
    for i, e in enumerate(elevators):
        if i != 0:
            # Only the 0th elevator will be empty.
            e.assign(existing_passenger)
        e.current_floor = 10 - i
    strategy = ClosestEmptyStrategy()

    result = strategy.assign_elevator(passenger, elevators)

    assert result == 0


def test_closest_empty_strategy_returns_none_if_no_elevators_are_empty():
    passenger = Passenger(id="", source_floor=1, destination_floor=10, request_time=0)
    existing_passenger = Passenger(id="", source_floor=10, destination_floor=1, request_time=0)
    elevators = [Elevator(num_floors=10, max_capacity=1) for _ in range(10)]
    for i, e in enumerate(elevators):
        # No elevators will be empty.
        e.assign(existing_passenger)
        e.current_floor = 10 - i
    strategy = ClosestEmptyStrategy()

    result = strategy.assign_elevator(passenger, elevators)

    assert result is None
