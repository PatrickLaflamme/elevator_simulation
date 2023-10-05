from io import StringIO

import numpy as np

from elevator_system_design.elevator_controller import ElevatorController
from elevator_system_design.log import logger
from elevator_system_design.passenger_providers import random_uniform_floor_selection_passenger_provider
from elevator_system_design.strategies.assignment import ExistingStopStrategy
from elevator_system_design.strategies.elevator_controller_persistence import CsvPersistenceStrategy
from elevator_system_design.strategies.idle import EqualSpreadIdleStrategy


def main():
    n_floors = 60
    n_elevators = 3
    max_elevator_capacity = 5
    csv_output = StringIO()
    np.random.seed(1231235)
    passenger_provider = random_uniform_floor_selection_passenger_provider(n=5, p=0.2, n_steps=100, n_floors=n_floors)
    state_persistence = CsvPersistenceStrategy(f=csv_output)
    elevator_system = ElevatorController(
        n_elevators=n_elevators,
        n_floors=n_floors,
        max_elevator_capacity=max_elevator_capacity,
        persistence_strategy=state_persistence,
        assignment_strategy=ExistingStopStrategy(),
        idle_strategy=EqualSpreadIdleStrategy(),
        stop_time=0
    )
    elevator_system.handle_passenger_requests(passenger_request_source=passenger_provider)
    logger.info(csv_output.getvalue())
    elevator_system.print_stats()


if __name__ == "__main__":
    main()
