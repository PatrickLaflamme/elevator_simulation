from heapq import heappop, heappush
from typing import List, Optional, Tuple

from elevator_controller.model.direction import Direction
from elevator_controller.model.passenger import Passenger
from elevator_controller.model.system_summary import SystemSummary


class Elevator:
    num_floors: int
    max_capacity: int
    stop_time: int
    targets: Tuple[List[int], List[int], List[int]]
    passenger_count: int = 0
    current_floor: int = 1
    current_stop_remaining: int = 0
    direction: Direction = Direction.IDLE
    idle_target: Optional[int] = None

    def __init__(self, num_floors: int, max_capacity: int, stop_time: int = 0):
        self.stop_time = stop_time
        self.num_floors = num_floors
        self.max_capacity = max_capacity
        self.targets = ([], [], [])
        self.wait_time_summary = SystemSummary()
        self.total_time_summary = SystemSummary()

    def is_empty(self) -> bool:
        return sum([len(h) for h in self.targets]) == 0

    def is_idle(self) -> bool:
        return self.direction == Direction.IDLE

    def can_accommodate(self) -> bool:
        return self.passenger_count < self.max_capacity

    def move(self):
        cur_dir_below_cur_floor, opposite_dir, cur_dir = self.targets
        for _ in range(3):
            while len(cur_dir) and (cur_dir[0] * self.direction.value) == self.current_floor:
                self.current_stop_remaining = self.stop_time
                heappop(cur_dir)
            if len(cur_dir) > 0:
                break
            opposite_start = self.current_floor
            if len(opposite_dir):
                opposite_start = opposite_dir[0] * -self.direction.value
            if (opposite_start - self.current_floor) * self.direction.value > 0:
                heappush(cur_dir, opposite_start * self.direction.value)
            else:
                self.direction = self.direction.reverse()
                self.targets = ([], cur_dir_below_cur_floor, opposite_dir)
                cur_dir_below_cur_floor, opposite_dir, cur_dir = self.targets
        if self.current_stop_remaining > 0:
            self.current_stop_remaining -= 1
            return

        if len(cur_dir) == 0:
            self.direction = Direction.IDLE
            if self.idle_target is None:
                return
            if len(cur_dir) == 0 and self.idle_target < self.current_floor:
                self.current_floor = max(1, min(self.num_floors, self.current_floor - 1))
            if len(cur_dir) == 0 and self.idle_target > self.current_floor:
                self.current_floor = max(1, min(self.num_floors, self.current_floor + 1))
        self.current_floor = max(1, min(self.num_floors, self.current_floor + self.direction.value))

    def assign(self, passenger: Passenger) -> bool:
        cur_dir_below_cur_floor, opposite_dir, cur_dir = self.targets
        if self.is_idle() and passenger.source_floor > self.current_floor:
            self.direction = Direction.UP
            heappush(cur_dir, passenger.source_floor)
        elif self.is_idle() and passenger.source_floor < self.current_floor:
            self.direction = Direction.DOWN
            heappush(cur_dir, passenger.source_floor * -1)

        if passenger.direction.value * self.direction.value < 0:
            heappush(opposite_dir, passenger.source_floor * passenger.direction.value)
            heappush(opposite_dir, passenger.destination_floor * passenger.direction.value)
        elif (passenger.source_floor - self.current_floor) * self.direction.value < 0:
            heappush(cur_dir_below_cur_floor, passenger.source_floor * passenger.direction.value)
            heappush(cur_dir_below_cur_floor, passenger.destination_floor * passenger.direction.value)
        else:
            heappush(cur_dir, passenger.source_floor * passenger.direction.value)
            heappush(cur_dir, passenger.destination_floor * passenger.direction.value)
        return True

    def embark(self, passenger: Passenger) -> bool:
        if passenger.source_floor != self.current_floor:
            return False
        if not self.can_accommodate():
            return False
        if passenger.direction != self.direction:
            if self.is_idle():
                self.direction = passenger.direction
            else:
                return False
        self.passenger_count += 1
        _, _, cur_dir = self.targets
        heappush(cur_dir, passenger.destination_floor * passenger.direction.value)
        return True

    def disembark(self, passenger: Passenger) -> bool:
        if passenger.destination_floor != self.current_floor:
            return False
        self.passenger_count -= 1
        return True
