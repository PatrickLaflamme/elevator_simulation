from io import StringIO

from elevator_controller.elevator_system import ElevatorSystem
from elevator_controller.passenger_providers import csv_passenger_provider
from elevator_controller.strategies.assignment import DirectionalStrategy
from elevator_controller.strategies.elevator_system_persistence import CsvPersistenceStrategy
from elevator_controller.strategies.idle import EqualSpreadIdleStrategy

input_str = """time,id,source,dest
0,passenger1,1,51
0,passenger2,1,37
10,passendar3,20,1"""

expected_csv_output = """time,elevator_1,elevator_2,elevator_3
0,12,25,38
1,11,24,37
2,10,23,36
3,9,22,35
4,8,21,34
5,7,20,34
6,6,19,34
7,5,18,34
8,4,17,34
9,3,17,34
10,2,17,34
11,1,18,33
12,2,19,32
13,3,20,31
14,4,19,30
15,5,18,29
16,6,17,28
17,7,16,27
18,8,15,26
19,9,14,25
20,10,13,25
21,11,12,25
22,12,11,25
23,13,10,25
24,14,9,25
25,15,8,25
26,16,7,25
27,17,6,25
28,18,5,25
29,19,4,25
30,20,3,25
31,21,2,25
32,22,1,25
33,23,2,25
34,24,3,26
35,25,4,27
36,26,5,28
37,27,6,29
38,28,7,30
39,29,8,31
40,30,9,32
41,31,10,33
42,32,11,34
43,33,12,34
44,34,13,34
45,35,14,34
46,36,15,34
47,37,16,34
48,38,17,34
49,39,17,34
50,40,17,34
51,41,17,34
52,42,17,34
53,43,17,34
54,44,17,34
55,45,17,34
56,46,17,34
57,47,17,34
58,48,17,34
59,49,17,34
60,50,17,34
61,51,17,34
62,50,17,34
"""


def test_full_system1():
    reader_strategy = csv_passenger_provider(StringIO(input_str))

    n_floors = 51
    n_elevators = 3
    max_elevator_capacity = 5
    csv_output = StringIO()
    state_persistence = CsvPersistenceStrategy(f=csv_output)
    elevator_system = ElevatorSystem(
        n_elevators=n_elevators,
        n_floors=n_floors,
        max_elevator_capacity=max_elevator_capacity,
        persistence_strategy=state_persistence,
        assignment_strategy=DirectionalStrategy(),
        idle_strategy=EqualSpreadIdleStrategy(),
        stop_time=0
    )
    elevator_system.handle_passenger_requests(reader_strategy)

    expected_stats = {'total_time': {'max': 61,
                                     'mean': 43.333333333333336,
                                     'min': 22,
                                     'n_passengers': 3,
                                     'no_action_passengers': 0},
                      'wait_time': {'max': 11,
                                    'mean': 8.333333333333334,
                                    'min': 3,
                                    'n_passengers': 3,
                                    'no_action_passengers': 0}}
    assert csv_output.getvalue().replace("\r", "") == expected_csv_output
    assert elevator_system.get_stats() == expected_stats
