@echo off
setlocal

if exist %~dp0env\ (
    call %~dp0env\Scripts\activate
) else (
    call venv_setup.py
)

call python bot.py --bot_config c:\home\dev\ashrabot_config.json --blocked_words c:\home\dev\blocked.json
