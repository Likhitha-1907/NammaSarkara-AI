
import csv
import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = PROJECT_DIR / "data" / "schemes.csv"
DB_FILE = PROJECT_DIR / "database" / "schemes.db"


def build_database():
    if not CSV_FILE.exists():
        print("ERROR: schemes.csv not found.")
        return

    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(CSV_FILE, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        schemes = list(reader)

    if not schemes:
        print("ERROR: No scheme records found.")
        return

    columns = list(schemes[0].keys())

    with sqlite3.connect(DB_FILE) as connection:
        column_definitions = []

        for column in columns:
            if column == "scheme_id":
                column_definitions.append(
                    '"scheme_id" TEXT PRIMARY KEY'
                )
            else:
                column_definitions.append(f'"{column}" TEXT')

        create_query = (
            "CREATE TABLE IF NOT EXISTS schemes ("
            + ", ".join(column_definitions)
            + ")"
        )

        connection.execute(create_query)

        placeholders = ", ".join(["?"] * len(columns))
        column_names = ", ".join(f'"{c}"' for c in columns)

        insert_query = (
            f"INSERT OR REPLACE INTO schemes "
            f"({column_names}) VALUES ({placeholders})"
        )

        values = [
            tuple(row[column] for column in columns)
            for row in schemes
        ]

        connection.executemany(insert_query, values)

        count = connection.execute(
            "SELECT COUNT(*) FROM schemes"
        ).fetchone()[0]

    print("PASS: Database created successfully.")
    print("Scheme records:", count)
    print("Database location:", DB_FILE)


if __name__ == "__main__":
    build_database()
