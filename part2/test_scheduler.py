# ARI711S - Artificial Intelligence
# Group Project 2026 - Part 2 Tests
# Run with: python3 test_scheduler.py

from shift_solver import Shift_AI_Solver, DAYS, ALL_VARIABLES, MAX_SHIFTS


# helper to create a basic solver for testing
def make_solver(extra_leave=None):
    nurses = ["Tangi", "Matias", "Aguero", "Meke", "Trizzy", "Kamati R", "Beukes D", "Naruseb J"]
    leave = extra_leave if extra_leave else {}
    return Shift_AI_Solver(nurses, leave)


def test_all_21_shifts_assigned():
    solver = make_solver()
    schedule = solver.solve()
    assert schedule is not None, "Schedule should not be None"
    assert len(schedule) == 21, f"Expected 21 shifts but got {len(schedule)}"
    print("  PASS - All 21 shifts were assigned")


def test_max_5_shifts_per_nurse():
    solver = make_solver()
    schedule = solver.solve()
    assert schedule is not None
    counts = {}
    for nurse in schedule.values():
        counts[nurse] = counts.get(nurse, 0) + 1
    for nurse, count in counts.items():
        assert count <= MAX_SHIFTS, f"{nurse} has {count} shifts which is over the limit of {MAX_SHIFTS}"
    print("  PASS - No nurse exceeded 5 shifts")


def test_night_to_morning_rest():
    solver = make_solver()
    schedule = solver.solve()
    assert schedule is not None
    for i in range(len(DAYS) - 1):
        night = f"{DAYS[i]}_Night"
        morning = f"{DAYS[i+1]}_Morning"
        assert schedule[night] != schedule[morning], (
            f"Constraint broken: {schedule[night]} worked {night} and {morning}"
        )
    print("  PASS - Night to Morning rest constraint is satisfied")


def test_nurse_on_leave_not_scheduled():
    leave = {"Tangi": {"Monday", "Tuesday"}}
    solver = make_solver(extra_leave=leave)
    schedule = solver.solve()
    assert schedule is not None
    for var, nurse in schedule.items():
        if nurse == "Tangi":
            day = var.rsplit("_", 1)[0]
            assert day not in leave["Tangi"], f"Tangi is on leave {day} but was scheduled for {var}"
    print("  PASS - Nurses on leave are not scheduled on those days")


def test_node_consistency_removes_leave():
    leave = {"Matias": {"Wednesday"}}
    solver = make_solver(extra_leave=leave)
    solver.enforce_node_consistency()
    for var in ALL_VARIABLES:
        day = var.rsplit("_", 1)[0]
        if day == "Wednesday":
            assert "Matias" not in solver.domains[var], f"Matias should not be in domain of {var}"
    print("  PASS - Node consistency removed Matias from Wednesday shifts")


def test_ac3_works_on_valid_problem():
    solver = make_solver()
    solver.enforce_node_consistency()
    result = solver.ac3()
    assert result == True, "AC-3 should return True for a valid problem"
    print("  PASS - AC-3 returned True for solvable problem")


def test_unsolvable_returns_none():
    # only 2 nurses cant fill 21 shifts with max 5 each
    nurses = ["Tangi", "Matias"]
    solver = Shift_AI_Solver(nurses, {})
    schedule = solver.solve()
    assert schedule is None, "Expected None for unsolvable problem"
    print("  PASS - Unsolvable problem correctly returned None")


def test_mrv_picks_smallest_domain():
    solver = make_solver()
    solver.enforce_node_consistency()
    # force one shift to have only 1 option
    solver.domains["Friday_Night"] = {"Meke"}
    picked = solver.select_unassigned_variable({})
    assert picked == "Friday_Night", f"MRV should pick Friday_Night but picked {picked}"
    print("  PASS - MRV picked the shift with the smallest domain")


def test_staff_file_end_to_end():
    from scheduler import load_staff
    nurses, leave_days = load_staff("staff_small.txt")
    solver = Shift_AI_Solver(nurses, leave_days)
    schedule = solver.solve()
    assert schedule is not None, "Should get a valid schedule from staff_small.txt"
    assert len(schedule) == 21
    print("  PASS - staff_small.txt gives a valid 21-shift schedule")


if __name__ == "__main__":
    print("Running Part 2 tests...\n")
    test_all_21_shifts_assigned()
    test_max_5_shifts_per_nurse()
    test_night_to_morning_rest()
    test_nurse_on_leave_not_scheduled()
    test_node_consistency_removes_leave()
    test_ac3_works_on_valid_problem()
    test_unsolvable_returns_none()
    test_mrv_picks_smallest_domain()
    test_staff_file_end_to_end()
    print("\nAll tests passed!")
