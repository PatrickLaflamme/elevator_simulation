import csv
from typing import Protocol, List, Optional, Iterable, Any, IO

from elevator_controller.model.elevator import Elevator


class ElevatorSystemPersistenceStrategy(Protocol):
    def persist(self, t: int, elevators: List[Elevator]):
        ...


class Writer(Protocol):
    """
        Required because python's csv module doesn't provide a type for the native writer.
    """
    def writerow(self, row: Iterable[Any]) -> Any:
        ...

    def writerows(self, rows: Iterable[Iterable[Any]]) -> None:
        ...


class CsvPersistenceStrategy:
    wr: Writer
    n_elevators: Optional[int] = None

    def __init__(self, f: IO):
        self.wr = csv.writer(f)

    def _write_header(self):
        fieldnames = ["time", *[f"elevator_{i+1}" for i in range(self.n_elevators)]]
        self.wr.writerow(fieldnames)

    def persist(self, t: int, elevators: List[Elevator]):
        if self.n_elevators is None:
            self.n_elevators = len(elevators)
            self._write_header()
        self.wr.writerow([t, *[e.current_floor for e in elevators]])
