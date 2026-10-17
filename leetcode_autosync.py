from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
SOLUTIONS_DIR = PROJECT_DIR / "solutions"


def main():
    SOLUTIONS_DIR.mkdir(exist_ok=True)
    print("LeetCode AutoSync started!")
    print("Project folder:", PROJECT_DIR)
    print("Solutions folder:", SOLUTIONS_DIR)
    print("Setup successful!")


if __name__ == "__main__":
    main()