from io import StringIO

from elevator_controller.model.elevator import Elevator
from elevator_controller.strategies.elevator_system_persistence import CsvPersistenceStrategy


def test_csv_elevator_persistence():
    # given
    elevators = [Elevator(num_floors=10, max_capacity=1), Elevator(num_floors=10, max_capacity=1)]
    output = StringIO()
    strategy = CsvPersistenceStrategy(output)

    # when
    strategy.persist(0, elevators)
    elevators[0].current_floor += 1
    strategy.persist(1, elevators)

    # then
    expected = "time,elevator_1,elevator_2\r\n0,1,1\r\n1,2,1\r\n"
    assert output.getvalue() == expected
