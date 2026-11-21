
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Make the project folders accessible
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from src.scheme_search import search_schemes, get_scheme_details

# Load the API key
load_dotenv(PROJECT_DIR / ".env")

client = OpenAI()


# Tools available to the AI agent
tools = [
    {
        "type": "function",
        "name": "search_schemes",
        "description": "Search the government scheme database using a citizen's question.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The citizen's scheme-related question."
                }
            },
            "required": ["question"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_scheme_details",
        "description": "Retrieve complete details of a government scheme.",
        "parameters": {
            "type": "object",
            "properties": {
                "scheme_name": {
                    "type": "string",
                    "description": "Name of the government scheme."
                }
            },
            "required": ["scheme_name"],
            "additionalProperties": False
        },
        "strict": True
    }
]


def run_scheme_search(question):
    results = search_schemes(question)

    if not results:
        return json.dumps({
            "message": "No matching schemes found in the database."
        }, ensure_ascii=False)

    return json.dumps(results, ensure_ascii=False)


def ask_agent(question, language="English"):

    response = client.responses.create(
        model="gpt-6-luna",
       instructions=(
    "You are NammaSarkara AI, a government scheme information "
    "assistant for Indian citizens. "

    "Always use the search_schemes tool for scheme-related questions. "

    "STRICT DATABASE RULES: "
    "Use only schemes returned by the search_schemes tool. "
    "Never mention a scheme that is not present in the tool results. "
    "Never add unrelated schemes just to provide more information. "
    "If a returned scheme does not match the user's purpose, "
    "clearly explain that it may not be suitable. "
    "If no relevant scheme is found, say that the database "
    "does not currently contain a matching scheme. "

    "Do not invent scheme names, benefits, eligibility rules, "
    "deadlines, or application procedures. "

    "Use simple language that ordinary citizens can understand. "
    "Explain that final eligibility is decided by government authorities. "

    f"Respond in {language}."
),
        input=question,
        tools=tools,
        tool_choice="required"
    )

    # Execute function calls requested by the AI
    tool_outputs = []

    for item in response.output:

        if item.type == "function_call":

            if item.name == "search_schemes":
                print("\n[Agent] Searching the scheme database...")
                arguments = json.loads(item.arguments)

                result = run_scheme_search(
                    arguments["question"]
                )

            elif item.name == "get_scheme_details":
                print("\n[Agent] Retrieving complete scheme details...")
                arguments = json.loads(item.arguments)

                details = get_scheme_details(
                    arguments["scheme_name"]
                )

                result = json.dumps(
                    details if details else {
                        "message": "Scheme not found in the database."
                    },
                    ensure_ascii=False
                )

            else:
                continue

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": result
            })

    # Send database results back to the AI
    if tool_outputs:

        response = client.responses.create(
            model="gpt-6-luna",
            instructions=(
                "Answer using only the supplied database results. "
                "Do not invent missing information. "
                f"Respond in {language}."
            ),
            previous_response_id=response.id,
            input=tool_outputs
        )

    return response.output_text


if __name__ == "__main__":

    print("\n🇮🇳 NAMMASARKARA AI")
    print("Government Scheme Assistant")
    print("--------------------------------")

    question = input("\nAsk your question: ")

    if question.strip():
        answer = ask_agent(question)

        print("\nNammaSarkara AI:")
        print(answer)
    else:
        print("Please enter your question.")
