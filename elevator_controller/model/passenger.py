from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(unsafe_hash=True, frozen=True)
class Passenger(BaseModel):
    id: str
    source_floor: int
    destination_floor: int
    request_time: int  # the time step at which they requested the elevator
