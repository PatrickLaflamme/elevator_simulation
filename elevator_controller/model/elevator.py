from typing import List, Optional, Dict
from heapq import heappop, heappush

from elevator_controller.model.direction import Direction
from elevator_controller.model.passenger import Passenger
from elevator_controller.model.system_summary import SystemSummary


class Elevator:
    top_floor: int
    max_passengers: int
    current_floor: int = 1
    pending_passengers: Dict[Direction, List[Passenger]]
    embarked_passengers: Dict[Direction, List[Passenger]]
    direction: Direction = Direction.IDLE
    idle_target: Optional[int] = None
    wait_time_summary: SystemSummary
    total_time_summary: SystemSummary

    def __init__(self, top_floor: int, max_passengers: int):
        self.top_floor = top_floor
        self.max_passengers = max_passengers
        self.pending_passengers = {
            Direction.UP: [],
            Direction.DOWN: []
        }
        self.embarked_passengers = {
            Direction.UP: [],
            Direction.DOWN: []
        }
        self.wait_time_summary = SystemSummary()
        self.total_time_summary = SystemSummary()

    def is_empty(self) -> bool:
        return len(self.embarked_passengers) == 0 and len(self.pending_passengers) == 0

    def is_idle(self) -> bool:
        return self.direction == Direction.IDLE

    def can_accommodate(self) -> bool:
        return len(self.embarked_passengers) < self.max_passengers

    def move(self, time: int):
        while self.embarked_passengers and self.current_floor == self.embarked_passengers[self.direction][0].destination_floor:
            arrived_passenger = heappop(self.embarked_passengers[self.direction])
            self.total_time_summary.include(time - arrived_passenger.request_time)
        while self.can_accommodate() and self.pending_passengers and self.current_floor == self.pending_passengers[0].source_floor and self.pending_passengers[0].direction == self.direction:
            new_passenger = heappop(self.pending_passengers[self.direction])
            self.embarked_passengers.append(new_passenger)
            self.wait_time_summary.include(time - new_passenger.request_time)

        # First set direction based on embarked passengers
        if self.embarked_passengers:
            self.direction = self.embarked_passengers[0].direction
        # Then set direction based on pending passengers
        elif self.pending_passengers and self.pending_passengers[0].source_floor > self.current_floor:
            self.direction = Direction.UP
        elif self.pending_passengers and self.pending_passengers[0].source_floor < self.current_floor:
            self.direction = Direction.DOWN
        # Then set direction based on the idle target
        elif self.idle_target and self.idle_target < self.current_floor:
            self.direction = Direction.DOWN
        elif self.idle_target and self.idle_target > self.current_floor:
            self.direction = Direction.UP
        else:
            self.direction = Direction.IDLE
        self.current_floor = min(max(self.current_floor + self.direction.value, 1), self.top_floor)

    def request_pickup(self, passenger: Passenger) -> bool:
        if passenger.source_floor < 1 or passenger.destination_floor > self.top_floor:
            return False
        if self.can_accommodate() and passenger.source_floor == self.current_floor and passenger.direction == self.direction:
            self.embarked_passengers[self.direction].append(passenger)
        elif passenger.source_floor > self.current_floor:
            self.pending_passengers[Direction.UP].append(passenger)
        elif passenger.source_floor < self.current_floor:
            self.pending_passengers[Direction.DOWN].append(passenger)
        else:
            return False
        return True
