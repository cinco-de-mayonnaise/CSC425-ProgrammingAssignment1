"""
CSC425 - Artificial Intelligence
Programming Assignment 1
Ahnaf Abdullah - 2130223 - Original Work


"""

from copy import copy, deepcopy
from matplotlib import pyplot
import matplotlib.patches
    

input1 = """7 7
2 2
6 6
32
1 1 
1 2
1 3
1 4
1 5
1 6
1 7
2 1
2 7
3 1
3 3
3 4
3 5
3 6
3 7
4 1
4 7
5 1
5 2 
5 3
5 4
5 6
5 7
6 1
6 7
7 1
7 2
7 3
7 4
7 5
7 6
7 7
"""

input2 = """5 3
1 1
1 3
4
1 2 
2 2
3 2
4 2
"""

# TODO: For some reason, starting position is being interpreted differently by some 
input3 = """21 17
14 4
2 2
194
1 1
1 2
1 3
1 4
1 5
1 6
1 7
1 8
1 9
1 10
1 11
1 12
1 13
1 14
1 15
1 16
1 17
2 1
2 7
2 10
2 17
3 1
3 2
3 3
3 4
3 5
3 7
3 9
3 10
3 11
3 13
3 15
3 17
4 1
4 7
4 9
4 13
4 15
4 17
5 1
5 3
5 4
5 5
5 6
5 7
5 9
5 11
5 13
5 15
5 17
6 1
6 11
6 13
6 15
6 17
7 1
7 2
7 3
7 4
7 5
7 6
7 7
7 9
7 10
7 11
7 13
7 15
7 17
8 1
8 13
8 15
8 17
9 1
9 3
9 4
9 6
9 7
9 8
9 9
9 10
9 11
9 12
9 13
9 15
9 17
10 1
10 4
10 17
11 1
11 2
11 3
11 4
11 5
11 6
11 7
11 8
11 9
11 10
11 11
11 12
11 13
11 14
11 15
11 17
12 1
12 17
13 1
13 3
13 4
13 5
13 6
13 8
13 9
13 10
13 11
13 12
13 13
13 14
13 15
13 17
14 1
14 3
14 6
14 8
14 13
14 17
15 1
15 3
15 4
15 6
15 8
15 9
15 11
15 13
15 15
15 16
15 17
16 1
16 3
16 6
16 9
16 11
16 15
16 17
17 1
17 3
17 5
17 6
17 7
17 9
17 10
17 11
17 12
17 13
17 15
17 17
18 1
18 3
18 6
18 9
18 15
18 17
19 1
19 3
19 4
19 6
19 8
19 9
19 11
19 12
19 13
19 14
19 15
19 17
20 1
20 6
20 17
21 1
21 2
21 3
21 4
21 5
21 6
21 7
21 8
21 9
21 10
21 11
21 12
21 13
21 14
21 15
21 16
21 17
"""

GOAL = 255
FLEA = 128
START = 64
BLOCK = 1
EMPTY = 0

def pprint_maze(maze: list[list[int]], action: tuple[int, int, int] = None, goal: tuple[int, int] = None, path: list[tuple[int, int, int]] = None): 
    def map_mazeelements(i: int):
        if i == GOAL:
            return 'G'
        elif i == FLEA:
            return '•'
        elif i == START:
            return 'S'
        elif i == BLOCK:
            return '█'
        else:
            return ' '

    maze = deepcopy(maze)
    if action is not None:
        maze[action[1]][action[0]] = FLEA
    if goal is not None:
        maze[goal[1]][goal[0]] = GOAL

    # implement drawing the goal and flea positions later
    if path is not None:
        start = path.pop(0)
        maze[start[0]][start[1]] = START
        for ac in path:
            maze[start[0]][start[1]] = FLEA

    for row in maze:
        print(''.join([map_mazeelements(cell) for cell in row]))

def pprint_maze_GUI(maze: list[list[int]], action: tuple[int, int, int] = None, goal: tuple[int, int] = None, path: list[tuple[int, int, int]] = None):    
    from matplotlib.patches import Circle, Rectangle
    maze = deepcopy(maze)

    def draw_circle(x, y, r=0.5, facecolor="blue"):
        pyplot.gca().add_patch(Circle((x+0.5,y+0.5), r, facecolor=facecolor))

    #def draw_rectangle(x_bl, y_bl, ):
        #pyplot.gca().add_patch(Rectangle(x_bl+0.5, y_bl+0.5, ))

    #pyplot.axes().invert_yaxis()
    pyplot.axes().set_aspect('equal')
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.pcolormesh(maze, cmap='Grays')

    if goal is not None:
        draw_circle(goal[0], goal[1], facecolor="green")

    # draw a rectangle connecting (1,1) to (1,2)
    # a = (1, 1)
    # b = (2, 2)
    # pyplot.gca().add_patch(Rectangle((a[0]+0.375, a[1]+0.375), 1.5, 0.25))
    # pyplot.plot(1, 2, "bo")

    if path is not None:
        start = path[0]
        draw_circle(start[0], start[1], r=0.35, facecolor="red")
        for ac in path:
            draw_circle(ac[0], ac[1], r=0.25, facecolor="lightblue")
    
    if action is not None:
        draw_circle(action[0], action[1], r=0.35, facecolor="blue")

    pyplot.gca().invert_yaxis()
    pyplot.show()


def get_possible_actions(maze: list[list[int]], cur_state: tuple[int, int, int]):
    """Returns the set of possible actions that can be taken from the current state. Requires the maze to decide what actions are possible."""
    r, c = len(maze), len(maze[0])
    flea_x, flea_y = cur_state[0:2]
    actions = []

    # Check North
    if flea_y > 0:
        if maze[flea_y-1][flea_x] == BLOCK:
            actions.append("JN")
        else:
            actions.append("N")      
    # West
    if flea_x > 0:
        if maze[flea_y][flea_x-1] == BLOCK:
            actions.append("JW")
        else:
            actions.append("W")  
    # South
    if flea_y < r-1:
        if maze[flea_y+1][flea_x] == BLOCK:
            actions.append("JS")
        else:
            actions.append("S")
    # East
    if flea_x < c-1:
        if maze[flea_y][flea_x+1] == BLOCK:
            actions.append("JE")
        else:
            actions.append("E")
    return actions

def take_action(action: str, cur_state: tuple[int, int, int]):
    """Takes an action based on the current state and returns the new state

    `action` must be a valid action that can be taken from the current state, based on the return values of `get_possible_actions(maze, cur_state)`. 
    No error checking is done inside this function
    """
    flea_x, flea_y = cur_state[0:2]
    cost = cur_state[2]

    if action == "N":
        return (flea_x, flea_y-1, cost+1)
    elif action == "W":
        return (flea_x-1, flea_y, cost+1)
    elif action == "S":
        return (flea_x, flea_y+1, cost+1)
    elif action == "E":
        return (flea_x+1, flea_y, cost+1)
    
    elif action == "JN":
        return (flea_x, flea_y-1, cost+2)
    elif action == "JW":
        return (flea_x-1, flea_y, cost+2)
    elif action == "JS":
        return (flea_x, flea_y+1, cost+2)
    elif action == "JE":
        return (flea_x+1, flea_y, cost+2)
    else:
        raise ValueError("Invalid action")
    
def DFS_BB_v2(maze: list[list[int]], startstate:tuple[int, int, int], goal, h, bound_max=2**32):
    """
    Performs a depth-first search with branch and bound to find the shortest path from the flea to the goal.
    This version abstracts away cost from the state and tracks it seperately, and simplifies the graph to .
    """
    class Graph:
        nodes = dict() # graph: set[State] 

        def __init__(self):
            pass

        def putStateInGraph(self, state: tuple[int, int, int]) -> int:
            h = hash(state)
            if (self.nodes.get(h, None) is not None) and (self.nodes[h] != state):
                raise Exception("OH NO HASH COLLISION!!")
            self.nodes[h] = state
            return h

        def getStateFromID(self, id:int):
            return self.nodes.get(id)
        
        """these are kind of useless"""
        def getCostFromID(self, id:int):
            return self.nodes.get(id)[-1]
        
        def getPosFromID(self, id:int):
            return self.nodes.get(id)[:2]
        
    def isCycle_v1(path: list[int], *args) -> bool:
        visited = set()   # visited is a hash of positions
        for st in path:
            #print(st)
            h = hash(gra.getPosFromID(st))
            if h in visited:
                return True
            else:
                visited.add(h)

        for st in args:   # throw in more states here why not xd
            #print(st)
            h = hash(gra.getPosFromID(st))
            if h in visited:
                return True
            else:
                visited.add(h)
        
        return False
    
    def isCycle_v2(path: list[int], *args) -> bool:
        visited = set()   # visited is a set of positions
        for st in path:
            #print(st)
            st = gra.getPosFromID(st)
            if st in visited:
                return True
            else:
                visited.add(st)

        for st in args:   # throw in more states here why not xd
            #print(st)
            st = gra.getPosFromID(st)
            if st in visited:
                return True
            else:
                visited.add(st)

    global best_path
    global bound 
    global steps 
    global gra
    global max_len_path

    bound = bound_max
    best_path = None
    steps = 0
    max_len_path = 0
    gra = Graph()    

    

    def cbsearch(path: list[int]):
        global bound
        global best_path
        global steps
        global gra
        global max_len_path

        l = len(path)
        if (l > max_len_path):
            print("Path is now currently: ", l)
            max_len_path = l
        cur_node = gra.getStateFromID(path[-1])

        if (cur_node[2] + h(cur_node)) < bound:      # cost(path) + h(cur_node)) < bound, but... cost of the path is just the total cost... that's already part of the state
            if goal(cur_node):
                best_path = copy(path)
                bound = cur_node[2]
                #print(bound)
            else:
                for ac in get_possible_actions(maze, cur_node):
                    if (isCycle_v1(path, gra.putStateInGraph(take_action(ac, cur_node)))):
                        continue            # this action causes it to become a cycle, so avoid this.
                    newpath = copy(path)
                    newpath.append(gra.putStateInGraph(take_action(ac, cur_node)))
                    
                    cbsearch(newpath)
        
        steps+=1

    cbsearch([gra.putStateInGraph(startstate)])
    print(gra.nodes)
    print("Steps: ", steps)

    # best_path is a list of hashes, we need to turn them back into states.
    returnpath = []
    for h in best_path:
        returnpath.append(gra.getStateFromID(h))
    
    return returnpath    # this is guaranteed to be the smallest path through the maze.


def DFS_BB_v1(maze: list[list[int]], startstate:tuple[int, int, int], goal, h, bound_max=2**32):
    """
    Performs a depth-first search with branch and bound to find the shortest path from the flea to the goal.
    This version adds cycle detection and avoids cyclic paths as they are guaranteed to not be a shortest path.
    

    """
    def isCycle(path: list[tuple[int, int, int]], *args) -> bool:
        visited = set()
        for st in path:
            st = st[:2]
            #print(st)
            if st in visited:
                return True
            else:
                visited.add(st)

        for st in args:   # throw in more states here why not xd
            st = st[:2]
            #print(st)
            if st in visited:
                return True
            else:
                visited.add(st)
        
        return False

    global best_path
    global bound 
    global steps 
    global max_len_path
    
    bound = bound_max
    best_path = None
    steps = 0
    max_len_path = 0

    def cbsearch(path: list[tuple[int, int, int]]):
        global bound
        global best_path
        global steps
        global max_len_path

        l = len(path)
        if (l > max_len_path):
            print("Path is now currently: ", l)
            max_len_path = l
        cur_node = path[-1]

        if (cur_node[2] + h(cur_node)) < bound:      # cost(path) + h(cur_node)) < bound, but... cost of the path is just the total cost... that's already part of the state
            if goal(cur_node):
                best_path = deepcopy(path)
                bound = cur_node[2]
                #print(bound)
            else:
                for ac in get_possible_actions(maze, cur_node):
                    if (isCycle(path, take_action(ac, cur_node))):
                        continue            # this action causes it to become a cycle, so avoid this.
                    newpath = deepcopy(path)
                    newpath.append(take_action(ac, cur_node))
                    
                    cbsearch(newpath)
        
        steps+=1

    cbsearch([startstate])

    print("Steps: ", steps)

    return best_path    # this is guaranteed to be the smallest path through the maze.


def DFS_BB(maze: list[list[int]], startstate:tuple[int, int, int], goal, h, bound_max=2**32):
    """
    Performs a depth-first search with branch and bound to find the shortest path from the flea to the goal.
    This is the verbatim version of the algorithm taken from the book, with barely any changes to the algorithm.
    As a result, it is not very efficient. This function serves as the base for other functions with improved performance.
    
    For grading the correctness of the algorithm, please use this function only.

    """
    global best_path
    global bound 
    global steps 
    
    bound = bound_max
    best_path = None
    steps = 0

    def cbsearch(path: list[tuple[int, int, int]]):
        global bound
        global best_path
        global steps
        cur_node = path[-1]
        if (cur_node[2] + h(cur_node)) < bound:      # cost(path) + h(cur_node)) < bound, but... cost of the path is just the total cost... that's already part of the state
            if goal(cur_node):
                best_path = deepcopy(path)
                bound = cur_node[2]
                #print(bound)
            else:
                for ac in get_possible_actions(maze, cur_node):
                    newpath = deepcopy(path)
                    newpath.append(take_action(ac, cur_node))
                    #print(len(path))
                    cbsearch(newpath)
        
        steps+=1

    cbsearch([startstate])

    print("Steps: ", steps)

    return best_path    # this is guaranteed to be the smallest path through the maze.



def create_maze_from_image(path):
    from PIL import Image
    maze_img = Image.open(path)
    r, c = maze_img.size
    print(c, r)
    flea_pos = None
    goal_pos = None
    num_blocks = 0
    blocks = []

    for x in range(r):
        for y in range(c):
            pixel = maze_img.getpixel((x, y))[:3]   # get rgb val
            if (pixel == (0, 0, 0)):  # black, block
                num_blocks += 1
                blocks.append((x, y))
            elif (pixel == (0, 255, 0)):   # green, goal
                goal_pos = (x, y)
            elif (pixel == (255, 0, 0)):   # red, start pos
                flea_pos = (x, y)
            elif (pixel == (255, 255, 255)):   # white, traverseable, pass
                pass
            else:
                print("UNEXPECTED PIXEL: %s at %s" % (pixel, (x, y)))

    returnstr = "{} {}\n".format(r, c)
    returnstr += "{} {}\n".format(flea_pos[0]+1, flea_pos[1]+1)
    returnstr += "{} {}\n".format(goal_pos[0]+1, goal_pos[1]+1)
    returnstr += "{}\n".format(num_blocks)

    for b in blocks:
        returnstr += "{} {}\n".format(b[0]+1, b[1]+1)
    
    #print(returnstr)
    return returnstr




def main():
    path = "./csc425-ai/maze_wierd.png"
    input1 = create_maze_from_image(path)

    #input1 = input2

    inputshorok = [int(k) for k in input1.split()]
    c, r = inputshorok[0], inputshorok[1]           # number of rows and number of columns of the grid
    flea_pos = (inputshorok[2]-1, inputshorok[3]-1)     # initial position of the flea
    goal_pos = (inputshorok[4]-1, inputshorok[5]-1)     # coordinates of the goal location
    num_blocks = inputshorok[6]                     # number of blocked cells

    # pop first 7 numbers from the list
    inputshorok = inputshorok[7:]
    # everything else in the input should now be a coordinate, do offset
    inputshorok = [i-1 for i in inputshorok]
    maze = [[0 for i in range(c)] for j in range(r)]
    try:
        for i in range(num_blocks):
            x, y = inputshorok[0:2]
            inputshorok = inputshorok[2:]
            maze[y][x] = BLOCK
    except Exception as e:
        print("WARNING: Not enough coordinates for the number of blocks specified!")
    
    if len(inputshorok) > 0:
        print("WARNING: More block coordinates provided than number of blocks specified! Ignoring the rest")

    # test get_possible_actions()
    # testcases = [(0, 0, 0), (1, 1, 0), (1, 0, 0), (0, 1, 0)]
    # for t in testcases:
    #     print("%s:%s" % (t, get_possible_actions(maze, t)))

    # test take_action()
    #pprint_maze(maze, action=flea_pos, goal=goal_pos)
    pprint_maze_GUI(maze, action=flea_pos, goal=goal_pos)

    # run the DFS_BranchAndBound algorithm
    def goal(state: tuple[int, int, int]):
        return state[0:2] == goal_pos

    def h(state: tuple[int, int, int]):
        return abs(state[0]-goal_pos[0]) + abs(state[1]-goal_pos[1])    # Manhattan distance heuristic, will definitely be <cost(s) because sometimes an action may cost 2

    shortest_path = DFS_BB_v2(maze, (flea_pos[0], flea_pos[1], 0), goal, h, bound_max=85)
    #print(shortest_path)

    #for ac in shortest_path:
    #    pprint_maze(maze, ac, goal=goal_pos)
    #    print()

    pprint_maze_GUI(maze, goal=goal_pos, path=shortest_path)
    

    """ 
        State: How should we define our state? We only really need to track two things.
            * Current position (flea_pos)
            * Total Cost
        
        Everything else (maze, goal_pos) influences the state space, but doesn't really change, so we can hoist it out of the state. This
        makes our graph implementation small and supple. Thus, our initial state is 

        s_0 = (flea_pos, 0)

        And we start to consider all states that could exist(i.e. we could move to) from our current state. For example, we can move in the 
        4 cardinal directions

        s_0 --N--> s_N (flea_pos.y-1, 1)
            --W--> s_W (flea_pos.x-1, 1)
            --S--> s_S (flea_pos.y+1, 1)
            --E--> s_E (flea_pos.x+1, 1)

        and so on, until we find a path that leads to the exit. suppose s_N,W,W,W,S,W,S which has a cost of 7. Then we start traversing from
        s_0 again until we have evaluated all paths with cost less than 7.  
    """
main()

#create_maze_from_image("bla")

## maze_wierd work started at 4:09 PM