from csv import DictReader
from typing import Iterator, List, IO

from elevator_controller.model.passenger import Passenger


def csv_passenger_provider(f: IO) -> Iterator[List[Passenger]]:
    reader = DictReader(f)
    i = 0
    passengers = []
    for p_dict in reader:
        passenger = Passenger(request_time=int(p_dict.get("time")),
                              id=p_dict.get("id"),
                              source_floor=int(p_dict.get("source")),
                              destination_floor=int(p_dict.get("dest")))
        while passenger.request_time > i:
            yield passengers
            passengers = []
            i += 1
        passengers.append(passenger)
    while len(passengers) and passengers[0].request_time > i:
        yield []
        i += 1
    yield passengers
