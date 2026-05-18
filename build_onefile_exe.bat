@echo off
cd /d "%~dp0"
python -m pip install -r requirements.txt
python -m PyInstaller --noconsole --onefile --name NTERayTracingPanel --add-data "web;web" --collect-all py7zz --collect-submodules py7zr app.py
