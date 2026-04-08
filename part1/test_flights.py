"""
Unit tests for Part 1 – Flight Connections Search
Run with:  python3 test_flights.py
"""

import sys
sys.path.insert(0, ".")
import flights  # noqa: E402 – import after path setup


def setup():
    """Load data before each test group."""
    # Reset module globals
    flights.cities.clear()
    flights.airlines.clear()
    flights.city_name_to_ids.clear()
    flights.flight_airline_map.clear()
    flights.load_data("data")


def test_shortest_path_exists():
    """Windhoek → Cairo should be exactly 3 hops."""
    setup()
    src = next(iter(flights.city_name_to_ids["windhoek"]))
    tgt = next(iter(flights.city_name_to_ids["cairo"]))
    path = flights.shortest_path(src, tgt)
    assert path is not None, "Expected a path, got None"
    assert len(path) == 3, f"Expected 3 hops, got {len(path)}"
    print(f"  PASS  Windhoek → Cairo: {len(path)} hops")


def test_same_city():
    """Path from a city to itself should be an empty list."""
    setup()
    cid = next(iter(flights.city_name_to_ids["windhoek"]))
    path = flights.shortest_path(cid, cid)
    assert path == [], f"Expected [], got {path}"
    print("  PASS  Same city returns []")


def test_direct_flight():
    """Windhoek → Lusaka has a direct 1-hop connection."""
    setup()
    src = next(iter(flights.city_name_to_ids["windhoek"]))
    tgt = next(iter(flights.city_name_to_ids["lusaka"]))
    path = flights.shortest_path(src, tgt)
    assert path is not None, "Expected a path, got None"
    assert len(path) == 1, f"Expected 1 hop, got {len(path)}"
    print(f"  PASS  Windhoek → Lusaka: {len(path)} hop")


def test_no_path():
    """A fabricated isolated city should return None."""
    setup()
    # Add an isolated city not connected to anything
    flights.cities["999"] = {"name": "Isolated", "country": "Nowhere", "flights": set()}
    flights.city_name_to_ids["isolated"] = {"999"}
    src = next(iter(flights.city_name_to_ids["windhoek"]))
    path = flights.shortest_path(src, "999")
    assert path is None, f"Expected None, got {path}"
    print("  PASS  No path returns None")


def test_neighbors_for_city():
    """neighbors_for_city should return a non-empty set for Johannesburg."""
    setup()
    jnb_id = next(iter(flights.city_name_to_ids["johannesburg"]))
    neighbors = flights.neighbors_for_city(jnb_id)
    assert isinstance(neighbors, set), "neighbors_for_city should return a set"
    assert len(neighbors) > 0, "Johannesburg should have outgoing flights"
    # Each item should be a (flight_id, city_id) tuple
    for item in neighbors:
        assert isinstance(item, tuple) and len(item) == 2
    print(f"  PASS  neighbors_for_city(Johannesburg): {len(neighbors)} direct routes")


def test_path_format():
    """Each hop in the path must be a 2-tuple (flight_id, city_id)."""
    setup()
    src = next(iter(flights.city_name_to_ids["windhoek"]))
    tgt = next(iter(flights.city_name_to_ids["cairo"]))
    path = flights.shortest_path(src, tgt)
    for hop in path:
        assert isinstance(hop, tuple) and len(hop) == 2, \
            f"Each hop must be a 2-tuple, got: {hop}"
    print(f"  PASS  Path format correct ({len(path)} tuples)")


if __name__ == "__main__":
    print("Running Part 1 tests...\n")
    test_shortest_path_exists()
    test_same_city()
    test_direct_flight()
    test_no_path()
    test_neighbors_for_city()
    test_path_format()
    print("\nAll tests passed!")
