from io import StringIO

import numpy as np

from elevator_system_design.model.passenger import Passenger
from elevator_system_design.passenger_providers import csv_passenger_provider, \
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
            assert p.destination_floor <= n_floors
