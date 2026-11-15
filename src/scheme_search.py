
import sqlite3
import re
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "database" / "schemes.db"


def search_schemes(question):
    if not question.strip():
        return []

    keywords = re.findall(r"[a-zA-Z0-9-]+", question.lower())

    stop_words = {
        "i", "am", "a", "an", "the", "is", "are", "for",
        "to", "of", "and", "in", "from", "can", "what",
        "how", "do", "get", "me", "my", "any", "please",
        "need", "want", "with", "there"
    }

    keywords = [
        word for word in keywords
        if word not in stop_words and len(word) > 1
    ]

    word_variations = {
        "farmers": ["farmer", "agriculture"],
        "farming": ["farmer", "agriculture"],
        "farmer": ["agriculture"],
        "students": ["student"],
        "girls": ["girl"],
        "scholarships": ["scholarship"],
        "women": ["woman"]
    }

    expanded_keywords = set(keywords)

    for word in keywords:
        if word in word_variations:
            expanded_keywords.update(word_variations[word])

    keywords = list(expanded_keywords)

    if not keywords:
        return []

    with sqlite3.connect(DB_FILE) as connection:
        connection.row_factory = sqlite3.Row

        results = {}

        for keyword in keywords:
            search_term = f"%{keyword}%"

            query = """
                SELECT *
                FROM schemes
                WHERE scheme_name LIKE ?
                   OR category LIKE ?
                   OR target_beneficiary LIKE ?
                   OR benefits LIKE ?
            """

            matches = connection.execute(
                query,
                (search_term,) * 4
            ).fetchall()

            for row in matches:
                scheme = dict(row)
                scheme_id = scheme["scheme_id"]

                if scheme_id not in results:
                    scheme["_matches"] = 0
                    results[scheme_id] = scheme

                results[scheme_id]["_matches"] += 1

        ranked_results = sorted(
            results.values(),
            key=lambda item: item["_matches"],
            reverse=True
        )

        return ranked_results


if __name__ == "__main__":
    question = input("Ask about a government scheme: ")

    schemes = search_schemes(question)

    if schemes:
        print(f"\nFound {len(schemes)} matching scheme(s):")

        for scheme in schemes:
            print("\nScheme:", scheme["scheme_name"])
            print("Category:", scheme["category"])
            print("Beneficiary:", scheme["target_beneficiary"])
            print("Benefits:", scheme["benefits"])
            print("Matching keywords:", scheme["_matches"])
    else:
        print("\nNo matching schemes found.")
