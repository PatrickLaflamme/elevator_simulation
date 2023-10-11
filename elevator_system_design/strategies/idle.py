from math import floor
import numpy as np
from typing import Protocol, List

from elevator_system_design.model.elevator import Elevator


class ElevatorIdleStrategy(Protocol):
    def position_idle_elevators(self, elevators: List[Elevator]):
        """
        The function positions idle elevators.

        :param elevators: The "elevators" parameter is a list of Elevator objects
        :type elevators: List[Elevator]
        """
        ...


class MiddleFloorIdleStrategy:
    def position_idle_elevators(self, elevators: List[Elevator]):
        """
        The function sets the idle target floor for each elevator to the middle floor of the building.

        :param elevators: The "elevators" parameter is a list of Elevator objects
        :type elevators: List[Elevator]
        """
        for elevator in elevators:
            middle_floor = elevator.num_floors // 2
            elevator.idle_target = middle_floor


class EqualSpreadIdleStrategy:
    def position_idle_elevators(self, elevators: List[Elevator]):
        """
        The function positions idle elevators evenly across the floors they can reach.

        :param elevators: The `elevators` parameter is a list of `Elevator` objects
        :type elevators: List[Elevator]
        """
        assert len(elevators) > 0
        assert len(set([e.num_floors for e in elevators])) == 1
        top_floor = elevators[0].num_floors
        idle_elevators = [e for e in elevators if e.is_empty()]
        for i in range(len(idle_elevators)):
            elevator = idle_elevators[i]
            target_floor = round((i + 0.5) * top_floor / (len(idle_elevators)))
            elevator.idle_target = target_floor


class HistoricalDistributionIdleStrategy:
    def __init__(self, historical_counts: List[int]):
        """
        This init allows the user to specify historical data observed prior to simulation start
        """
        self.total_obs = sum(historical_counts)
        self.historical_counts = [i + 1  for i, h in enumerate(historical_counts) for _ in range(h)]

    def position_idle_elevators(self, elevators: List[Elevator]):
        """
        This strategy positions idle elevators across the floors, weighted by the frequency at which
        each floor is a source floor for historical passenger requests. 

        :param elevators: The `elevators` parameter is a list of `Elevator` objects
        :type elevators: List[Elevator]
        """
        floor_counts = set([e.num_floors for e in elevators])
        assert len(elevators) > 0
        assert len(floor_counts) == 1
        assert floor_counts.pop() >= max(self.historical_counts)
        idle_elevators = [e for e in elevators if e.is_empty()]
        i = 0
        for i in range(len(idle_elevators)):
            elevator = idle_elevators[i]
            target_quantile = (i + 0.5) / len(idle_elevators)
            elevator.idle_target = floor(np.quantile(self.historical_counts, target_quantile))

