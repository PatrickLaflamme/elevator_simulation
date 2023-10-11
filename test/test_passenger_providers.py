from io import StringIO

import numpy as np

from elevator_system_design.model.passenger import Passenger
from elevator_system_design.passenger_providers import csv_passenger_provider, random_normal_floor_selection_passenger_provider, \
    random_uniform_floor_selection_passenger_provider

input_str = """time,id,source,dest
0,passenger1,1,51
0,passenger2,1,37
10,passendar3,20,1"""


def test_csv_passenger_provider():
    provider = csv_passenger_provider(StringIO(input_str))
    expected = [[Passenger("passenger1", 1, 51, 0), Passenger("passenger2", 1, 37, 0)],
                *[[] for _ in range(1, 10)],
                [Passenger("passendar3", 20, 1, 10)]]
    assert list(provider) == expected


def test_random_uniform_floor_passenger_provider():
    np.random.seed(123456)
    n_floors = 200
    provider = random_uniform_floor_selection_passenger_provider(10, 0.6, 1000, n_floors)
    for ps in provider:
        for p in ps:
            assert p.source_floor != p.destination_floor
            assert p.source_floor <= n_floors
            assert p.source_floor >= 1
            assert p.destination_floor >= 1
            assert p.destination_floor <= n_floors

def test_random_normal_floor_passenger_provider():
    np.random.seed(123456)
    n_floors = 200
    source_std = 20
    source_mean_floor = 80
    destination_mean_floor = 120
    destination_std = 20
    provider = random_normal_floor_selection_passenger_provider(
        n=5,
        p=0.6,
        n_steps=1000,
        n_floors=n_floors,
        source_std=source_std,
        source_mean_floor=source_mean_floor,
        destination_mean_floor=destination_mean_floor,
        destination_std=destination_std
    )
    sources = []
    dests = []

    for ps in provider:
        for p in ps:
            sources.append(p.source_floor)
            dests.append(p.destination_floor)
            assert p.source_floor != p.destination_floor
            assert p.source_floor <= n_floors
            assert p.destination_floor <= n_floors
            assert p.source_floor >= 1
            assert p.destination_floor >= 1
    assert source_mean_floor - 1 <= np.mean(sources) <= source_mean_floor + 1
    assert source_std - 1 <= np.std(sources) <= source_std + 1
    assert destination_mean_floor - 1 <= np.mean(dests) <= destination_mean_floor + 1
    assert destination_std - 1 <= np.std(dests) <= destination_std + 1

