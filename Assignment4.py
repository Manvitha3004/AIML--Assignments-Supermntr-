""" Assignment (17/02/2026)
Logic Builder
Description : Print numbers 1 to 50 with Fizz/Buzz logic and count occurrences using loops and functions.
""" 

# ── Logic Builder: FizzBuzz 1–50 ────

def classify(n: int) -> str:
    """Return FizzBuzz label for a given number."""
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


def run_fizzbuzz(start: int = 1, end: int = 50) -> dict:
    """
    Print FizzBuzz from start to end.
    Returns a count dict: {fizz, buzz, fizzbuzz, number}
    """
    counts = {"Fizz": 0, "Buzz": 0, "FizzBuzz": 0, "Number": 0}

    print("\n" + "=" * 45)
    print("         🔢  FizzBuzz  1 – 50")
    print("=" * 45)

    for n in range(start, end + 1):
        label = classify(n)

        # Align output into 5 columns
        print(f"{label:>10}", end="\n" if n % 5 == 0 else "")

        # Count occurrences
        if label in counts:
            counts[label] += 1
        else:
            counts["Number"] += 1

    print("\n" + "=" * 45)
    return counts


def print_summary(counts: dict, total: int) -> None:
    """Display a formatted summary of occurrences."""
    print("         📊  Occurrence Summary")
    print("=" * 45)
    print(f"  {'Category':<12} {'Count':>6}   {'Bar'}")
    print(f"  {'-'*12} {'-'*6}   {'-'*20}")

    for label, count in counts.items():
        bar = "█" * count
        print(f"  {label:<12} {count:>6}   {bar}")

    print("-" * 45)
    print(f"  {'Total':<12} {total:>6}")
    print("=" * 45 + "\n")


# ── Main ────
def main():
    print("\n  Welcome to the Logic Builder Program!")

    counts = run_fizzbuzz(1, 50)
    total  = sum(counts.values())
    print_summary(counts, total)


if __name__ == "__main__":
    main()
