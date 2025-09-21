# openai_search_minimal.py
import os
import json
import sys
from openai import OpenAI, OpenAIError

MODEL = "gpt-4o-mini"

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(json.dumps({"success": False, "error": "OPENAI_API_KEY not set"}))
        return 1

    client = OpenAI(api_key=api_key)

    try:
        phrase = input("Enter your search phrase: ").strip()
    except (KeyboardInterrupt, EOFError):
        print(json.dumps({"success": False, "error": "Input aborted"}))
        return 0

    if not phrase:
        print(json.dumps({"success": False, "error": "No input provided"}))
        return 2

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": phrase}],
        )

        ai_text = resp.choices[0].message.content
        tokens = resp.usage.total_tokens

        out = {
            "input_phrase": phrase,
            "ai_response": ai_text,
            "tokens_used": tokens,
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    except OpenAIError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        return 3
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        return 4

if __name__ == "__main__":
    sys.exit(main())
