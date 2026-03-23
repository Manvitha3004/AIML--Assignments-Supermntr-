""" Assignment (12/02/2026)
Smart Input Program
Description: Build a Python program that takes a name, age, and a hobby and prints a personalized message while categorizing age using conditionals.
"""

# ── Smart Input Program ───

def categorize_age(age: int) -> str:
    """Return an age category based on the given age."""
    if age < 0:
        return None  # Invalid
    elif age <= 12:
        return "Child"
    elif age <= 17:
        return "Teenager"
    elif age <= 35:
        return "Young Adult"
    elif age <= 59:
        return "Adult"
    else:
        return "Senior"


def get_valid_name() -> str:
    """Prompt until a non-empty alphabetic name is entered."""
    while True:
        name = input("Enter your name: ").strip()
        if name and all(c.isalpha() or c.isspace() for c in name):
            return name.title()
        print("  ⚠  Name must contain letters only. Please try again.\n")


def get_valid_age() -> int:
    """Prompt until a valid non-negative integer age is entered."""
    while True:
        try:
            age = int(input("Enter your age: ").strip())
            if age < 0:
                raise ValueError
            return age
        except ValueError:
            print("  ⚠  Age must be a positive whole number. Please try again.\n")


def get_valid_hobby() -> str:
    """Prompt until a non-empty hobby is entered."""
    while True:
        hobby = input("Enter your hobby: ").strip()
        if hobby:
            return hobby.lower()
        print("  ⚠  Hobby cannot be empty. Please try again.\n")


def print_message(name: str, age: int, hobby: str) -> None:
    """Print a personalized message with age category."""
    category = categorize_age(age)

    print("\n" + "=" * 45)
    print("        🎉  Personalized Message  🎉")
    print("=" * 45)
    print(f"  Hello, {name}!")
    print(f"  You are {age} years old — that makes you a {category}.")
    print(f"  It's awesome that you enjoy {hobby}!")

    # Tailored line based on age group
    if category == "Child":
        print(f"  Keep exploring and having fun with {hobby}!")
    elif category == "Teenager":
        print(f"  {hobby.capitalize()} is a great way to express yourself!")
    elif category == "Young Adult":
        print(f"  Pursuing {hobby} will take you far in life!")
    elif category == "Adult":
        print(f"  It's great that you still make time for {hobby}!")
    else:  # Senior
        print(f"  Your passion for {hobby} is truly inspiring!")

    print("=" * 45 + "\n")


# ── Main ────
def main():
    print("\n Welcome to the Smart Input Program! \n")

    name  = get_valid_name()
    age   = get_valid_age()
    hobby = get_valid_hobby()

    print_message(name, age, hobby)


if __name__ == "__main__":
    main()
