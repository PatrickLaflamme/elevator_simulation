import sys
from typing import Dict, Union


class SystemSummary:
    min_value: int = sys.maxsize
    max_value: int = -1
    sum: int = 0
    n: int = 0
    no_action_passengers: int = 0

    def include(self, time: int):
        """
        The function updates the minimum, maximum, and sum values of a given time, and increments the count.

        :param time: The "time" parameter is an integer representing a value that you want to include in some calculations
        :type time: int
        """
        self.min_value = min(self.min_value, time)
        self.max_value = max(self.max_value, time)
        self.sum += time
        self.n += 1

    def no_action(self):
        """
        The function increments the count of passengers who did not take any action.
        """
        self.no_action_passengers += 1

    def mean(self) -> float:
        """
        The mean function calculates the average of a set of times.
        :return: The mean value of the times stored in the object.
        """
        if self.n == 0:
            return 0.0
        return self.sum / self.n

    def __dict__(self) -> Dict[str, Union[int, float]]:
        """
        The function returns a dictionary containing the summary statistics, including the minimum,
        maximum, mean, total number of passengers, and number of passengers with no action.
        :return: A dictionary is being returned. The dictionary contains the following key-value pairs:
            - mean
            - min
            - max
            - n_passengers
            - no_action_passengers
        """
        return {
            "min": self.min_value if self.min_value < sys.maxsize else None,
            "max": self.max_value if self.max_value > -1 else None,
            "mean": self.mean(),
            "n_passengers": self.n + self.no_action_passengers,
            "no_action_passengers": self.no_action_passengers
        }
