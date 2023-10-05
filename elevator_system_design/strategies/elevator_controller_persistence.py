import csv
from typing import Protocol, List, Optional, Iterable, Any, IO

from elevator_system_design.model.elevator import Elevator


class ElevatorControllerPersistenceStrategy(Protocol):
    def persist(self, t: int, elevators: List[Elevator]):
        """
        The persist function takes an integer t and a list of Elevator objects as input and performs some operation.

        :param t: The parameter `t` represents the current time in seconds. It is an integer value
        :type t: int
        :param elevators: The `elevators` parameter is a list of `Elevator` objects. Each `Elevator` object represents an
        elevator in a building
        :type elevators: List[Elevator]
        """
        ...


class Writer(Protocol):
    """
        Required because python's csv module doesn't provide a type for the native writer.
    """
    def writerow(self, row: Iterable[Any]) -> Any:
        ...

    def writerows(self, rows: Iterable[Iterable[Any]]) -> None:
        ...


class NoopPersistenceStrategy:
    def persist(self, t: int, elevators: List[Elevator]):
        """
        The persist function takes an integer t and a list of Elevator objects as parameters.

        :param t: An integer representing the current time in seconds
        :type t: int
        :param elevators: The `elevators` parameter is a list of `Elevator` objects. Each `Elevator` object represents an
        elevator in a building and contains information such as its current floor, direction, and status
        :type elevators: List[Elevator]
        """
        pass


class CsvPersistenceStrategy:
    wr: Writer
    n_elevators: Optional[int] = None

    def __init__(self, f: IO):
        self.wr = csv.writer(f)

    def _write_header(self):
        fieldnames = ["time", *[f"elevator_{i+1}" for i in range(self.n_elevators)]]
        self.wr.writerow(fieldnames)

    def persist(self, t: int, elevators: List[Elevator]):
        """
        The `persist` function writes the current floor of each elevator to a CSV file along with the current time.

        :param t: The parameter "t" represents the current time in the simulation. It is an integer value
        :type t: int
        :param elevators: The `elevators` parameter is a list of `Elevator` objects. Each `Elevator` object represents an
        elevator and contains information such as the current floor of the elevator
        :type elevators: List[Elevator]
        """
        if self.n_elevators is None:
            self.n_elevators = len(elevators)
            self._write_header()
        self.wr.writerow([t, *[e.current_floor for e in elevators]])
