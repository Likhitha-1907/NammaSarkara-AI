
import sqlite3
import re
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "database" / "schemes.db"


def search_schemes(question):
    if not question.strip():
        return []

    # Hindi and Kannada keyword translations
    language_keywords = {
        # Hindi
        "किसान": "farmer",
        "किसानों": "farmers",
        "कृषि": "agriculture",
        "खेती": "farming",
        "योजना": "scheme",
        "योजनाएं": "schemes",
        "योजनाओं": "schemes",
        "छात्र": "student",
        "छात्रों": "students",
        "महिला": "woman",
        "महिलाओं": "women",
        "लाभ": "benefits",
        "पैसा": "financial",
        "सहायता": "assistance",

        # Kannada
        "ಕಾಲೇಜು": "college",
        "ವಿದ್ಯಾರ್ಥಿ": "student",
        "ವಿದ್ಯಾರ್ಥಿಗಳು": "students",
        "ವಿದ್ಯಾರ್ಥಿವೇತನ": "scholarship",
        "ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು": "scholarship",
        "ವಿದ್ಯಾರ್ಥಿವೇತನದ": "scholarship",
        "ಯೋಜನೆ": "scheme",
        "ಯೋಜನೆಗಳು": "schemes",
        "ಸಹಾಯ": "assistance",
        "ಹಣಕಾಸು": "financial",
        "ಸರ್ಕಾರಿ": "government",
        "ರೈತ": "farmer",
        "ರೈತರು": "farmers",
        "ರೈತರ": "farmers",
        "ಕೃಷಿ": "agriculture",
        "ಕೃಷಿಕ": "farmer",
        "ಕೃಷಿಕರು": "farmers",
        "ಬೇಸಾಯ": "farming",
        "ಬೆಳೆ": "crop",
        "ಬೆಳೆಗಳು": "crops",
        "ಯೋಜನೆ": "scheme",
        "ಯೋಜನೆಗಳು": "schemes",
    }

    question_words = question.lower().split()

    translated_words = [
        language_keywords.get(word.strip("।,.?!"), word)
        for word in question_words
    ]

    translated_question = " ".join(translated_words)

    keywords = re.findall(
        r"[a-zA-Z0-9-]+",
        translated_question
    )

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


def get_scheme_details(scheme_name):
    """
    Retrieve complete information about a scheme
    from the local database.
    """

    results = search_schemes(scheme_name)

    if not results:
        return None

    scheme = results[0].copy()
    scheme.pop("_matches", None)

    return scheme
