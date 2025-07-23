@echo off
cd /d D:\Code
call .\env\Scripts\activate

:: Optional: Wait and show Python version (helps confirm env is active)
python --version

:: Run Streamlit
streamlit run code.py

:: Pause to keep the window open and show errors
pause