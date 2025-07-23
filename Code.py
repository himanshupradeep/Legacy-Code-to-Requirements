import streamlit as st
import os
import ast
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from deepseek import DeepSeekAPI

# 📁 Load API key
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    st.error("❌ API key not found. Please check your .env file.")
    st.stop()

client = DeepSeekAPI(api_key=api_key)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def extract_functions(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        st.error(f"🧯 Syntax error parsing code: {e}")
        return []
    funcs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            src = ast.get_source_segment(code, node)
            funcs.append((node.name, src))
    return funcs

def generate_system_requirements(code: str) -> list:
    prompt = f"""
You are a systems engineering and coding expert.

Analyze this Python application as a whole and extract its system-level functional requirements.

Focus on:
• What the system enables the user to do
• How data flows through the application
• What core capabilities the system provides
• Avoid low-level implementation details

Return 5–10 lines, each beginning with "Text: The system shall..."

Code:
{code}
"""
    try:
        resp = client.chat_completion(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            stream=False,
        )
        content = (
            resp["choices"][0]["message"]["content"]
            if isinstance(resp, dict) and "choices" in resp
            else resp if isinstance(resp, str)
            else ""
        )
        return [
            line.replace("Text:", "").strip()
            for line in content.splitlines()
            if line.strip().startswith("Text:")
        ]
    except Exception as e:
        return [f"⚠️ Error generating high-level requirements: {e}"]

def generate_functional_requirement(name: str, snippet: str) -> str:
    prompt = f"""
You are a requirements engineer.

Write one formal requirement statement for this function starting with "The system shall..."

Function name: {name}
Code:
{snippet}

Return only the requirement statement without any ID or numbering.
"""
    try:
        resp = client.chat_completion(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            stream=False,
        )
        if isinstance(resp, dict) and "choices" in resp:
            text = resp["choices"][0]["message"]["content"].strip()
        elif isinstance(resp, str):
            text = resp.strip()
        else:
            text = ""
        import re
        text = re.sub(r'^\s*(RQ[-\w]*|ID\s*[:\-]?)\s*', '', text, flags=re.I)
        return text
    except Exception as e:
        return f"⚠️ Error generating functional requirement: {e}"

# ─── Session-State Initialization ───────────────────────────────────────────

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "full_code" not in st.session_state:
    st.session_state.full_code = ""
if "timestamp" not in st.session_state:
    st.session_state.timestamp = ""
if "system_reqs" not in st.session_state:
    st.session_state.system_reqs = []
if "func_reqs" not in st.session_state:
    st.session_state.func_reqs = []

# ─── Streamlit UI ─────────────────────────────────────────────────────────────

st.set_page_config(page_title="Code → Intelligent Requirements", layout="wide")

st.markdown(
    """
    <div style="text-align: center; margin-bottom: 30px; font-family:sans-serif;">
        <h1>🕵️‍♂️ Legacy Code → Intelligent Requirements</h1>
        <h3>📘 Instructions</h3>
        <p>Paste your full Python code below. The app will extract both system-level insights and function-specific requirements.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.subheader("🔍 Python Code Input")
    code_input = st.text_area(
        "",
        value=st.session_state.full_code,
        height=300,
    )
    analyze_clicked = st.button("Analyze")

    if analyze_clicked:
        if not code_input.strip():
            st.error("⚠️ Please paste some code first.")
        else:
            st.session_state.analyzed = True
            st.session_state.full_code = code_input
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            st.session_state.timestamp = ts

            with st.spinner("🔄 Generating system-level requirements..."):
                st.session_state.system_reqs = generate_system_requirements(code_input)

            funcs = extract_functions(code_input)
            frs = []
            for name, snippet in funcs:
                with st.spinner(f"📦 Generating requirement for `{name}`..."):
                    text = generate_functional_requirement(name, snippet)
                frs.append({"Name": name, "Text": text, "Code": snippet})
            st.session_state.func_reqs = frs

if st.session_state.analyzed:
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.subheader("📋 High-Level System Requirements")
        for idx, text in enumerate(st.session_state.system_reqs, start=1):
            st.success(f"{idx}. {text}")

        st.subheader("🧩 Function-Level Requirements")
        for idx, req in enumerate(st.session_state.func_reqs, start=1):
            label_text = f"{idx}. {req['Text']}"
            with st.expander(label_text):
                st.code(req["Code"], language="python")

        # Combine system and functional requirements into a single CSV with category and serial numbers
        sys_data = [
            {"S.No.": idx, "Requirement": text, "Category": "System Requirement", "Status": "New"}
            for idx, text in enumerate(st.session_state.system_reqs, start=1)
        ]
        func_data = [
            {"S.No.": idx + len(sys_data), "Requirement": req["Text"], "Category": "Functional Requirement", "Status": "New"}
            for idx, req in enumerate(st.session_state.func_reqs, start=1)
        ]

        combined_df = pd.DataFrame(sys_data + func_data)

        st.subheader("📤 Export Requirements")
        st.download_button(
            label="📥 Download Requirements CSV",
            data=combined_df.to_csv(index=False).encode("utf-8"),
            file_name="requirements.csv",
            mime="text/csv",
        )
