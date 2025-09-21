import os
import sys
import json
import argparse
from pathlib import Path
from openai import OpenAI, OpenAIError
from rich.console import Console
from rich.panel import Panel

MODEL = "gpt-4o-mini"
TOKEN_LOG_FILE = Path("token_log.json")

console = Console()

def load_token_total():
    """Load total tokens from log file if exists."""
    if TOKEN_LOG_FILE.exists():
        try:
            data = json.loads(TOKEN_LOG_FILE.read_text())
            return data.get("tokens_total", 0)
        except Exception:
            return 0
    return 0

def save_token_total(total):
    """Save updated token total to log file."""
    with open(TOKEN_LOG_FILE, "w") as f:
        json.dump({"tokens_total": total}, f)

def main():
    # CLI args
    parser = argparse.ArgumentParser(description="Query OpenAI and return JSON")
    parser.add_argument("--phrase", type=str, help="Phrase to send to OpenAI")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(json.dumps({"success": False, "error": "OPENAI_API_KEY not set"}))
        return 1

    client = OpenAI(api_key=api_key)

    # Load running total from log
    running_total = load_token_total()

    # Get phrase
    if args.phrase:
        phrase = args.phrase.strip()
    else:
        try:
            phrase = input("Enter your search phrase: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(json.dumps({"success": False, "error": "Input aborted"}))
            return 0

    if not phrase:
        print(json.dumps({"success": False, "error": "No input provided"}))
        return 2

    try:
        # Call API
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": phrase}],
        )

        ai_text = resp.choices[0].message.content
        tokens_used = resp.usage.total_tokens
        running_total += tokens_used

        # Save updated total
        save_token_total(running_total)

        # JSON output
        out = {
            "input_phrase": phrase,
            "ai_response": ai_text,
            "tokens_this_query": tokens_used,
            "tokens_total": running_total
        }

        # Rich panel log
        console.print(Panel.fit(
            f"[bold cyan]Input:[/bold cyan] {phrase}\n\n"
            f"[bold green]AI:[/bold green] {ai_text}\n\n"
            f"[yellow]Tokens this query:[/yellow] {tokens_used} | "
            f"[magenta]Tokens total:[/magenta] {running_total}",
            title="OpenAI Response",
            border_style="blue"
        ))

        # JSON heading
        console.rule("[bold green]JSON Output[/bold green]")
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
