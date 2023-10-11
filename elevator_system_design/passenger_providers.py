from csv import DictReader
from typing import Iterator, List, IO, Optional

import numpy as np

from elevator_system_design.log import logger
from elevator_system_design.model.passenger import Passenger


def csv_passenger_provider(f: IO) -> Iterator[List[Passenger]]:
    """
    The function `csv_passenger_provider` reads a CSV file and yields a list of passengers for each request time. If no
    passengers are present for a given time, and empty list is returend.

    :param f: The parameter `f` is an input file object of type `IO`. It is used to read the contents of a CSV file that
    contains information about passengers
    :type f: IO
    """
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


def random_uniform_floor_selection_passenger_provider(n: int, p: float, n_steps: int, n_floors: int) -> Iterator[
    List[Passenger]]:
    """
    The function generates randomly sampled passengers for each time step, with specified parameters for the number of
    passengers, probability of a passenger appearing, number of time steps, and number of floors.

    :param n: The parameter `n` represents the total number of passengers that can be generated, sampled from a binomial distribution
    :type n: int
    :param p: The parameter `p` represents the probability of a passenger arriving at each time step. It is used in the
    `np.random.binomial` function to determine the number of passengers that arrive at each time step
    :type p: float
    :param n_steps: The parameter `n_steps` represents the number of time steps for which passengers will be generated
    :type n_steps: int
    :param n_floors: The parameter `n_floors` represents the total number of floors in the building
    :type n_floors: int
    """
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


def random_normal_floor_selection_passenger_provider(
        n: int,
        p: float,
        n_steps: int,
        n_floors: int,
        source_mean_floor: Optional[int] = None,
        source_std: Optional[float] = None,
        destination_mean_floor: Optional[int] = None,
        destination_std: Optional[float] = None) -> Iterator[List[Passenger]]:
    if source_mean_floor is None:
        source_mean_floor = n_floors // 2
    if source_std is None:
        source_std = n_floors // 9
    if destination_mean_floor is None:
        destination_mean_floor = n_floors // 2
    if destination_std is None:
        destination_std = n_floors // 9
    i = 0
    logger.info("generating randomly sampled passengers for each time step")
    for time_step, n_passengers in enumerate(np.random.binomial(n=n, p=p, size=n_steps)):
        source_floor = round(np.random.normal(loc=source_mean_floor, scale=source_std))
        while source_floor > n_floors:
            source_floor = round(np.random.normal(loc=source_mean_floor, scale=source_std))
        destination_floor = round(np.random.normal(loc=destination_mean_floor, scale=destination_std))
        while destination_floor > n_floors or destination_floor == source_floor:
            destination_floor = round(np.random.normal(loc=destination_mean_floor, scale=destination_std))
        yield [Passenger(
            id=f"passenger{i + j}",
            source_floor=source_floor,
            destination_floor=destination_floor,
            request_time=time_step
        ) for j in range(n_passengers)]
        i += n_passengers
