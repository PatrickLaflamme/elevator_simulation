from io import StringIO

from elevator_system_design.elevator_controller import ElevatorController
from elevator_system_design.passenger_providers import csv_passenger_provider
from elevator_system_design.strategies.assignment import DirectionalStrategy
from elevator_system_design.strategies.elevator_controller_persistence import CsvPersistenceStrategy
from elevator_system_design.strategies.idle import EqualSpreadIdleStrategy

input_str = """time,id,source,dest
0,passenger1,1,51
0,passenger2,1,37
10,passendar3,20,1"""

expected_csv_output = """time,elevator_1,elevator_2,elevator_3
0,8,26,42
1,7,25,41
2,6,24,40
3,5,23,39
4,4,22,38
5,3,21,38
6,2,20,38
7,1,19,38
8,2,18,38
9,3,17,38
10,4,16,38
11,5,17,37
12,6,18,36
13,7,19,35
14,8,20,34
15,9,19,33
16,10,18,32
17,11,17,31
18,12,16,30
19,13,15,29
20,14,14,28
21,15,13,27
22,16,12,26
23,17,11,26
24,18,10,26
25,19,9,26
26,20,8,26
27,21,7,26
28,22,6,26
29,23,5,26
30,24,4,26
31,25,3,26
32,26,2,26
33,27,1,26
34,28,2,27
35,29,3,28
36,30,4,29
37,31,5,30
38,32,6,31
39,33,7,32
40,34,8,33
41,35,9,34
42,36,10,35
43,37,11,36
44,38,12,37
45,39,13,38
46,40,13,38
47,41,13,38
48,42,13,38
49,43,13,38
50,44,13,38
51,45,13,38
52,46,13,38
53,47,13,38
54,48,13,38
55,49,13,38
56,50,13,38
57,51,13,38
58,50,14,39
"""


def test_full_system1():
    reader_strategy = csv_passenger_provider(StringIO(input_str))

    n_floors = 51
    n_elevators = 3
    max_elevator_capacity = 5
    csv_output = StringIO()
    state_persistence = CsvPersistenceStrategy(f=csv_output)
    elevator_system = ElevatorController(
        n_elevators=n_elevators,
        n_floors=n_floors,
        max_elevator_capacity=max_elevator_capacity,
        persistence_strategy=state_persistence,
        assignment_strategy=DirectionalStrategy(),
        idle_strategy=EqualSpreadIdleStrategy(),
        stop_time=0
    )
    elevator_system.handle_passenger_requests(reader_strategy)

    expected_stats = {'total_time': {'max': 57,
                                     'mean': 41.0,
                                     'min': 23,
                                     'n_passengers': 3,
                                     'no_action_passengers': 0},
                      'wait_time': {'max': 7,
                                    'mean': 6.0,
                                    'min': 4,
                                    'n_passengers': 3,
                                    'no_action_passengers': 0}}
    assert csv_output.getvalue().replace("\r", "") == expected_csv_output
    assert elevator_system.get_stats() == expected_stats
