from typing import List

from pydantic import BaseModel

from elevator_controller.model.direction import Direction
from elevator_controller.model.passenger import Passenger


class Elevator(BaseModel):
    current_floor: int = 0
    pending_passengers: List[Passenger] = []
    embarked_passengers: List[Passenger] = []
    direction: Direction = Direction.IDLE
    idle_target: int
    top_floor: int
    max_passengers: int

    def is_empty(self) -> bool:
        return len(self.embarked_passengers) == 0

    def is_idle(self) -> bool:
        return self.direction == Direction.IDLE

    def can_accommodate(self) -> bool:
        return len(self.embarked_passengers) < self.max_passengers

    def move(self):
        while self.pending_passengers and self.current_floor == self.pending_passengers[0].source_floor:
            self.embarked_passengers.append(self.pending_passengers.pop(0))
        while self.embarked_passengers and self.current_floor == self.embarked_passengers[0].destination_floor:
            self.embarked_passengers.pop(0)

        # First set direction based on embarked passengers
        if self.embarked_passengers:
            self.direction = self.embarked_passengers[0].direction
        # Then set direction based on pending passengers
        elif self.pending_passengers and self.pending_passengers[0].source_floor > self.current_floor:
            self.direction = Direction.UP
        elif self.pending_passengers and self.pending_passengers[0].source_floor < self.current_floor:
            self.direction = Direction.DOWN
        # Then set direction based on the idle target
        elif self.idle_target < self.current_floor:
            self.direction = Direction.DOWN
        elif self.idle_target > self.current_floor:
            self.direction = Direction.UP
        else:
            self.direction = Direction.IDLE
        self.current_floor += self.direction.value

    def request_pickup(self, passenger: Passenger) -> bool:
        if self.can_accommodate():
            self.pending_passengers.append(passenger)
            return True
        return False

