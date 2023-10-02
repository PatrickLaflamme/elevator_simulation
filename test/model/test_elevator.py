from elevator_controller.model.elevator import Elevator, Direction
from elevator_controller.model.passenger import Passenger


def test_is_empty():
    e = Elevator(idle_target=0, top_floor=10, max_passengers=5)
    assert e.is_empty()
    e2 = Elevator(idle_target=0,
                  top_floor=10,
                  max_passengers=5,
                  embarked_passengers=[Passenger("", source_floor=0, destination_floor=1, request_time=0)])
    assert not e2.is_empty()


def test_can_accommodate():
    e = Elevator(idle_target=0, top_floor=10, max_passengers=5)
    assert e.can_accommodate()
    e2 = Elevator(idle_target=0,
                  top_floor=10,
                  max_passengers=5,
                  embarked_passengers=[Passenger("", source_floor=0, destination_floor=1, request_time=0)] * 5)
    assert not e2.can_accommodate()


def test_is_idle():
    e = Elevator(idle_target=0, top_floor=10, max_passengers=5)
    assert e.is_idle()
    e2 = Elevator(direction=Direction.UP, idle_target=0, top_floor=10, max_passengers=5)
    assert not e2.is_idle()


def test_move():
    e = Elevator(idle_target=0, top_floor=10, max_passengers=1)
    assert e.current_floor == 0
    e.idle_target = 1
    e.move()
    assert e.current_floor == 1
    e.idle_target = 0
    e.move()
    assert e.current_floor == 0
    assert e.request_pickup(Passenger(destination_floor=5, request_time=0, id="", source_floor=0))
    e.move()
    assert e.current_floor == 1
    assert not e.is_empty()
    e.request_pickup(Passenger(destination_floor=5, request_time=0, id="", source_floor=2))
    e.move()
    e.move()
    assert e.current_floor == 3
    assert not len(e.pending_passengers)
