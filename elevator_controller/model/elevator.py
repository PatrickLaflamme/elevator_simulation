from enum import Enum
from typing import List

from pydantic import BaseModel


class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0


class Elevator(BaseModel):
    current_floor: int = 0
    target_floors: List[int] = []
    direction: Direction = Direction.IDLE
    passengers: int = 0
    MAX_PASSENGERS: int = 5
