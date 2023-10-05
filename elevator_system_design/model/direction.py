from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

    def reverse(self) -> "Direction":
        """
        Convenience function to reverse the direction.
        :return: The reverse direction of the given direction. If the direction is UP, it will return DOWN. If the direction
        is DOWN, it will return UP. Otherwise, it will return IDLE.
        """
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        else:
            return Direction.IDLE
