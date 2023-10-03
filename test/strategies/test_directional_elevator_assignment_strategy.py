from elevator_controller.model.direction import Direction
from elevator_controller.model.elevator import Elevator
from elevator_controller.model.passenger import Passenger
from elevator_controller.strategies.assignment import DirectionalStrategy


def test_directional_strategy_assigns_elevator_on_same_floor_moving_in_passenger_dir():
    passenger = Passenger(id="", source_floor=2, destination_floor=10, request_time=0)
    elevators = [Elevator(num_floors=10, max_capacity=1) for _ in range(10)]
    for i, e in enumerate(elevators):
        e.direction = Direction.UP
        e.current_floor = i + 1
    strategy = DirectionalStrategy()

    result = strategy.assign_elevator(passenger, elevators)

    assert result == 1


def test_directional_strategy_assigns_elevator_moving_toward_passenger():
    passenger = Passenger(id="", source_floor=2, destination_floor=10, request_time=0)
    elevators = [Elevator(num_floors=10, max_capacity=1) for _ in range(10)]
    for i, e in enumerate(elevators):
        e.direction = Direction.DOWN
        e.current_floor = i + 1
    strategy = DirectionalStrategy()

    result = strategy.assign_elevator(passenger, elevators)

    assert result == 2


def test_directional_strategy_assigns_no_elevator_if_all_moving_away_from_passenger():
    passenger = Passenger(id="", source_floor=2, destination_floor=10, request_time=0)
    elevators = [Elevator(num_floors=10, max_capacity=1) for _ in range(10)]
    for i, e in enumerate(elevators):
        e.direction = Direction.UP
        e.current_floor = 5
    strategy = DirectionalStrategy()

    result = strategy.assign_elevator(passenger, elevators)

    assert result is None
