from csv import DictReader
from typing import Iterator, List, IO

import numpy as np

from elevator_system_design.log import logger
from elevator_system_design.model.passenger import Passenger


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


def random_uniform_floor_selection_passenger_provider(n: int, p: float, n_steps: int, n_floors: int) -> Iterator[List[Passenger]]:
    i = 0
    logger.info("generating randomly sampled passengers for each time step")
    for time_step, n_passengers in enumerate(np.random.binomial(n=n, p=p, size=n_steps)):
        source_floor = round(np.random.uniform(1, n_floors + 1))
        while source_floor > n_floors:
            source_floor = round(np.random.uniform(1, n_floors + 1))
        destination_floor = round(np.random.uniform(1, n_floors + 1))
        while destination_floor > n_floors or destination_floor == source_floor:
            destination_floor = round(np.random.uniform(1, n_floors + 1))
        yield [Passenger(
            id=f"passenger{i + j}",
            source_floor=source_floor,
            destination_floor=destination_floor,
            request_time=time_step
        ) for j in range(n_passengers)]
        i += n_passengers

