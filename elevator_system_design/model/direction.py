from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

    def reverse(self) -> "Direction":
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        else:
            return Direction.IDLE
