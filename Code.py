import streamlit as st
import os
import ast
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from deepseek import DeepSeekAPI
import re

# 📁 Load API key
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    st.error("❌ API key not found. Please check your .env file.")
    st.stop()

client = DeepSeekAPI(api_key=api_key)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def extract_functions_by_lang(code: str, lang: str):
    if lang.lower() == 'python':
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

    elif lang.lower() in ['c', 'cpp', 'c++']:
        # Naive C/C++ function extractor by regex and brace matching
        pattern = re.compile(
            r'([a-zA-Z_][a-zA-Z0-9_*\s]*?)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*{', re.MULTILINE
        )
        funcs = []
        for match in pattern.finditer(code):
            return_type = match.group(1).strip()
            func_name = match.group(2).strip()
            start = match.start()
            # Brace matching to find function body end
            brace_level = 0
            end = start
            for i in range(start, len(code)):
                if code[i] == '{':
                    brace_level += 1
                elif code[i] == '}':
                    brace_level -= 1
                    if brace_level == 0:
                        end = i + 1
                        break
            snippet = code[start:end]
            funcs.append((func_name, snippet))
        return funcs

    elif lang.lower() == 'javascript':
        # Naive JavaScript function extractor for function declarations only
        pattern = re.compile(
            r'function\s+([a-zA-Z$_][a-zA-Z0-9$_]*)\s*\([^)]*\)\s*{', re.MULTILINE
        )
        funcs = []
        for match in pattern.finditer(code):
            func_name = match.group(1)
            start = match.start()
            # Brace matching
            brace_level = 0
            end = start
            for i in range(start, len(code)):
                if code[i] == '{':
                    brace_level += 1
                elif code[i] == '}':
                    brace_level -= 1
                    if brace_level == 0:
                        end = i + 1
                        break
            snippet = code[start:end]
            funcs.append((func_name, snippet))
        return funcs

    else:
        st.warning(f"Language '{lang}' not supported for function extraction yet.")
        return []

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
        <p>Paste your full code below. The app will extract both system-level insights and function-specific requirements.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    language = st.selectbox(
        "Select your code language",
        options=["Python", "C", "C++", "JavaScript"],
        index=0,
    )
    st.subheader("🔍 Your Code Input")
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

            funcs = extract_functions_by_lang(code_input, language)
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
            st.markdown(
                f"""
                <div style="
                    background-color: #23272f;
                    color: #e0e0e0;
                    padding: 14px 20px;
                    border-radius: 7px;
                    margin-bottom: 12px;
                    font-size: 1.08rem;
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    box-shadow: 0 1px 5px rgba(0,0,0,0.11);
                ">
                    <span style="font-weight: 700;">{idx}. </span>{text}
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        st.subheader("🧩 Function-Level Requirements")
        for idx, req in enumerate(st.session_state.func_reqs, start=1):
            label_text = f"{idx}. {req['Text']}"
            with st.expander(label_text):
                st.code(req["Code"], language=language.lower() if language.lower() != "c++" else "cpp")

        # Prepare CSV export with serial numbering continuing from system to functional requirements
        sys_count = len(st.session_state.system_reqs)
        sys_data = [
            {"S.No.": idx, "Requirement": text, "Category": "System Requirement", "Status": "New"}
            for idx, text in enumerate(st.session_state.system_reqs, start=1)
        ]
        func_data = [
            {"S.No.": idx + sys_count, "Requirement": req["Text"], "Category": "Functional Requirement", "Status": "New"}
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
