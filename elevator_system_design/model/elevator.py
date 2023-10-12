from heapq import heappop, heappush
from typing import List, Optional, Tuple

from elevator_system_design.log import logger
from elevator_system_design.model.direction import Direction
from elevator_system_design.model.passenger import Passenger


class InvalidDisembarkRequest(Exception):
    def __init__(self, passenger_id: str, passenger_dest_floor: int, current_elevator_floor: int):
        self.passenger_id = passenger_id
        self.passenger_dest_floor = passenger_dest_floor
        self.current_elevator_floor = current_elevator_floor


class InvalidEmbarkRequest(Exception):
    def __init__(self, passenger_id: str, passenger_source_floor: int, current_elevator_floor: int):
        self.passenger_id = passenger_id
        self.passenger_source_floor = passenger_source_floor
        self.current_elevator_floor = current_elevator_floor


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
        """
        The function initializes an elevator object with the specified number of floors, maximum capacity, and optional stop
        time.

        :param num_floors: The `num_floors` parameter represents the total number of floors in the building
        :type num_floors: int
        :param max_capacity: The `max_capacity` parameter represents the maximum number of people that the elevator can hold
        at a time
        :type max_capacity: int
        :param stop_time: The `stop_time` parameter represents the time it takes for the elevator to stop at each floor.
        Defaults to 0.
        :type stop_time: int (optional)
        """
        self.stop_time = stop_time
        self.num_floors = num_floors
        self.max_capacity = max_capacity
        self.targets = ([], [], [])

    def is_empty(self) -> bool:
        """
        The function `is_empty` checks if all the elevator is empty and has no target floors.
        :return: a boolean value indicating whether the elevator has any target floors.
        """
        return sum([len(h) for h in self.targets]) == 0

    def is_idle(self) -> bool:
        """
        The function checks if the elevator is idle.
        :return: a boolean value, specifically whether the direction is equal to the IDLE direction.
        """
        return self.direction == Direction.IDLE

    def can_accommodate(self) -> bool:
        """
        The function checks if the current passenger count is less than the maximum capacity.
        :return: a boolean value, indicating whether the passenger count is less than the maximum capacity.
        """
        return self.passenger_count < self.max_capacity

    def has_target_with_direction(self, target: int, direction: Direction) -> bool:
        """
        The function checks if a target already exists in the provided direction for this elevator.
        attribute of the object.

        :param target: The target parameter is an integer representing the target value that we are checking for
        :type target: int
        :param direction: The `direction` parameter is of type `Direction`, which is likely an enumeration or a custom class
        representing different directions (e.g., north, south, east, west)
        :type direction: Direction
        :return: a boolean value.
        """
        target_with_dir = target * direction.value
        return any([target_with_dir in h for h in self.targets])

    def distance_from(self, target: int, direction: Direction) -> int:
        """
        The function calculates the distance from the current floor to a target floor based on the elevator's direction and
        current targets.

        :param target: The `target` parameter in the `distance_from` method is an integer representing the floor number that
        the elevator needs to reach
        :type target: int
        :param direction: The `direction` parameter is of type `Direction`, which is an enumeration. It represents the
        direction in which the target is located relative to the current position
        :type direction: Direction
        :return: an integer value, which represents the distance from the current floor to the target floor.
        """
        if self.direction == Direction.IDLE:
            return abs(target - self.current_floor)
        target_with_dir = target * direction.value
        if self.current_floor * self.direction.value < target_with_dir:
            return abs(target - self.current_floor) + sum({1 for t in self.targets[-1] if t <= target_with_dir}) * self.stop_time
        end_of_current_sweep = abs(max(abs(max(self.targets[-1]) if self.targets[-1] else 0) * self.direction.value, abs(max(self.targets[1]) if self.targets[1] else 0) * self.direction.value))
        distance_to_turn = abs(self.current_floor - abs(end_of_current_sweep)) + len(set(self.targets[-1])) * self.stop_time
        if direction != self.direction:
            distance_from_turn_to_target = abs(abs(end_of_current_sweep) - target) + sum({1 for t in self.targets[1] if t <= target_with_dir}) * self.stop_time
            return distance_to_turn + distance_from_turn_to_target
        end_of_next_sweep = abs(max(abs(max(self.targets[0]) if self.targets[0] else 0) * self.direction.value, abs(max(self.targets[1]) if self.targets[1] else 0) * self.direction.value))
        distance_to_next_turn = abs(abs(end_of_next_sweep) - abs(end_of_current_sweep)) + len(set(self.targets[1])) * self.stop_time
        distance_from_next_turn_to_target = abs(abs(end_of_next_sweep) - target) + sum({1 for t in self.targets[0] if t <= target_with_dir}) * self.stop_time
        return distance_to_turn + distance_to_next_turn + distance_from_next_turn_to_target

    def adjust_targets(self):
        """
        The function adjusts the elevator's target floors based on its current direction and floor.
        """
        cur_dir_below_cur_floor, opposite_dir, cur_dir = self.targets
        for _ in range(3):
            while len(cur_dir) and cur_dir[0] <= self.current_floor * self.direction.value:
                self.current_stop_remaining = self.stop_time
                heappop(cur_dir)
            if len(cur_dir) > 0:
                break
            opposite_start = self.current_floor * -self.direction.value
            if len(opposite_dir):
                opposite_start = opposite_dir[0] * -self.direction.value
            if (opposite_start - self.current_floor) * self.direction.value > 0:
                heappush(cur_dir, opposite_start * self.direction.value)
            else:
                self.direction = self.direction.reverse()
                self.targets = ([], cur_dir_below_cur_floor, opposite_dir)
                cur_dir_below_cur_floor, opposite_dir, cur_dir = self.targets

    def move(self):
        """
        The function `move` is responsible for adjusting the elevator's targets and moving the elevator accordingly.
        This can be considered to be the movement achieved in one time-step for this elevator.
        :return: The code does not explicitly return anything.
        """
        self.adjust_targets()
        cur_dir_below_cur_floor, opposite_dir, cur_dir = self.targets
        if self.current_stop_remaining > 0:
            self.current_stop_remaining -= 1
            return

        if self.is_empty():
            self.direction = Direction.IDLE
            if self.idle_target is None:
                return
            if self.is_empty() and self.idle_target < self.current_floor:
                self.current_floor = max(1, min(self.num_floors, self.current_floor - 1))
            if self.is_empty() and self.idle_target > self.current_floor:
                self.current_floor = max(1, min(self.num_floors, self.current_floor + 1))
        elif cur_dir[0] > 0:
            self.direction = Direction.UP
        elif cur_dir[0] < 0:
            self.direction = Direction.DOWN
        self.current_floor = max(1, min(self.num_floors, self.current_floor + self.direction.value))
        self.adjust_targets()

    def assign(self, passenger: Passenger) -> bool:
        """
        The `assign` function assigns a passenger to an elevator and updates the elevator's targets based on the passenger's
        source and destination floors.

        :param passenger: The "passenger" parameter is an instance of the "Passenger" class
        :type passenger: Passenger
        :return: a boolean value, which is always True.
        """
        cur_dir_below_cur_floor, opposite_dir, cur_dir = self.targets
        if self.is_empty() and passenger.source_floor > self.current_floor:
            self.direction = Direction.UP
            heappush(cur_dir, passenger.source_floor)
        elif self.is_empty() and passenger.source_floor < self.current_floor:
            self.direction = Direction.DOWN
            heappush(cur_dir, passenger.source_floor * -1)

        if passenger.direction.value * self.direction.value < 0:
            heappush(opposite_dir, passenger.source_floor * passenger.direction.value)
            heappush(opposite_dir, passenger.destination_floor * passenger.direction.value)
        elif (passenger.source_floor - self.current_floor) * self.direction.value <= 0:
            heappush(cur_dir_below_cur_floor, passenger.source_floor * passenger.direction.value)
            heappush(cur_dir_below_cur_floor, passenger.destination_floor * passenger.direction.value)
        else:
            heappush(cur_dir, passenger.source_floor * passenger.direction.value)
            heappush(cur_dir, passenger.destination_floor * passenger.direction.value)
        return True

    def embark(self, passenger: Passenger) -> bool:
        """
        The `embark` function checks if the elevator can accommodate a passenger, if it is on the correct floor and
        moving in the correct direction to embark the passenger. If so, it increments the passenger count, considering
        the passenger to be on the elevator.

        :param passenger: The "passenger" parameter is of type "Passenger"
        :type passenger: Passenger
        :return: The method `embark` returns a boolean value.
        """
        if passenger.source_floor != self.current_floor:
            logger.error(f"Attempt to embark passenger {passenger.id} from floor {passenger.source_floor} while the "
                         f"elevator is on floor {self.current_floor}")
            raise InvalidEmbarkRequest(passenger_id=passenger.id,
                                       passenger_source_floor=passenger.source_floor,
                                       current_elevator_floor=self.current_floor)
        if not self.can_accommodate():
            logger.debug(f"Elevator is too full to embark passenger {passenger.id}")
            return False
        if passenger.direction != self.direction:
            logger.debug(f"Elevator is moving in the wrong direction to embark passenger {passenger.id}: "
                         f"passenger direction: {passenger.direction}; elevator direction: {self.direction}")
            return False
        self.passenger_count += 1
        return True

    def disembark(self, passenger: Passenger):
        """
        The `disembark` function checks if a passenger wants to disembark at the current floor and updates the passenger
        count.

        :param passenger: The "passenger" parameter is an instance of the "Passenger" class. It represents a passenger who
        wants to disembark from the elevator
        :type passenger: Passenger
        """
        if passenger.destination_floor != self.current_floor:
            raise InvalidDisembarkRequest(passenger_id=passenger.id,
                                          passenger_dest_floor=passenger.destination_floor,
                                          current_elevator_floor=self.current_floor)
        self.passenger_count -= 1
