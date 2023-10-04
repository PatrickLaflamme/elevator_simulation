from dataclasses import dataclass

from pydantic import BaseModel

from elevator_system_design.model.direction import Direction


@dataclass(unsafe_hash=True, frozen=True)
class Passenger(BaseModel):
    id: str
    source_floor: int
    destination_floor: int
    request_time: int  # the time step at which they requested the elevator

    @property
    def direction(self) -> Direction:
        if self.source_floor > self.destination_floor:
            return Direction.DOWN
        else:
            return Direction.UP
