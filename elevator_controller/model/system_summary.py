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
        if self.n == 0:
            return 0.0
        return self.sum / self.n

    def __dict__(self) -> Dict[str, Union[int, float]]:
        return {
            "min": self.min_value if self.min_value < sys.maxsize else None,
            "max": self.max_value if self.max_value > -1 else None,
            "mean": self.mean(),
            "n_passengers": self.n
        }
