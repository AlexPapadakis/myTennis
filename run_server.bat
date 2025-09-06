@echo off

echo Activating my virtual environment...

REM Activate virtual environment
Set-ExecutionPolicy RemoteSigned -Scope Process

call C:\Users\Alex\coding\myTennis\myTennis\fastapi-venv\Scripts\activate.bat
echo Virtual environment activated.

REM Change directory to 'backend'
cd /d C:\Users\Alex\coding\myTennis\myTennis\backend

REM Run UVicorn
uvicorn main:app --reload
