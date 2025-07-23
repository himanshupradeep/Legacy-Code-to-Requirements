# Legacy2Reqs: Automated Requirements Extraction from Legacy Code
<img width="1302" height="623" alt="Screenshot 2025-07-23 151334" src="https://github.com/user-attachments/assets/361d9b9e-4fbd-432a-9bc7-fe58147459c7" />

## Overview

**Legacy2Reqs** is a Streamlit-powered tool that helps engineering teams in the automotive industry extract high-level system and function-specific requirements directly from legacy Python codebases. This workflow accelerates requirement traceability, refactoring, and modernization—enabling safer, more agile, and standards-compliant product development.

## Results showcasing Functional Requirements with respective function block snippet
<img width="1139" height="907" alt="Screenshot 2025-07-23 183917" src="https://github.com/user-attachments/assets/5a5867bd-64a3-43df-a0bb-0b447a118697" />

## Results showcasing System Requirements
<img width="1839" height="728" alt="Screenshot 2025-07-23 120037" src="https://github.com/user-attachments/assets/6157875c-7228-43cf-8cec-b7d39fd99b49" />

## Why Extract Requirements from Legacy Code in Automotive?

Automotive suppliers (OEMs, Tier 1/2) often deliver the same base software to multiple customers, customizing features for each project. As legacy code accumulates, capturing and formalizing requirements brings multiple critical benefits:

### 1. **Ensures Compliance and Functional Safety**

- Requirements-centric development is essential for meeting ISO 26262 and other automotive standards for safety, traceability, and verification.

### 2. **Promotes Reuse & Modularization**

- Translating legacy code into explicit requirements enables code/function reuse across projects, facilitating modular architectures and reducing redundant engineering effort.

### 3. **Simplifies Legacy Modernization and Refactoring**

- By making underlying requirements explicit, teams can confidently migrate or refactor code (e.g., to new architectures or languages) while ensuring compatibility with original system intents.

### 4. **Drives Knowledge Transfer & Reduces Dependency on Experts**

- Many legacy codebases are understood by a handful of engineers. Requirement extraction documents the system, reducing key-person risk and aiding onboarding.

### 5. **Improves Customer Alignment and Accelerates Customization**

- Clear requirements make it easier to deliver project-specific variants, satisfy audits, and communicate system capabilities and boundaries to Tier 1/2 customers and OEMs.

## Features

- **Paste Any Python File:** Instantly extract and view both high-level system requirements and per-function requirements.
- **Expandable, Numbered Requirement Cards:** Each requirement is interactive and linked to its code snippet.
- **Export to CSV:** Download a categorized list of all requirements (System/Functional) with serial numbers.
- **Designed for Automotive Legacy Modernization & Safety Workflows**

## Getting Started

1. Clone this repository:<br>
   `git clone https://github.com/himanshupradeep/Legacy-Code-to-Requirements`
2. Install dependencies:<br>
   `pip install -r requirements.txt`
3. Add your DeepSeek API key to a `.env` file:<br>
   DEEPSEEK_API_KEY=your_api_key_here
4. Run the app:<br>
    `streamlit run code.py`
5. Paste your Python code, click **Analyze**, and review the extracted requirements!

## Example: CSV Export Schema

| S.No. | Requirement                                                            | Category                | Status |
|-------|------------------------------------------------------------------------|-------------------------|--------|
| 1     | The system shall support variant-specific configuration.                | System Requirement     | New    |
| 2     | The system shall control CAN communication based on configuration data. | Functional Requirement | New    |
| ...   | ...                                                                    | ...                     | ...    |

## License & Usage

This project is **free to use, modify, and distribute** for anyone whether you are developing your own projects, integrating it for professional use, or studying as a student. No restrictions apply.

Feel free to contribute, experiment, and build upon this tool to suit your needs.
