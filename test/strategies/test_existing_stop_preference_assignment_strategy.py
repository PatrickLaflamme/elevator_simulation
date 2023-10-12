from elevator_system_design.model.elevator import Elevator
from elevator_system_design.model.passenger import Passenger
from elevator_system_design.strategies.assignment import ExistingStopPreferenceStrategy


def test_existing_stop_preference_assignment_strategy_prefers_elevator_already_stopping_at_source_and_dest():
    elevators = [Elevator(num_floors=10, max_capacity=10) for _ in range(3)]
    # first elevator is going to stop at floors 3 and 6
    elevators[0].assign(Passenger(id="", source_floor=4, destination_floor=6, request_time=0))
    # second elevator is going to stop at floors 4 and 7
    elevators[1].assign(Passenger(id="", source_floor=4, destination_floor=7, request_time=0))
    # third elevator is going to stop at floors 5 and 7
    elevators[2].assign(Passenger(id="", source_floor=5, destination_floor=7, request_time=0))

    assignment = ExistingStopPreferenceStrategy().assign_elevator(
        passenger=Passenger(id="", source_floor=4, destination_floor=7, request_time=1),
        elevators=elevators
    )

    # Since elevator at index 1 is already stopping at floors 4 and 7, it's selected.
    assert assignment == 1


def test_existing_stop_preference_assignment_strategy_prefers_elevator_already_stopping_at_source_over_none():
    elevators = [Elevator(num_floors=10, max_capacity=10) for _ in range(3)]
    # first elevator is going to stop at floors 3 and 6
    elevators[0].assign(Passenger(id="", source_floor=4, destination_floor=6, request_time=0))
    # second elevator is going to stop at floors 4 and 7
    elevators[1].assign(Passenger(id="", source_floor=4, destination_floor=7, request_time=0))
    # third elevator is going to stop at floors 5 and 7
    elevators[2].assign(Passenger(id="", source_floor=5, destination_floor=7, request_time=0))

    assignment = ExistingStopPreferenceStrategy().assign_elevator(
        passenger=Passenger(id="", source_floor=5, destination_floor=9, request_time=1),
        elevators=elevators
    )

    # Since elevator at index 2 is already stopping at floor 5, it's selected.
    assert assignment == 2


def test_existing_stop_preference_assignment_strategy_selects_elevator_able_to_pick_up_soonest():
    elevators = [Elevator(num_floors=10, max_capacity=10) for _ in range(3)]
    # first elevator is going to stop at floors 3 and 6
    elevators[0].assign(Passenger(id="", source_floor=4, destination_floor=6, request_time=0))
    # second elevator is going to stop at floors 4 and 7
    elevators[1].assign(Passenger(id="", source_floor=4, destination_floor=7, request_time=0))
    # third elevator is going to stop at floors 5 and 7
    elevators[2].assign(Passenger(id="", source_floor=5, destination_floor=7, request_time=0))

    assignment = ExistingStopPreferenceStrategy().assign_elevator(
        passenger=Passenger(id="", source_floor=3, destination_floor=1, request_time=1),
        elevators=elevators
    )

    # Since no elevator shares a floor with the passenger, the one at index 0 needs to go up the least, and so will
    # be able to sweep downward and pick up the passenger first.
    assert assignment == 0
