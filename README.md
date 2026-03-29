# Intelligent Warehouse Navigation Via Search Algorithms
### Robot Pathfinding With A* Search

- A Python script reflecting the processes and implementation behind the A* search algorithm, ran to determine the optimal path for a robot to travel in a weighted 5 x 5 grid representing a warehouse.

## Author Info

- Full Name: Ethan E. Lopez
- Chapman Email: etlopez@chapman.edu

## Usage

To run this program, use the following command in your command window:

python project1.py

If you want to use another heuristic, simply change the call to the following in your script:

a_star_search("manhattan")
# or
a_star_search("euclidean")

## Input Format

The program does not need any external input files. All parameters of the environment are hardcoded as follows:

1. Grid Size: 5 × 5
2. Start State: (1, 1)
3. Goal State: (4, 5)
4. Movement Costs

- Cardinal moves (N, S, E, W): 1.0
- Diagonal moves: 1.41

5. Special Terrain (Overrides Movement Cost)

- (3, 3): cost = 5
- (4, 2): cost = 2
- (3, 4): cost = 3

## Output

The program prints:

1. Search Trace
2. Expanded node at each step
3. Current frontier state

Format:

Parent_State -> Current_State (g=path_cost, f=total_cost)

Final Results
- Optimal path (sequence of coordinates)
- Total path cost
- Total number of nodes generated

## Implementation Details

### Algorithm
----------

Implements the A* search algorithm with the following heuristic function:

f(n) = g(n) + h(n)

Supports two heuristics:

1. Manhattan Distance
2. Euclidean Distance

### Data Structures
-------------

1. Frontier (Priority Queue)
- Implemented manually using Python lists
- Nodes are kept sorted by lowest f(n)
2. Reached Set
- Implemented using a dictionary
- Stores states that have been reached and their best known cost

## Key Features
- Weighted Grid with terrain overrides
- Diagonal and Cardinal movement
- Heuristic comparison
- Step-by-step trace of search process

## Report

- View detailed results and findings here:

https://docs.google.com/document/d/1IzdWcC34rbnH5E_56keG9onPOK7AgVlNLndYHyrxwhA/edit?usp=sharing

