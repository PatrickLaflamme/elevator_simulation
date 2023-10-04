from elevator_system_design.model.direction import Direction


def test_reverse():
    d = Direction.UP
    assert d.reverse() == Direction.DOWN
    d = Direction.DOWN
    assert d.reverse() == Direction.UP
