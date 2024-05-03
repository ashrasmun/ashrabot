@echo off
setlocal

if exist %~dp0env\ (
    call %~dp0env\Scripts\activate
) else (
    call venv_setup.bat
)

call python bot.py --bot_config %~dp0config.json --blocked_words %~dp0blocked.json
