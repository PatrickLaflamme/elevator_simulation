import json
from io import StringIO

from elevator_controller.elevator_system import ElevatorSystem
from elevator_controller.log import logger
from elevator_controller.passenger_providers import random_passenger_provider
from elevator_controller.strategies.elevator_system_persistence import CsvPersistenceStrategy


def main():
    n_floors = 10
    max_elevator_capacity = 5
    csv_output = StringIO()
    passenger_provider = random_passenger_provider(n=5, p=0.05, n_steps=100, n_floors=n_floors)
    state_persistence = CsvPersistenceStrategy(f=csv_output)
    elevator_system = ElevatorSystem(
        n_elevators=3,
        n_floors=n_floors,
        max_elevator_capacity=max_elevator_capacity,
        persistence_strategy=state_persistence
    )
    elevator_system.handle_passenger_requests(passenger_request_source=passenger_provider)
    print(csv_output.getvalue())
    print(json.dumps(elevator_system.get_stats(), indent=2))


if __name__ == "__main__":
    main()
