from elevator_system_design.model.elevator import Elevator, Direction
from elevator_system_design.model.passenger import Passenger


def test_is_empty():
    e = Elevator(num_floors=10, max_capacity=5)
    assert e.is_empty()
    e2 = Elevator(num_floors=10, max_capacity=1)
    e2.assign(Passenger(id="", source_floor=1, destination_floor=10, request_time=0))
    assert not e2.is_empty()


def test_can_accommodate():
    e = Elevator(num_floors=10, max_capacity=1)
    assert e.can_accommodate()
    e2 = Elevator(num_floors=10, max_capacity=1)
    e2.direction = Direction.UP
    assert e2.embark(Passenger(id="", source_floor=1, destination_floor=10, request_time=0))
    assert not e2.can_accommodate()


def test_is_idle():
    e = Elevator(num_floors=10, max_capacity=1)
    assert e.is_idle()
    e2 = Elevator(num_floors=10, max_capacity=1)
    e2.direction = Direction.UP
    assert not e2.is_idle()


def test_move_drifts_toward_idle_target():
    e = Elevator(num_floors=10, max_capacity=1)
    assert e.current_floor == 1
    e.idle_target = 2
    e.move()
    assert e.current_floor == 2
    e.idle_target = 1
    e.move()
    assert e.current_floor == 1


def test_move_moves_to_pick_up_assigned_passenger():
    e = Elevator(num_floors=10, max_capacity=1)
    assert e.assign(Passenger(destination_floor=5, request_time=0, id="", source_floor=2))
    e.move()
    assert e.current_floor == 2
    assert not e.is_empty()
    e.assign(Passenger(destination_floor=5, request_time=0, id="", source_floor=3))
    e.move()
    e.move()
    assert e.current_floor == 4
    # the target heap has the two passengers' destination  floors.
    assert e.targets[-1] == [5, 5]


def test_move_changes_elevator_to_idle_after_all_targets_achieved():
    e = Elevator(num_floors=10, max_capacity=1)
    assert e.assign(Passenger(destination_floor=5, request_time=0, id="", source_floor=2))
    e.move()
    e.move()
    e.move()
    e.move()
    e.move()
    assert e.current_floor == 5
    # the target heap has the two passengers' destination  floors.
    assert e.is_idle()


def test_assign_passenger_puts_current_floor_on_next_sweep():
    e = Elevator(num_floors=10, max_capacity=1)
    e.current_floor = 3
    e.assign(Passenger(destination_floor=5, request_time=0, id="", source_floor=3))
    # current sweep is empty
    assert e.targets[-1] == []
    # next upward sweep is populated with the source and dest floors of the passenger
    assert e.targets[0] == [3, 5]

