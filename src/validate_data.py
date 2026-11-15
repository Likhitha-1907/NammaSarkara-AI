
import csv
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

FILES = {
    "schemes.csv": PROJECT_DIR / "data" / "schemes.csv",
    "scheme_research.csv": PROJECT_DIR / "data" / "scheme_research.csv",
}


def validate_csv(file_name, file_path):
    print(f"\nChecking {file_name}...")

    if not file_path.exists():
        print("ERROR: File not found.")
        return False

    with open(file_path, encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        print("ERROR: No data records found.")
        return False

    ids = []
    errors = []

    for row_number, row in enumerate(rows, start=2):
        if not row.get("scheme_id", "").strip():
            errors.append(f"Row {row_number}: Missing scheme ID.")

        if not row.get("scheme_name", "").strip():
            errors.append(f"Row {row_number}: Missing scheme name.")

        ids.append(row.get("scheme_id", "").strip())

    if len(ids) != len(set(ids)):
        errors.append("Duplicate scheme IDs found.")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return False

    print("PASS: All records passed basic validation.")
    print("Records:", len(rows))
    return True


if __name__ == "__main__":
    results = [
        validate_csv(name, path)
        for name, path in FILES.items()
    ]

    print("\nOverall result:", "PASS" if all(results) else "CHECK ERRORS")
