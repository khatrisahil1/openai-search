# 🚀 OpenAI Search Scripts

A small Python sample project that demonstrates how to use the OpenAI Chat Completions API by taking a search phrase from the user, sending it to the API, and returning a JSON response.
This repo contains **two scripts**:

1. **`openai_search_minimal.py`** – the internship deliverable ✅  
   - Accepts a phrase as input  
   - Calls OpenAI Chat Completions API  
   - Prints the result as well-formatted JSON  

2. **`openai_search_cli.py`** – an upgraded CLI version 🎨  
   - Same JSON output as above  
   - Adds a styled Rich panel in the terminal  
   - Shows **tokens used (this query)** and **running total**  
   - Persists total tokens across runs (`token_log.json`)  

---

## 📦 Requirements

- Python **3.9+** (tested on 3.12)  
- Virtual environment recommended  
- OpenAI account + API key  

Install dependencies:

```bash
pip install -r requirements.txt
