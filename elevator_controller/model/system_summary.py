import sys
from typing import Dict, Union


class SystemSummary:
    min_value: int = sys.maxsize
    max_value: int = -1
    sum: int = 0
    n: int = 0

    def add(self, time: int):
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
            "mean": self.mean()
        }
