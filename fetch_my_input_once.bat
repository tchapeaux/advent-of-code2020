set year=2020
set /p mySession=<.secret_session_cookie

echo %mySession%

set day=%1
rem force to 2 digits
set "day=0%day%"
set "day=%day:~-2%"

set inputPath="inputs\day%day%.txt"

if not EXIST %inputPath% (
    curl https://adventofcode.com/%year%/day/%1/input --cookie "session=%mySession%" > %inputPath%
    type %inputPath%
)

