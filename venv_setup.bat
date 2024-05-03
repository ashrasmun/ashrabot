call py -3 -m pip install virtualenv
call py -3 -m virtualenv env
call env\Scripts\activate
call python -m pip install --upgrade pip
call python -m pip install -U twitchio

rem Sounds
call python -m pip install -U twitchio[sounds]
call pip install pyaudio
