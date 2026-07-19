@echo off
echo ==========================
echo Installing ATLAS...
echo ==========================

python -m venv .venv

call .venv\Scripts\activate

python -m pip install --upgrade pip

pip install -r requirements.txt

echo.
echo Installation Complete!
pause