import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

def ask(question: str) -> dict:
    """
    Send a question to Claude and get back a structured JSON response.
    """
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="""You are a helpful assistant. 
        Always respond in valid JSON format with this structure:
        {
            "answer": "your answer here",
            "confidence": "high | medium | low",
            "follow_up": "one useful follow-up question the user might want to ask",
            "topic": "one word category of the question"
        }
        Return only the JSON object. No preamble, no markdown backticks.""",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    raw = response.content[0].text

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "Failed to parse response", "raw": raw}


if __name__ == "__main__":
    print("Claude CLI — type 'quit' to exit\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "quit":
            break

        if not question:
            continue

        result = ask(question)
        print("\nClaude:")
        print(f"  Answer     : {result.get('answer', result)}")
        print(f"  Confidence : {result.get('confidence', '-')}")
        print(f"  Follow-up  : {result.get('follow_up', '-')}")
        print()