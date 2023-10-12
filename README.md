# Elevator Simulation System

A simple elevator simulation system built to model the behavior of multiple elevators serving multiple floors in a building. It takes into account various passenger requests with differing start and end floors, and optimizes elevator movement based on chosen strategies.

## Getting started

This tool was implemented and tested using python 3.9.

An example of the tool has been provided in `example.py`. To run it, navigate to the root of the project and 
execute the following:

```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=elevator_system_design python example.py
```

## Assumptions and Decisions

This solution is intended to be flexible, but in order to build something simple, some basic assumptions were made:

* Capacity limits and measured in `persons` not in some other unit like `mass`
* Embarking and Disembarking the elevator takes a fixed (but configurable) amount of time, regardless of the number of
passengers who may be embarking or disembarking at the floor.
* All elevators move at the same speed, regardless of load.
* All elevators have the same `max_capacity` and can serve all floors.
* Floors are 1-indexed, and no basements exist (or floor 1 corresponds to the lowest floor, regardless of whether that 
floor is the first floor or a basement level.)
* The ideal configuration of the following may vary depending on context and so are configurable:
  * How passenger requests are sourced for the controller
  * How elevator state is recorded
  * How passengers are assigned to elevators
  * Where idle elevators sit until called

## Key System Components

### Passenger

A `Passenger` instance encapsulates details about an individual using the elevator, including the source and destination
floors. The definition for the passenger class can be found [here](elevator_system_design/model/passenger.py)

### Elevator

An `Elevator` instance keeps track of its current state, including its present floor and its 
target floors. It manages passenger pickup requests and ensures it stops at appropriate floors to embark or disembark 
passengers. The definition for the elevator class can be found [here](elevator_system_design/model/elevator.py)

### ElevatorController

The `ElevatorController` orchestrates the movements of all elevators and efficiently assigns passengers to elevators, 
considering factors like direction, proximity, and load. The definition for the elevator controller can be found 
[here](elevator_system_design/elevator_controller.py)

## Decomposing the problem

The elevator problem consists of a collection of individual problems whose solutions can be tuned independently:
- **Managing Elevator Movement**: Tracking where each elevator should be moving at each time step.
- **Elevator Assignment**: How requests from passengers are routed to specific elevators can impact wait and travel times.
- **Idle Behavior**: Where an idle elevator is placed can impact passenger wait times.

### Managing Elevator Movement

The problem of managing elevator movement given a set of assigned passengers requires some thought. The naive way to 
do it would be to go to the source floor of the first passenger to pick them up, then drop them off at their destination
floor, followed by going to the source floor of the second passenger, and so on. This solution is extremely inefficient 
because in most cases, the elevator will go up and down, one passenger at a time. This results in a lot of movement
where the elevator is moving between floors without any passengers. 

To avoid this, we can employ a SCAN algorithm to sweep upward, picking up any upward bound passengers assigned to the 
elevator that we may we pass along the way.Then, once all upward bound passengers have disembarked, we can move to the
highest source floor among the passengers who are downward bound and move downward, repeating the process. 

The SCAN algorithm can be implemented with 3 heaps. In the event the elevator is moving up, those 3 heaps would be: 
1.  a min-heap of all floors (pickup and drop-off) of upward bound passengers above the elevator's current floor;
2.  a max-heap of all floors of downward bound passengers; and
3.  a min-heap of all floors of upward bound passengers who are below the elevator's current floor. 

The elevator proceeds in the current direction (here, it's upward) until all floors in heap (1) have been 
visited. When heap (1) is empty, we move up to the first element in (2) if head (2) starts above the current floor, and 
rotate the heaps, changing directions to sweep downward. Rotating the heaps consists of moving heap (2) to position (1), 
heap (3) to position (2) and having and empty heap in position (3). Now, the elevator performs a downward sweep with the 
following heaps:
1. a max-heap of all floors (pickup and drop-off) of downward bound passengers below the elevator's current floor;
2. a min-heap of all floors of upward bound passengers; and
3. a max-heap of all floors of downward bound passengers who are above the elevator's current floor.

### Elevator Assignment

Elevator assignment is a problem whose optimal solution is heavily dependent on the usage patterns of passengers. For
this reason, the `Strategy` design pattern has been employed to support any number of strategies depending on the 
context.

### Idle Behavior

Idle elevator behavior is also a problem whose optimal solution is dependent on passenger usage patterns. The `Strategy`
design pattern was employed here as well. 

## Strategies 

The last two components of the problem are components whose solutions might vary depending on the details of a specific
application of the solution. For example, if one has access to historical statistics of usage, one might want to incorporate
that into the `Elevator Assignment` algorithm. We don't want to make it required, though, for someone to have such statistics.
To allow for flexibility and extensibility of this solution, we employ the `Strategy` design pattern. 

The system supports extensible strategies for:
- **Elevator Assignment**: Determines which elevator is assigned to cater to a passenger's request. The interface is defined [here](elevator_system_design/strategies/assignment.py)
- **Idle Behavior**: Specifies the elevator’s actions when no requests are pending. The interface for this strategy is defined [here](elevator_system_design/strategies/idle.py)

### Elevator Assignment Strategies

Elevator assignment strategies can vary in sophistication. Here are a few that have been implemented. All these strategies
are implemented [here](elevator_system_design/strategies/assignment.py)

#### Closest Empty Elevator Strategy

This strategy is extremely naive and selects the closest empty elevator to assign a passenger. If no elevator is 
available, the strategy will attempt to re-assign an elevator at the next time step. This is the least optimal solution.

#### Directional Match Elevator Strategy

This strategy is slightly more sophisticated and assigns passengers to elevators which are heading in the same direction
as the passenger which haven't yet passed the passenger. If no elevator meets these conditions, then the strategy attempts
to re-assign an elevator at the next time step. 

#### Existing Stop Strategy

This strategy considers a passenger's source and destination floors, attempting to assign the passenger to an elevator
that is already stopping there. If no such elevator exists, it will use the `Directional Match Elevator Strategy`
described above. This strategy is best for conditions in which the elevator stops for some period of time each time a 
passenger embarks or disembarks as it attempts to minimize the number of unique stops. 

### Idle Behavior Strategies

The idle behaviour is the most sensitive component of the problem with respect to usage patterns. Positioning elevators
such that they're ready and waiting for passengers can cut the mean wait time almost to zero. 

#### Middle Floor Idle Strategy

This simple strategy puts all elevators on the middle floor. It is the least optimal of all strategies, but may convey
benefits in the event that the use-case involves minimal unnecessary elevator movement (such as conserving energy).

#### Equal Spread Idle Strategy

This strategy spreads all elevators equally across the floors, such that the distance between one idle elevator and any
given floor is minimized.

#### Usage Pattern Weighted Spread Idle Strategy

This strategy spreads elevators across floors, weighting each floor based on historical stats on how often that floor 
is a source floor for passengers.

## Specifying passenger requests

There are a multitude of ways to specify passenger requests. 

### Source passenger requests from a CSV file

You can specify an existing set of passenger requests from a CSV file using the `csv_passenger_provider` which takes
a file object of an open csv file as input. You can find the source code [here](elevator_system_design/passenger_providers.py).

### Randomly generate passenger requests where any source/destination floor is equally likely

If you don't have an existing CSV file handy, you can randomly generate passenger requests using 
the `random_uniform_floor_selection_passenger_provider`. This will randomly generate passenger requests at each time 
step with source and destination floors that are randomly sampled from a uniform distribution covering all possible 
floors. Generated passengers whose source and destination floors are the same are ignored. You can find the source code
[here](elevator_system_design/passenger_providers.py).

### Randomly generate passenger requests where source/destination floors follow a statistical curve

Finally, if you want a random set of passengers who follow a general pattern to better simulate real-world 
conditions, you can use the `random_gaussian_floor_selection_passenger_provider`. This will randomly generate passenger
requests at each time step whose source and destination floors are randomly sampled from gaussian distributions. 
The gaussian distributions are defined separately for source and destination floors. You can find the source code 
[here](elevator_system_design/passenger_providers.py).

## Statistics

The system keeps track of key metrics, such as min, max, and mean wait times, and total time for passengers, providing 
insights into efficiency and areas for improvement. It also tracks the location of each elevator at each timestep. 

### Key Metrics

Key metrics are tracked throughout the simulation. These metrics are tracked using the `SystemSummary` class defined 
[here](elevator_system_design/model/system_summary.py). A summary is retained for both `wait time` and `total time` experienced
by passengers throughout the simulation. A dictionary of the summary stats can be obtained by invoke the `get_stats` function
within the `ElevatorController` class. Alternatively, a markdown table containing the summary can be printed using the 
`print_stats` function on the same class.

### Elevator location persistence

The location of each elevator can be recorded at each timestep and saved to csv. Simply specify the 
`state_persistence_strategy` on the `ElevatorController` class at instantiation with the `CsvPersistenceStrategy` defined
[here](elevator_system_design/strategies/elevator_controller_persistence.py). Custom persistence strategies such as 
persistence to a database can be achieved by implementing the `ElevatorPersistenceStrategy` protocol.
