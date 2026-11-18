
import heapq


GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)   # where 0 = blank tile

def goal_positions():
    """Pre-compute {tile: (row, col)} for Manhattan distance."""
    pos = {}
    for i, val in enumerate(GOAL):
        pos[val] = (i // 3, i % 3)
    return pos

GOAL_POS = goal_positions()

def manhattan(state):
    """Sum of Manhattan distances of each tile from its goal position."""
    dist = 0
    for i, val in enumerate(state):
        if val == 0:
            continue
        gr, gc = GOAL_POS[val]
        cr, cc = i // 3, i % 3
        dist += abs(gr - cr) + abs(gc - cc)
    return dist

def misplaced_tiles(state):
    """Number of tiles not in their goal position (alternative heuristic)."""
    return sum(1 for i, val in enumerate(state) if val != 0 and val != GOAL[i])


MOVES = {
    # blank_index: [(direction_name, new_blank_index), ...]
}

def get_moves(blank_idx):
    """Return valid (move_name, new_blank_idx) pairs for the blank position."""
    row, col = blank_idx // 3, blank_idx % 3
    moves = []
    if row > 0: moves.append(("UP",    blank_idx - 3))
    if row < 2: moves.append(("DOWN",  blank_idx + 3))
    if col > 0: moves.append(("LEFT",  blank_idx - 1))
    if col < 2: moves.append(("RIGHT", blank_idx + 1))
    return moves

def apply_move(state, blank_idx, new_blank_idx):
    """Swap blank with target tile and return new state tuple."""
    lst = list(state)
    lst[blank_idx], lst[new_blank_idx] = lst[new_blank_idx], lst[blank_idx]
    return tuple(lst)


def astar(start, heuristic=manhattan):
    """
    A* search for the 8-puzzle.

    Returns:
        path  : list of (move_name, state) from start to goal
        stats : dict with nodes_explored, nodes_generated, max_frontier
    """
    start = tuple(start)
    if start == GOAL:
        return [(None, start)], {"nodes_explored": 0, "nodes_generated": 1, "max_frontier": 1}

    # Priority queue entries: (f, g, state, blank_idx, parent_ref)
    # We store the full path as a list to reconstruct easily.
    h0 = heuristic(start)
    blank0 = start.index(0)

    # Each entry: (f, g, state, blank_idx, path_so_far)
    # path_so_far is a list of (move_name, state)
    frontier = []
    heapq.heappush(frontier, (h0, 0, start, blank0, [(None, start)]))

    visited = set()
    nodes_explored = 0
    nodes_generated = 1
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        f, g, state, blank_idx, path = heapq.heappop(frontier)

        if state in visited:
            continue
        visited.add(state)
        nodes_explored += 1

        if state == GOAL:
            return path, {
                "nodes_explored": nodes_explored,
                "nodes_generated": nodes_generated,
                "max_frontier": max_frontier
            }

        for move_name, new_blank in get_moves(blank_idx):
            new_state = apply_move(state, blank_idx, new_blank)
            if new_state not in visited:
                new_g = g + 1
                new_h = heuristic(new_state)
                new_f = new_g + new_h
                nodes_generated += 1
                heapq.heappush(
                    frontier,
                    (new_f, new_g, new_state, new_blank, path + [(move_name, new_state)])
                )

    return None, {"nodes_explored": nodes_explored,
                  "nodes_generated": nodes_generated,
                  "max_frontier": max_frontier}


def print_board(state):
    """Pretty-print a board state."""
    for i in range(3):
        row = state[i*3 : i*3+3]
        print("\t" + "  ".join("_" if v == 0 else str(v) for v in row))

def print_solution(path, stats):
    """Print the full step-by-step solution."""
    print("  A* SOLUTION PATH")
    print("-"*50)
    for step, (move, state) in enumerate(path):
        label = f"Step {step}: [{move}]" if move else "Step 0: [START]"
        print(f"\n{label}")
        print_board(state)
        if step < len(path) - 1:
            print("\t |\n\t V")
    print(f"\n{'-'*50}")
    print(f"  Total moves   : {len(path) - 1}")
    print(f"  Nodes explored: {stats['nodes_explored']}")
    print(f"  Nodes generated: {stats['nodes_generated']}")
    print(f"  Max frontier size: {stats['max_frontier']}")
    print("-"*50)



if __name__ == "__main__":
    # Puzzle configuration
    start_state = [
        3, 1, 2,
        0, 4, 6,
        7, 5, 8
    ]
    goal_state = [
        1, 2, 3,
        4, 5, 6,
        7, 8, 0
    ]

    print("  A* - 8 PUZZLE SOLVER")
    print("-"*50)

    print("\nInitial State:")
    print_board(tuple(start_state))

    print("\nGoal State:")
    print_board(tuple(goal_state))

    print("\nSearching with Manhattan Distance heuristic...")
    path, stats = astar(start_state, heuristic=manhattan)

    if path:
        print(f"\n  Goal found! Depth: {len(path) - 1}")
        print_solution(path, stats)
    else:
        print("\n  No solution found. (Puzzle may be unsolvable.)")