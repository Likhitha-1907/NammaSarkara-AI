
import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "database" / "schemes.db"


def search_schemes(keyword):
    if not keyword.strip():
        return []

    with sqlite3.connect(DB_FILE) as connection:
        connection.row_factory = sqlite3.Row

        query = """
            SELECT *
            FROM schemes
            WHERE scheme_name LIKE ?
               OR category LIKE ?
               OR target_beneficiary LIKE ?
               OR benefits LIKE ?
        """

        search_term = f"%{keyword.strip()}%"

        results = connection.execute(
            query,
            (search_term, search_term, search_term, search_term)
        ).fetchall()

        return [dict(row) for row in results]


if __name__ == "__main__":
    keyword = input("Enter a scheme name, category or beneficiary: ")

    schemes = search_schemes(keyword)

    if schemes:
        print(f"\nFound {len(schemes)} matching scheme(s):")

        for scheme in schemes:
            print("\nScheme:", scheme["scheme_name"])
            print("Category:", scheme["category"])
            print("Beneficiary:", scheme["target_beneficiary"])
            print("Benefits:", scheme["benefits"])
    else:
        print("\nNo matching schemes found.")

