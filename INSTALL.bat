@echo off

echo Check python version...
python check_python.py
if %errorlevel% neq 0 exit /b 1

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 exit /b 1

echo Installing playwright...
playwright install --with-deps

echo Copying .env-example to .env...
copy .env-example .env

echo Please edit the .env file to add your API_ID and API_HASH.
pause
