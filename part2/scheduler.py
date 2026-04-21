# ARI711S - Artificial Intelligence
# Group Project 2026 - Part 2: Hospital Shift Scheduler
# This is the main file that loads the staff and runs the solver


import sys
from shift_solver import Shift_AI_Solver, DAYS, SHIFTS


# reads the staff file and returns list of nurses and their leave days
def load_staff(filename):
    nurses = []
    leave_days = {}

    file = open(filename, "r")
    for line in file:
        line = line.strip()

        # skip empty lines and comments
        if line == "" or line.startswith("#"):
            continue

        parts = [p.strip() for p in line.split(",")]
        name = parts[0]

        # the rest of the columns are leave days (if any)
        leave = set()
        for p in parts[1:]:
            if p != "":
                leave.add(p)

        nurses.append(name)
        leave_days[name] = leave

    file.close()
    return nurses, leave_days


# prints the schedule in a readable format
def print_schedule(schedule, leave_days):
    if schedule is None:
        print("Could not find a valid schedule.")
        return

    totals = {}

    for day in DAYS:
        print(f"\n{day.upper()}:")
        for shift in SHIFTS:
            var = f"{day}_{shift}"
            nurse = schedule[var]

            # keep count of how many shifts each nurse gets
            if nurse not in totals:
                totals[nurse] = 0
            totals[nurse] += 1

            # show which nurses are off today as a note
            off_list = []
            for n, days in leave_days.items():
                if day in days:
                    off_list.append(n)

            note = ""
            if len(off_list) > 0:
                note = "  (Note: " + ", ".join(off_list) + " is Off)"

            print(f"  {shift}: {nurse}{note}")

    # print how many shifts each nurse was assigned
    print("\nSchedule Totals:")
    for nurse in sorted(totals):
        print(f"  - {nurse}: {totals[nurse]} shifts")

    print(f"\nStatus: Done! All {len(schedule)} shifts assigned. Constraints satisfied.")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scheduler.py <staff_file>")
        sys.exit(1)

    filename = sys.argv[1]

    print(f"\nGenerating Weekly Schedule for 2026...g")
    nurses, leave_days = load_staff(filename)
    print(f"Data loaded: {len(nurses)} staff members available.")

    solver = Shift_AI_Solver(nurses, leave_days)
    schedule = solver.solve()

    print_schedule(schedule, leave_days)


if __name__ == "__main__":
    main()
