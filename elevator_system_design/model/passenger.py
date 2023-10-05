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
        """
        The function determines the passenger's direction of travel based on the source and destination floors.
        :return: the direction in which the passenger wants to move. If the source floor is greater than the destination
        floor, it will return Direction.DOWN. Otherwise, it will return Direction.UP.
        """
        if self.source_floor > self.destination_floor:
            return Direction.DOWN
        else:
            return Direction.UP
