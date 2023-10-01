from io import StringIO

from elevator_controller.model.elevator import Elevator
from elevator_controller.strategies.elevator_system_persistence import CsvPersistenceStrategy


def test_csv_elevator_persistence():
    # given
    elevators = [Elevator(current_floor=0), Elevator(current_floor=0)]
    output = StringIO()
    strategy = CsvPersistenceStrategy(output)

    # when
    strategy.persist(0, elevators)
    elevators[0].current_floor += 1
    strategy.persist(1, elevators)

    # then
    expected = "time,elevator_1,elevator_2\r\n0,0,0\r\n1,1,0\r\n"
    assert output.getvalue() == expected
