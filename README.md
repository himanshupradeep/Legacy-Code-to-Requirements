# Legacy2Reqs: Automated Requirements Extraction from Legacy Code
<img width="1576" height="902" alt="Screenshot 2025-07-24 123945" src="https://github.com/user-attachments/assets/47b64b86-6ca2-4c79-be17-d5913c5cd3d6" />



## Overview

This is an AI-powered Python application that helps engineering teams in the automotive industry extract high-level system and function-specific requirements directly from legacy C, C++, JavaScript and Python codebases. This workflow accelerates requirement traceability, refactoring, and modernization enabling safer, more agile, and standards-compliant product development.

## Code Example
The ADAS Adaptive Cruise Control (ACC) code snippet simulates a realistic vehicle speed and distance control system that automatically maintains safe following distance and adjusts speed based on sensor data. It includes modular functions for initialization, sensor input processing, state management (OFF, STANDBY, ACTIVE, ERROR), speed control via acceleration commands, and status reporting. This structured, well-commented code with clear functional boundaries enables the requirements extraction tool to generate meaningful system-level and function-level requirements reflecting real-world ACC capabilities and control logic.

This explanation highlights the key aspects inside the code that drive the generated requirements, helping your viewers connect the code structure and behavior to the formalized requirements statements.
## Results showcasing Functional Requirements with respective function block snippet
<img width="1557" height="880" alt="image" src="https://github.com/user-attachments/assets/9b560228-037d-4b24-979b-e3c29477481b" />


## Results showcasing System Requirements
<img width="1401" height="704" alt="Screenshot 2025-07-24 124311" src="https://github.com/user-attachments/assets/ed810773-5d5c-486a-a7c9-8aa577a3bb1a" />



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

- **Paste Any code :** Instantly extract and view both high-level system requirements and per-function requirements.
- **Expandable, Numbered Requirement Cards:** Each requirement is interactive and linked to its code snippet.
- **Export to CSV:** Download a categorized list of all requirements (System/Functional) with serial numbers.
- **Designed for Automotive Legacy Modernization & Safety Workflows**

## Getting Started

1. Clone this repository:<br>
   `git clone https://github.com/himanshupradeep/Legacy-Code-to-Requirements`
2. Install dependencies:<br>
   `pip install -r requirements.txt`
3. Add your DeepSeek API key to a `.env` file:<br>
   `DEEPSEEK_API_KEY=your_api_key_here`
4. Run the app:<br>
    `streamlit run code.py`
5. Paste your code, click **Analyze**, and review the extracted requirements!

## Example: CSV Export Schema

| S.No. | Requirement                                                            | Category                | Status |
|-------|------------------------------------------------------------------------|-------------------------|--------|
| 1     | The system shall support variant-specific configuration.                | System Requirement     | New    |
| 2     | The system shall control CAN communication based on configuration data. | Functional Requirement | New    |
| ...   | ...                                                                    | ...                     | ...    |

<img width="1315" height="509" alt="image" src="https://github.com/user-attachments/assets/fd64b98b-9886-4890-848c-50f769df83ed" />


## License & Usage

This project is **free to use, modify, and distribute** for anyone whether you are developing your own projects, integrating it for professional use, or studying as a student.

Feel free to contribute, experiment, and build upon this tool to suit your needs.
