COLOR 6
Rem run three terminals to start server and clients for game testing
start cmd /k python .\main.py -host
timeout /t 2 /nobreak > NUL

start /min cmd /c python .\main.py
timeout /t 2 /nobreak > NUL

start /min cmd /c python .\main.py
