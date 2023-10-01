from io import StringIO

from elevator_controller.model.passenger import Passenger
from elevator_controller.passenger_providers import csv_passenger_provider

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
