py -3 pip install virtualenv
py -3 -m virtualenv env
env\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -U twitchio

rem Sounds
python -m pip install -U twitchio[sounds]
python -m pip install -U pipwin
pipwin install pyaudio
