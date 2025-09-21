# ChatUI deployed on streamlit
from pathlib import Path
import os, json, time
from typing import List, Dict

import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

MODEL_DEFAULT = "gpt-4o-mini"
TOKEN_LOG_FILE = Path("token_log.json")
HISTORY_FILE = Path("streamlit_history.json")

def load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except:
            return default
    return default

def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

def load_token_total() -> int:
    return int(load_json(TOKEN_LOG_FILE, {}).get("tokens_total", 0))

def save_token_total(total: int):
    save_json(TOKEN_LOG_FILE, {"tokens_total": int(total)})

def load_history() -> List[Dict]:
    return load_json(HISTORY_FILE, [])

def save_history(history: List[Dict]):
    save_json(HISTORY_FILE, history)

# build_client: prefer Streamlit secrets (deployed), fallback to env var (local)
def build_client() -> OpenAI:
    api_key = None
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        st.error("OPENAI_API_KEY not found. Add it to Streamlit Secrets or set the OPENAI_API_KEY environment variable.")
        st.stop()

    return OpenAI(api_key=api_key)

st.set_page_config(page_title="Chat UI", layout="wide")

mode = st.sidebar.radio("Theme", ["Dark", "Light"])
if mode == "Dark":
    bg, user_bg, user_color, asst_bg, asst_color = "#111827", "#0b84ff", "white", "#374151", "white"
else:
    bg, user_bg, user_color, asst_bg, asst_color = "#f9fafb", "#0b84ff", "white", "#e5e7eb", "black"

st.markdown(
    f"""
    <style>
    body {{ background:{bg}; }}
    .chat-box {{ height:65vh; overflow-y:auto; padding:1rem; border-radius:8px; background:{bg}; }}
    .msg {{ margin:0.5rem 0; clear:both; }}
    .msg.user {{ text-align:right; }}
    .bubble {{ display:inline-block; padding:10px 14px; border-radius:16px; max-width:70%; font-size:15px; line-height:1.4; }}
    .user .bubble {{ background:{user_bg}; color:{user_color}; border-bottom-right-radius:4px; }}
    .assistant .bubble {{ background:{asst_bg}; color:{asst_color}; border-bottom-left-radius:4px; }}
    .json-box {{ background:#1f2937; color:#f9fafb; padding:12px; border-radius:6px; font-family: monospace; white-space:pre-wrap; }}
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    model = st.selectbox("Model", [MODEL_DEFAULT, "gpt-4o", "gpt-3.5-turbo"])
    system_prompt = st.text_area("System prompt", value="You are concise and helpful.", height=80)
    total = load_token_total()
    st.metric("Tokens total", total)
    if st.button("Reset tokens"):
        save_token_total(0); st.rerun()
    if st.button("Clear history"):
        save_history([]); st.rerun()

st.title("💬 Chat Bot")

history = load_history()
client = build_client()

for entry in reversed(history):
    st.markdown(f"<div class='msg user'><div class='bubble'>{entry['input_phrase']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='msg assistant'><div class='bubble'>{entry['ai_response']}</div></div>", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Message", placeholder="Type here...", height=80)
    submitted = st.form_submit_button("Send")
    if submitted and user_input.strip():
        msgs = []
        if system_prompt.strip():
            msgs.append({"role": "system", "content": system_prompt})
        msgs.append({"role": "user", "content": user_input.strip()})
        resp = client.chat.completions.create(model=model, messages=msgs)
        ai_text = resp.choices[0].message.content
        tokens_used = int(getattr(resp.usage, "total_tokens", 0) or 0)
        total = load_token_total() + tokens_used
        save_token_total(total)

        entry = {
            "timestamp": time.time(),
            "input_phrase": user_input.strip(),
            "ai_response": ai_text,
            "model": model,
            "tokens_this_query": tokens_used,
            "tokens_total": total,
        }
        history.insert(0, entry)
        save_history(history)
        st.rerun()

if history:
    last = history[0]
    st.subheader("Final JSON")
    final_json = {
        "input_phrase": last["input_phrase"],
        "ai_response": last["ai_response"],
        "tokens_this_query": last["tokens_this_query"],
        "tokens_total": last["tokens_total"],
    }
    st.markdown(f"<div class='json-box'>{json.dumps(final_json, indent=2)}</div>", unsafe_allow_html=True)
    st.download_button("Download JSON", data=json.dumps(final_json, indent=2), file_name="response.json")