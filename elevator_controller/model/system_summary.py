import sys
from typing import Dict, Union


class SystemSummary:
    min_value: int = sys.maxsize
    max_value: int = -1
    sum: int = 0
    n: int = 0

    def include(self, time: int):
        self.min_value = min(self.min_value, time)
        self.max_value = max(self.max_value, time)
        self.sum += time
        self.n += 1

    def mean(self) -> float:
        return self.sum / self.n

    def __dict__(self) -> Dict[str, Union[int, float]]:
        return {
            "min": self.min_value,
            "max": self.max_value,
            "mean": self.mean(),
            "n_passengers": self.n
        }

    def __add__(self, other: "SystemSummary") -> "SystemSummary":
        new_summary = SystemSummary()
        new_summary.min_value = min(self.min_value, other.min_value)
        new_summary.max_value = max(self.max_value, other.max_value)
        new_summary.sum = self.sum + other.sum
        new_summary.n = self.n + other.n
        return new_summary
