# METRO NETWORK ROUTE PLANNER
- This project is a Python application that determines the fastest route with the fewest transfers in a metro network.

## TECHNOLOGIES AND LIBRARIES USED

- The project is developed using Python. The following libraries have been used:
- **heapq** Used for Priority Queue operations (utilized in the A* algorithm).
- **collections.defaultdict** Used to create default lists (for storing metro stations).
- **collections.deque** Enables efficient execution of the BFS algorithm using a double-ended queue (deque) data structure.
- **typing** Used to specify function parameter and return types.

## WORKING PRINCIPLES OF THE ALGORITHMS

### BFS (BREADTH-FIRST SEARCH) – FOR MINIMUM TRANSFERS
- The BFS algorithm is used to reach the destination with the fewest transfers in the metro network.

***How Does It Work?***

- The starting station is first added to the queue.
- Stations are visited level by level in an expanding manner.
- The first reached target station provides the path with the fewest transfers.

***Why Did We Use BFS?***

- BFS is ideal for finding the shortest path in a graph without edge weights.
- It is well-suited for minimizing the number of transfers in a metro network.

### A ALGORITHM
- The A* algorithm is used to reach the destination in the shortest time.

***How Does It Work?***

- Uses the formula: f(n) = g(n) + h(n)
- g(n): Actual travel time from the start to station n.
- h(n): Estimated time from station n to the destination (heuristic).

***Heuristic Function:***

- Same line: (Station index difference) × (average line travel time)
- Different lines: Nearest transfer point + estimated target line time.

### WHY THESE ALGORITHMS?
- BFS: Simple and guarantees the minimum number of transfers.
- A*: Finds the optimal route + fast execution (optimized with heuristics).

### EXAMPLE USAGE AND TEST RESULTS
- You can use the following test scenarios to see how the code works:

#### Example Test Scenarios
scenarios = [

    ("M1", "K4", "From AŞTİ to OSB"),
    
    ("T1", "T4", "From Batıkent to Keçiören"),
    
    ("T4", "M1", "From Keçiören to AŞTİ"),
    
]

##### Minimum transfers:
- AŞTİ → Kızılay (Blue) → Kızılay (Red) → Ulus → Demetevler → OSB

##### Fastest route (19 minutes):
- AŞTİ → Kızılay (Blue) → Kızılay (Red) → Ulus → Demetevler → OSB

##### Minimum transfers:
- Batıkent → Demetevler → Gar → Keçiören

##### Fastest route (21 minutes):
- Batıkent → Demetevler → Gar (Orange) → Gar (Blue) → Keçiören

## IDEAS FOR FURTHER DEVELOPMENT

**MORE ADVANCED HEURISTIC FUNCTION**
- Currently, our heuristic function returns a fixed value. We can improve it by calculating actual distances using geographical coordinates or the physical distance between stations.

**METRO MAP VISUALIZATION**
- A graphical user interface (GUI) or map visualization can be added to make the results more intuitive and easier to understand.

**REAL-TIME DATA INTEGRATION**
- Integrate real-world data from Istanbul Metro or other city transit systems for more accurate and dynamic route planning.

**MULTI-DESTINATION SUPPORT**
- Features like “Nearest Hospital” or “Least Crowded Route” can be added for enhanced user experience.
