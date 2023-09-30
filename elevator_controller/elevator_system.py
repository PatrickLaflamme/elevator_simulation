from typing import List, Set

from pydantic import BaseModel

from elevator_controller.model.elevator import Elevator
from elevator_controller.model.passenger import Passenger
from elevator_controller.model.system_summary import SystemSummary
from elevator_controller.strategies.assignment import ElevatorAssignmentStrategy
from elevator_controller.strategies.elevator_system_persistence import ElevatorSystemPersistenceStrategy
from elevator_controller.strategies.idle import ElevatorIdleStrategy


class ElevatorSystem(BaseModel):
    elevators: List[Elevator]
    assignment_strategy: ElevatorAssignmentStrategy
    idle_strategy: ElevatorIdleStrategy
    state_persistence_strategy: ElevatorSystemPersistenceStrategy
    num_floors: int
    wait_time_summary: SystemSummary = SystemSummary()
    total_time_summary: SystemSummary = SystemSummary()
    pending_passengers: Set[Passenger] = set()
