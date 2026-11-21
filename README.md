# NammaSarkara AI

### Your Multilingual Government Scheme Assistant

## About the Project

NammaSarkara AI is an AI-powered assistant designed to help Indian citizens discover government schemes and understand their benefits, eligibility criteria, required documents, and application procedures.

The project aims to make government scheme information easier to access through simple, multilingual conversations.

## Problem Statement

Many citizens are unaware of government schemes or find it difficult to understand complicated eligibility rules and application procedures. Language barriers and scattered information make access even harder.

## Our Solution

NammaSarkara AI provides a simple interface where citizens can ask questions about government schemes in their preferred language.

## Features

- Multilingual support: English, Hindi, and Kannada.
- Government scheme search.
- Scheme information and eligibility explanations.
- AI-powered question answering.
- SQLite database for storing scheme information.
- Initial PM-KISAN eligibility assessment logic.
- Simple Streamlit web interface.

## Technologies Used

- Python
- Streamlit
- OpenAI API
- SQLite
- Pandas
- CSV
- Pytest

## Project Structure

```text
NammaSarkara-AI/
â”‚
â”œâ”€â”€ agent/
â”‚   â”œâ”€â”€ scheme_agent.py
â”‚   â””â”€â”€ test_api_connection.py
â”‚
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ schemes.csv
â”‚   â””â”€â”€ scheme_research.csv
â”‚
â”œâ”€â”€ database/
â”‚   â””â”€â”€ schemes.db
â”‚
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ validate_data.py
â”‚   â”œâ”€â”€ build_database.py
â”‚   â”œâ”€â”€ scheme_search.py
â”‚   â””â”€â”€ eligibility_checker.py
â”‚
â”œâ”€â”€ tests/
â”‚   â””â”€â”€ test_eligibility.py
â”‚
â”œâ”€â”€ app.py
â”œâ”€â”€ requirements.txt
â””â”€â”€ README.md
```

## How to Run the Project

1. Clone or download the project.
2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Configure your OpenAI API key in a local `.env` file.
5. Validate the scheme data:

```bash
python src/validate_data.py
```

6. Build the SQLite database:

```bash
python src/build_database.py
```

7. Start the application:

```bash
python -m streamlit run app.py
```

## Testing

Run the test suite using:

```bash
python -m pytest -v
```

## Current Limitations

- The current database contains a limited number of government schemes.
- Eligibility assessment is currently implemented as initial PM-KISAN rule-based logic.
- Voice-based interaction is planned for a future version.
- Scheme information must be regularly checked against official government sources.
- Final eligibility is determined by the relevant government authorities.

## Future Scope

- Add more central and Karnataka state government schemes.
- Integrate voice input and output.
- Improve multilingual understanding.
- Add document-based scheme information retrieval.
- Expand automated eligibility assessments.

## Important Note


NammaSarkara AI is an informational assistant. Any eligibility assessment provided by the application is preliminary and does not guarantee approval or benefits. Final eligibility is determined by the relevant government authorities. Citizens should verify scheme details and application deadlines through official government portals before applying.
