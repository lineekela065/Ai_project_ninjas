# ARI711S - Artificial Intelligence
# Group Project 2026 - Part 2: Hospital Shift Scheduler
# Using CSP: Backtracking + AC3 + MRV heuristic

from collections import deque

# days of the week and shift types
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SHIFTS = ["Morning", "Afternoon", "Night"]

# all 21 shift slots (7 days x 3 shifts)
ALL_VARIABLES = [f"{day}_{shift}" for day in DAYS for shift in SHIFTS]

# max shifts a nurse can work in a week
MAX_SHIFTS = 5


class Shift_AI_Solver:

    def __init__(self, nurses, leave_days):
        self.nurses = nurses
        self.leave_days = leave_days
        self.variables = ALL_VARIABLES[:]

        # build the domain for each shift slot
        # domain = set of nurses who CAN work that shift (not on leave)
        self.domains = {}
        for var in self.variables:
            day = var.rsplit("_", 1)[0]
            self.domains[var] = set()
            for nurse in nurses:
                if day not in leave_days.get(nurse, set()):
                    self.domains[var].add(nurse)

        # binary constraints: night shift -> next morning (same nurse cant do both)
        self.arcs = []
        for i in range(len(DAYS) - 1):
            night = f"{DAYS[i]}_Night"
            next_morning = f"{DAYS[i+1]}_Morning"
            self.arcs.append((night, next_morning))
            self.arcs.append((next_morning, night))

    # step 1: node consistency
    # remove nurses who are on leave from each shift domain
    def enforce_node_consistency(self):
        for var in self.variables:
            day = var.rsplit("_", 1)[0]
            nurses_to_remove = set()
            for nurse in self.domains[var]:
                if day in self.leave_days.get(nurse, set()):
                    nurses_to_remove.add(nurse)
            self.domains[var] -= nurses_to_remove

    # step 2: revise - make x arc consistent with y
    # if assigning a nurse to x means y has no valid nurse left, remove them
    def revise(self, x, y):
        # only check if there is a constraint between x and y
        if (x, y) not in self.arcs:
            return False

        revised = False
        nurses_to_remove = set()

        for nurse in self.domains[x]:
            # check if there is at least one valid nurse in domain(y) thats not this nurse
            found_valid = False
            for other in self.domains[y]:
                if other != nurse:
                    found_valid = True
                    break
            if not found_valid:
                nurses_to_remove.add(nurse)

        if nurses_to_remove:
            self.domains[x] -= nurses_to_remove
            revised = True

        return revised

    # step 3: AC-3 algorithm
    # enforce arc consistency across all variables before we start searching
    def ac3(self):
        queue = deque(self.arcs)

        while queue:
            x, y = queue.popleft()

            if self.revise(x, y):
                # if domain of x is empty, no solution possible
                if len(self.domains[x]) == 0:
                    return False

                # re-check all arcs pointing to x
                for (a, b) in self.arcs:
                    if b == x and a != y:
                        queue.append((a, x))

        return True

    # step 4: MRV heuristic
    # pick the shift with the fewest nurses left in its domain
    def select_unassigned_variable(self, assignment):
        unassigned = []
        for v in self.variables:
            if v not in assignment:
                unassigned.append(v)

        # return the one with smallest domain (most constrained)
        best = unassigned[0]
        for v in unassigned:
            if len(self.domains[v]) < len(self.domains[best]):
                best = v
        return best

    # check if nurse can be assigned to this shift without breaking constraints
    def is_valid(self, var, nurse, assignment):
        day = var.rsplit("_", 1)[0]
        shift_type = var.rsplit("_", 1)[1]
        day_index = DAYS.index(day)

        # check night -> morning rest constraint
        if shift_type == "Night" and day_index < len(DAYS) - 1:
            next_morning = f"{DAYS[day_index + 1]}_Morning"
            if assignment.get(next_morning) == nurse:
                return False

        if shift_type == "Morning" and day_index > 0:
            prev_night = f"{DAYS[day_index - 1]}_Night"
            if assignment.get(prev_night) == nurse:
                return False

        # check nurse hasnt hit the 5 shift limit
        count = 0
        for assigned_nurse in assignment.values():
            if assigned_nurse == nurse:
                count += 1
        if count >= MAX_SHIFTS:
            return False

        return True

    # step 5: backtracking search
    # tries to assign nurses to all 21 shifts, backtracks if stuck
    def backtrack(self, assignment):
        # if all shifts are assigned we are done
        if len(assignment) == len(self.variables):
            return assignment

        # pick next shift to fill using MRV
        var = self.select_unassigned_variable(assignment)

        for nurse in self.domains[var]:
            if self.is_valid(var, nurse, assignment):
                assignment[var] = nurse

                result = self.backtrack(assignment)
                if result is not None:
                    return result

                # backtrack - remove and try next nurse
                del assignment[var]

        return None

    # main solve function - runs everything in order
    def solve(self):
        print("Enforcing node consistency...")
        self.enforce_node_consistency()

        print("Running AC-3 algorithm...")
        possible = self.ac3()
        if not possible:
            print("No solution found by AC-3.")
            return None

        print("Starting backtracking search...")
        result = self.backtrack({})
        return result
