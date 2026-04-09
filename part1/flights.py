"""
Part 1: Search Algorithms – Flight Connections Between Cities
ARI711S Artificial Intelligence – Group Project 2026

This program finds the shortest flight path between any two cities using
Breadth-First Search (BFS), which guarantees the minimum number of connections.
"""

import csv
import sys


# ─────────────────────────────────────────────
#  Data structures
# ─────────────────────────────────────────────

# city_name (lowercase) -> set of city_ids
city_name_to_ids = {}

# city_id -> {"name": str, "country": str, "flights": set of (flight_id, dest_city_id)}
cities = {}

# airline_id -> airline_name
airlines = {}

# flight_id -> airline_id
flight_airline_map = {}


# ─────────────────────────────────────────────
#  Search node & frontier classes
# ─────────────────────────────────────────────

class Node:
    """
    Represents a state in the search tree.

    Attributes
    ----------
    state  : the city_id at this node
    parent : the parent Node (None for the initial node)
    action : the (flight_id, city_id) pair that led to this node
    """

    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    """LIFO frontier – implements Depth-First Search (DFS)."""

    def __init__(self):
        self._frontier = []

    def add(self, node):
        self._frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self._frontier)

    def empty(self):
        return len(self._frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty.")
        return self._frontier.pop()


class QueueFrontier(StackFrontier):
    """FIFO frontier – implements Breadth-First Search (BFS). Guarantees shortest path."""

    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty.")
        return self._frontier.pop(0)


# ─────────────────────────────────────────────
#  Data loading
# ─────────────────────────────────────────────

def load_data(directory):
    """
    Load cities, flights, and airlines from CSV files in *directory*.

    Expected files
    --------------
    cities.csv   : city_id, city_name, country
    flights.csv  : flight_id, source_city_id, destination_city_id, airline_id
    airlines.csv : airline_id, airline_name
    """

    # Airlines
    with open(f"{directory}/airlines.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            airlines[row["airline_id"]] = row["airline_name"]

    # Cities
    with open(f"{directory}/cities.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cid = row["city_id"]
            name = row["city_name"]
            cities[cid] = {
                "name": name,
                "country": row["country"],
                "flights": set(),
            }
            city_name_to_ids.setdefault(name.lower(), set()).add(cid)

    # Flights
    with open(f"{directory}/flights.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            src = row["source_city_id"]
            dst = row["destination_city_id"]
            fid = row["flight_id"]
            aid = row["airline_id"]
            if src in cities:
                cities[src]["flights"].add((fid, dst))
            flight_airline_map[fid] = aid


# ─────────────────────────────────────────────
#  Required functions
# ─────────────────────────────────────────────

def neighbors_for_city(city_id):
    """
    Return all cities directly reachable from *city_id* by a single flight.

    Returns
    -------
    set of (flight_id, city_id) tuples
    """
    if city_id not in cities:
        return set()
    return cities[city_id]["flights"]


def shortest_path(source, target):
    """
    Find the shortest path (fewest connections) from *source* to *target*.

    Uses Breadth-First Search so the first solution found is guaranteed to
    use the minimum number of flights.

    Returns
    -------
    list of (flight_id, city_id) tuples, or None if no path exists.
    """

    if source == target:
        return []

    frontier = QueueFrontier()
    frontier.add(Node(state=source, parent=None, action=None))
    explored = set()

    while not frontier.empty():
        node = frontier.remove()

        if node.state in explored:
            continue
        explored.add(node.state)

        for flight_id, neighbor_id in neighbors_for_city(node.state):
            if neighbor_id in explored:
                continue

            child = Node(state=neighbor_id, parent=node, action=(flight_id, neighbor_id))

            # Goal check on addition (more efficient)
            if neighbor_id == target:
                return _reconstruct_path(child)

            if not frontier.contains_state(neighbor_id):
                frontier.add(child)

    return None


def _reconstruct_path(node):
    """Walk back up the parent chain to build the ordered path."""
    path = []
    while node.action is not None:
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path


# ─────────────────────────────────────────────
#  User interaction
# ─────────────────────────────────────────────

def resolve_city(prompt):
    """
    Prompt the user for a city name and resolve it to a single city_id.
    Handles ambiguous names gracefully.
    """
    while True:
        name = input(prompt).strip()
        key = name.lower()

        if key not in city_name_to_ids:
            print(f'  City "{name}" not found. Please try again.')
            continue

        matches = city_name_to_ids[key]

        if len(matches) == 1:
            return next(iter(matches))

        print(f'  Multiple cities named "{name}" found:')
        sorted_matches = sorted(matches)
        for idx, cid in enumerate(sorted_matches, 1):
            c = cities[cid]
            print(f"    {idx}. {c['name']}, {c['country']} (ID: {cid})")

        while True:
            choice = input("  Enter the number of the city you mean: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(sorted_matches):
                return sorted_matches[int(choice) - 1]
            print("  Invalid choice. Please enter a valid number.")


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

def main():
    if len(sys.argv) != 2:
        print("Usage: python flights.py <data-directory>")
        sys.exit(1)

    data_dir = sys.argv[1]

    print("Loading data...")
    load_data(data_dir)
    print(f"Data loaded. ({len(cities)} cities, {len(airlines)} airlines)\n")

    source_id = resolve_city("City: ")
    target_id = resolve_city("City: ")

    if source_id == target_id:
        print("Source and destination are the same city.")
        return

    path = shortest_path(source_id, target_id)

    if path is None:
        print("\nNo flight connections exist between those two cities.")
        return

    print(f"\n{len(path)} flight connection(s).\n")

    current_id = source_id
    for hop_num, (flight_id, dest_id) in enumerate(path, 1):
        src_name = cities[current_id]["name"]
        dst_name = cities[dest_id]["name"]
        airline_name = airlines.get(flight_airline_map.get(flight_id, ""), "Unknown Airline")
        print(f"  {hop_num}: {src_name} -> {dst_name}  (Flight {flight_id}, {airline_name})")
        current_id = dest_id


if __name__ == "__main__":
    main()
