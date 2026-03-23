""" Assignment (19/02/2026)
Student Data Manager
Description: Store data for 5 students using dictionaries, print topper, class average, and assign grades.
"""

# ── Student Data Manager ────

def get_grade(avg: float) -> str:
    """Assign a letter grade based on average marks."""
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"


def get_status(avg: float) -> str:
    """Return pass/fail status."""
    return "✅ Pass" if avg >= 50 else "❌ Fail"


def calculate_average(marks: list) -> float:
    """Return average of a list of marks."""
    return sum(marks) / len(marks)


def find_topper(students: dict) -> str:
    """Return the name of the student with the highest average."""
    return max(students, key=lambda name: students[name]["average"])


def find_class_average(students: dict) -> float:
    """Return the overall class average."""
    total = sum(students[s]["average"] for s in students)
    return total / len(students)


def print_student_report(students: dict) -> None:
    """Print a detailed report card for each student."""
    print("\n" + "=" * 65)
    print("               📋  Student Report Cards")
    print("=" * 65)

    for name, data in students.items():
        avg    = data["average"]
        grade  = data["grade"]
        status = data["status"]
        marks  = data["marks"]
        subjects = ["Math", "Science", "English", "History", "Computer"]

        print(f"\n  Student  : {name}")
        print(f"  {'─' * 40}")
        for subject, mark in zip(subjects, marks):
            bar = "█" * (mark // 10)
            print(f"  {subject:<10}: {mark:>3}/100  {bar}")
        print(f"  {'─' * 40}")
        print(f"  Average  : {avg:.2f}  |  Grade: {grade}  |  {status}")

    print("\n" + "=" * 65)


def print_summary(students: dict) -> None:
    """Print topper, class average, and grade leaderboard."""
    topper        = find_topper(students)
    class_average = find_class_average(students)

    print("               📊  Class Summary")
    print("=" * 65)
    print(f"  🏆  Topper         : {topper} "
          f"({students[topper]['average']:.2f} avg — {students[topper]['grade']})")
    print(f"  📈  Class Average  : {class_average:.2f}")
    print()

    # Leaderboard — sorted by average (highest first)
    print(f"  {'Rank':<6} {'Name':<15} {'Average':>8}  {'Grade':>6}  {'Status'}")
    print(f"  {'─'*6} {'─'*15} {'─'*8}  {'─'*6}  {'─'*10}")

    ranked = sorted(students.items(),
                    key=lambda item: item[1]["average"],
                    reverse=True)

    for rank, (name, data) in enumerate(ranked, start=1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "  ")
        print(f"  {medal} {rank:<4} {name:<15} {data['average']:>7.2f}  "
              f"{data['grade']:>6}  {data['status']}")

    print("=" * 65 + "\n")


# ── Main ────
def main():

    # ── Student data: name → list of 5 subject marks ─────
    raw_data = {
        "Alice":   [92, 88, 95, 91, 96],
        "Bob":     [74, 65, 70, 68, 72],
        "Charlie": [55, 60, 48, 52, 58],
        "Diana":   [85, 90, 88, 92, 87],
        "Ethan":   [40, 45, 38, 50, 42],
    }

    # ── Build enriched student dictionary ────
    students = {}
    for name, marks in raw_data.items():
        avg = calculate_average(marks)
        students[name] = {
            "marks":   marks,
            "average": avg,
            "grade":   get_grade(avg),
            "status":  get_status(avg),
        }

    print("\n  Welcome to the Student Data Manager!")

    print_student_report(students)
    print_summary(students)


if __name__ == "__main__":
    main()
