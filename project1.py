# Ethan E. Lopez
# February 17, 2026
# Project 1: Solve the Robot Warehouse Problem Through Search

# References
# Canvas Materials
#   1. 02_search-2_slides.pdf
#   2. Homework 2
#   3. Homework 1
#   4. 01_search-1_slides.pdf
# Other Materials
#   1. Previous Projects (Kruskal’s Algorithm) from CPSC 350
#       - for queue logic checking at the end before project submission (not for original code inspiration or generation)
# AI Platforms
#   1. CHATGPT
#       - you'll see comments throughout this code where the AI was implemented

# README
# this script serves to compute the paths, total estimated costs, nodes expanded, and nodes generated of A* search for a robot in a 5x5 grid

#!CAUTION: NO OTHER IMPORTS ARE ALLOWED!
import math # imports math modules and functions

# BRAINSTORMING

# data structure for the frontier (priority queue logic)
# reached set (lookup table)
# dictionary: {Node: cost} or {state: Node}?
# lists: [Node, Node, Node]

# environment: a 5x5 grid where (1,1) is the bottom-left and (5,5) is the top-right
# agent: a robot starting at (1,1) with the toal of reaching (4,5)
# direction costs:
#   1. cardinal directions (N(Up), S(Down), E(Left), W(Right)): action_cost = 1.00
#   2. diagonal directions (NE(Up-Right), NW(Up-Left), SE(Down-Right), SW(Down-Left)): action_cost = 1.41
# fragile override:
# (moving into fragile cells)
# (3,3): action_cost = 5.0
# (4,2): action_cost = 2.0
# (3,4): action_cost = 3.0

# A* search algorithm:
# Evaluation Function - f(n) = g(n) + h(n)
# Weighted Evaluation Function - f(n) = g(n) + w * h(n)

# sample outputs
# === A* Search (euclidean) ===
# Initial frontier: [None->(1,1)(0.00, 5.00)]

# Step 1
# Expanded: None->(1,1)(0.00, 5.00)
# Frontier: [(1,1)->(2,2)(1.41, 5.02), (1,1)->(1,2)(1.00, 5.24), (1,1)->(2,1)(1.00, 5.47)]

# Step 2
# Expanded: (1,1)->(2,2)(1.41, 5.02)
# Frontier: [(2,2)->(3,3)(2.82, 5.00), (1,1)->(1,2)(1.00, 5.24), (1,1)->(2,1)(1.00, 5.47), (2,2)->(3,2)(2.41, 5.57), (2,2)->(1,3)(2.82, 6.43),
# (2,2)->(3,1)(2.82, 6.94), (2,2)->(3,3)(6.41, 8.65)]

# Final Solution
# Goal reached.
# Path: [(1,1), (2,2), (3,3), (4,4), (4,5)]
# Total estimated cost (f=g+h) = some number
# Nodes expanded: some number
# Nodes generated: some number
# is nodes generated how many nodes were put into the frontier?

class Node: # defines node class
    def __init__(self, state, parent=None, action=None, g=0.0, h=0.0, w=1.0):
    # nodes include a state, parent, action, and values for the evaluation function
        self.state = state     # (x, y)
        self.parent = parent   # Parent Node object
        self.action = action   # e.g., "U", "UR"
        self.g = float(g)      # Path-cost from start to this node
        self.h = float(h)      # Heuristic estimate to goal
        self.w = float(w)      # When w>1.0, A* -> Weighted A*
        self.f = self.g + self.w * self.h # total estimated cost
        # the total estimated cost is the path cost plus the weighted heuristic

def get_manhattan_distance(pos, goal):
# function for manhattan_distance
# pos is the node's current state and the goal is the node's target state
    m_distance = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1]) # calculate manhattan distance
    # manhattan_distance = |x1-x2| + |y1-y2|
    # manhattan distance is the sum of:
        # 1. the absolute difference in x's between the current position and the goal
        # 2. the absolute difference in y's between the current position and the goal
    # since states are stored as sets, these values need to be called using indexing   
    return m_distance # return manhattan distance

def get_euclidean_distance(pos, goal):
# function for manhattan_distance
# pos is the node's current state and the goal is the node's target state
    e_distance = math.sqrt((pos[0] - goal[0])**2 + (pos[1] - goal[1])**2) # calculate euclidean distance
    # euclidean_distance = ((x1-x2)^2 + (y1-y2)^2)^(1/2)
    # the euclidean distance is the sum of:
        # 1. the squared difference in x's between the current position and the goal
        # 2. the squared difference in y's between the current position and the goal
        # 3. the square root of #1 and #2 added together
    return e_distance # return euclidean distance

def get_path_cost(node, action_cost, next_state):
# a function for calculating fragile override path-cost cases
# these would involve coordinates (3,3), (4,2), and (3,4)
# takes in 3 parameters:
    # 1. node: the parent node / the node being expanded
    # 2. action_cost: the cost of the action taken to get to the next state
    # 3. next_state: the coordinates of the next state (x,y)
    if (next_state == (3,3)):
    # if the next state is in the fire zone (3,3)
        return node.g + 5.00 # this is an added cost of 5
    elif (next_state == (4,2)):
    # if the next state is the first water zone (4,2)
        return node.g + 2.00 # this is an added cost of 2
    elif (next_state == (3,4)):
    # if the next state is the second water zone (3,4)
        return node.g + 3.00 # this is an added cost of 3
    else:
    # otherwise the next path cost is simply adding the standard action costs
        return node.g + action_cost
    

def get_children(node, heuristic_type, weight, goal):
# a function for retrieving child nodes
# this takes in 4 parameters:
    # 1. node: the parent node / the node being expanded
    # 2. heuristic_type: manhattan or euclidean
    # 3. weight: the heuristic weight in the evaluation function
    # 4. goal: the coordinates of the goal state (x,y)
    
    node_state = node.state # get the node's current state coordinates
    x = node_state[0] # get x coordinate from the node's state
    y = node_state[1] # get y coordinate from the node's state

    n = Node(state=(x, y+1), parent=node, action="U", g=0.0, h=0.0, w=weight) # north node (up / U)
    s = Node(state=(x, y-1), parent=node, action="D", g=0.0, h=0.0, w=weight) # south node (down / D)
    e = Node(state=(x+1, y), parent=node, action="R", g=0.0, h=0.0, w=weight) # east node (right / R)
    w = Node(state=(x-1, y), parent=node, action="L", g=0.0, h=0.0, w=weight) # west node (left / L)
    ne = Node(state=(x+1, y+1), parent=node, action="UR", g=0.0, h=0.0, w=weight) # northeast node (up-right / UR)
    nw = Node(state=(x-1, y+1), parent=node, action="UL", g=0.0, h=0.0, w=weight) # northwest node (up-left / UL)
    se = Node(state=(x+1, y-1), parent=node, action="DR", g=0.0, h=0.0, w=weight) # southeast node (down-right / DR)
    sw = Node(state=(x-1, y-1), parent=node, action="DL", g=0.0, h=0.0, w=weight) # southwest node (down-left / DL)
    og_children = [[n, s, e, w], [ne, nw, se, sw]] # create a list of child nodes for original cardinal and diagonal directions
    # this is defined as a 2d list to split cardinal and diagonal directions

    # print statement for checking generated children
    # for child_list in og_children: # for cardinal and diagonal directions
    #     for child in child_list:
    #         print(f"Generated: {node.state}->{child.state}") # print the generated child node information

    children = [[], []] # initialize a new list for valid child nodes in cardinal and diagonal directions
    
    # now validate if the child nodes are in the 5x5 grid
    index = -1 # initialize an index for adding valid child nodes to the correct list
    for child_list in og_children: # for cardinal and diagonal directions
        index += 1 # increment this index to move to the next list (switching between cardinal and diagonal)
        for child in child_list: # for each potential child in the list
            if (child.state[0] > 0 and child.state[0] < 6) and (child.state[1] > 0 and child.state[1] < 6): # if the x and y coordinates are within the 5x5 bounds
                children[index].append(child) # add the child node to the list of valid child nodes for the correct type of direction
    
    # next calculate the path cost (g), heuristic (h), and total estimated cost (f) for each valid child node
    action = 1.00 # assign action as 1 for cardinal directions
    for child in children[0]: # for each child in the cardinal list
        child.g = get_path_cost(node, action, child.state) # calculate the path cost for this child
        if heuristic_type == "euclidean": # if the heuristic type is euclidean
            child.h = get_euclidean_distance(child.state, goal) # calculate the euclidean heuristic
        else: # otherwise the heuristic is assigned to manhattan
            child.h = get_manhattan_distance(child.state, goal) # calculate the manhattan heuristic
        child.f = child.g + child.w * child.h # update the child's f value based on the new g and h values

        # print statement for logic
        # print(f"Valid child: {node.state}->{child.state}({child.g:.2f}, {child.f:.2f})") # print the valid child node information for checking

    action = 1.41 # change action to 1.41 for diagonal directions
    for child in children[1]: # for each child in the diagonal list
        child.g = get_path_cost(node, action, child.state) # calculate the path cost for this child
        if heuristic_type == "euclidean": # if the heuristic type is euclidean
            child.h = get_euclidean_distance(child.state, goal) # calculate the euclidean heuristic
        else: # otherwise the heuristic is assigned to manhattan
            child.h = get_manhattan_distance(child.state, goal) # calculate the manhattan heuristic
        child.f = child.g + child.w * child.h # update the child's f value based on the new g and h values

        # print statement for logic
        # print(f"Valid child: {node.state}->{child.state}({child.g:.2f}, {child.f:.2f})") # print the valid child node information for checking
        
    return children # return the list containing all valid child nodes

def get_path(goal_node):
# a function for getting the final path of the solution
# works by backtracking through parent nodes from the goal state
# goal_node contains the goal state and information from all previous nodes in the path
    path = [] # initialize a list for the final path
    path.append(goal_node.state) # add the goal node's state to the path list
    node = goal_node # assign node as the goal node
    while node.parent is not None: # while each node has a parent that is not None (we haven't reached the starting node yet)
        node = node.parent # get the parent of the current node
        path.append(node.state) # add the parent node's state to the path list

    path.reverse() # reverse the path list to get the correct order from start to goal
    return path # return the path from start to goal nodes as a list of coordinates

def get_frontier(children, frontier, expanded):
# a function for adding new child nodes and organizing the frontier
# children is the list containing all valid child nodes
# frontier is the current frontier as a list of nodes
# expanded is the set of expanded node states so far
    for child_list in children: # for cardinal and diagonal directions
        for child in child_list: # for each child node in the list

            # CHATGPT ASSISTANCE
            # for simpler formatting and checking logic
            # prompt: "I have a frontier as a list with node objects containing states, path-costs, heuristics, and total estimated costs."
            # "How can I check if a new child is already in the frontier and compare its cost according to A* search logic in python?"
            # output:
            # 1. gave me advice to modify my set (expanded) to ensure no states were repeated and to add on visiting states
            # 2. advised using an add or tracker variable to keep track of nodes that should and shouldn't be added to the frontier
            # 3. suggested comparing costs using the child's path-cost (g) rather than f cost due to the unpredictability of heuristics
            if child.state in expanded: # if the child node's state is already in the reached set, we skip it
                continue
            
            add = True # initialize to check if the child should be added

            for node in frontier: # for each node in the frontier
                if node.state == child.state: # if there is already a node that matches the child in the frontier
                    if child.g >= node.g: # if the child's path cost is worse than the node
                        add = False # do not add the child
                    break # since we found an identical node, break out of the loop

            if add: # if adding the node is valid since it is unique, not reached, or has a cheaper cost
                frontier.append(child) # add it to the frontier list

    # CHATGPT ASSISTANCE: For correct syntax and calculation
    frontier.sort(key=lambda n: n.g + n.w * n.h) # sort the frontier by f value (cost)
    return frontier # return the updated frontier

def a_star_search(start_pos, goal_pos, heuristic_type="manhattan", weight = 1.0):
# function for A* search
# A* search requires starting coordinates (start_pos), goal coordinates (goal_pos), a heuristic type (manhattan or euclidean), and a weight
    frontier = [] # initialize the frontier as an empty list
    # this will be printed in the format (parent location)->(current location)(g, f)
    
    # CHATGPT ASSISTANCE
    # reference details in get_frontier() function
    expanded = set() # initialize the reached set as an empty set for storing visited states

    generated = set() # an empty set for keeping track of generated states
    step = 0 # initialize step counter for printing
    print() # newline for neatness
    print(f"=== A* Search ({heuristic_type}) ===") # print the heuristic type being used
    if heuristic_type == "euclidean": # if the heuristic type is euclidean
        heuristic = get_euclidean_distance(start_pos, goal_pos) # get the euclidean heuristic       
    else: # otherwise get the manhattan heuristic
        heuristic = get_manhattan_distance(start_pos, goal_pos)
    
    current = Node(state=start_pos, parent=None, action=None, g=0.0, h=heuristic, w=weight) # create starting node
    frontier.append(current) # add the starting node to the frontier with its f value as the cost
    print(f"Initial frontier: [None->{current.state}({current.g:.2f}, {current.f:.2f})]") # print the initial frontier
    while True: # while A* search is still running
        current = frontier.pop(0) # assign the current node to that node
        if current.state == goal_pos:
            # if the current node's state is the goal state, we have reached the goal
            break # end the loop
        expanded.add(current.state) # add the current node's state to the reached set
        step += 1 # increment step counter
        print() # newline for neatness
        print(f"Step {step}") # print the current step number
        if current.parent is None: # if we are at the starting node, print this format since parent is None
            print(f"Expanded: None->{current.state}({current.g:.2f}, {current.f:.2f})")
        else: # otherwise print this for the current node being expanded
            print(f"Expanded: {current.parent.state}->{current.state}({current.g:.2f}, {current.f:.2f})")
        # determine the expanded node's children
        children = get_children(current, heuristic_type, weight, goal_pos) # get the current node's children in a list
        for child_list in children: # for nodes in the children
            for child in child_list: # for each valid child existing
                generated.add(child.state) # add their state to the genderated set
            # this would be inclusive of the goal state generated at the end (4.5) and the starting state (1,1) as these are both 'valid' children for various nodes
        # organize costs in the frontier
        frontier = get_frontier(children, frontier, expanded) # modify the frontier from valid children by f values
        print("Frontier: [", end="") # print the frontier in the correct format
        for node in frontier: # for all nodes in the frontier          
            print(f"{node.parent.state}->{node.state}({node.g:.2f}, {node.f:.2f})", end=", ") # print its information
        print("]")
        # the node with the lowest cost in the frontier will be expanded next
    
    print() # newline for neatness
    print("Goal reached.") # print that we have reached the goal
    path = get_path(current) # get the path from start to goal using backtracking through the parent nodes
    # now we need to backtrack to get the path from start to goal
    print(f"Path: {path}") # print the path
    print(f"Total estimated cost (f=g+h) = {current.f:.2f}") # print the total estimated cost to reach the goal
    print(f"Nodes expanded: {step}") # print the number of nodes expanded (steps taken)
    print(f"Nodes generated: {len(generated)-1}") # print the number of nodes generated
    # this is all unique states generated from valid children nodes (even those not added to the frontier) 
    # minus 1 because we don't want to count the starting state generated prior
    # we do count the goal state however as this is a generated node by expansion

    # # print statement for checking generated states
    # print(generated)

    print() # newline for neatness

# Test Case (run twice and compare)
if __name__ == "__main__":
    start = (1, 1) # beginning state in the grid
    goal = (4, 5) # goal state in the grid

    # modify here for cost task 2
    a_star_search(start, goal, heuristic_type="manhattan", weight=1.0) # a* search using manhattan distance
    a_star_search(start, goal, heuristic_type="euclidean", weight=1.0) # a* search using euclidean distance