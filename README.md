
# 🚀 OpenAI Search Scripts

A small Python project demonstrating how to interact with the **OpenAI Chat Completions API**.
It includes both a minimal internship deliverable and an enhanced CLI version with styling and token logging.

---

## ✨ Features

- Accepts a phrase as input
- Calls the OpenAI Chat Completions API
- Returns a **well-formatted JSON** response
- Enhanced CLI version with:
  - 🎨 Rich-styled terminal panel
  - 📊 Tokens per query + running total
  - 💾 Persists token usage across runs (`token_log.json`)

---

## 📦 Requirements

- Python 3.9+ (tested on 3.12)
- Virtual environment recommended
- OpenAI account + API key

Install dependencies:

```bash
pip install -r requirements.txt
````

-----

### 🔑 Setup API Key

Before running, export your OpenAI API key:

**macOS / Linux:**

```bash
export OPENAI_API_KEY="sk-..."
```

**Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY="sk-..."
```

-----

## 🚀 Usage

### 1\. Minimal Script (Classic)

```bash
python openai_search_minimal.py
```

**Input:**

```
Enter your search phrase: Explain recursion in one sentence
```

**Output:**
images/classic_example.png


-----

### 2\. CLI Script (Enhanced UI)

```bash
python openai_search_cli.py --phrase "What is 23 * 19?"
```
**Input:**

```
Enter your search phrase: Explain recursion in one sentence
```

**Output:**
/images/cli_example.png
```
