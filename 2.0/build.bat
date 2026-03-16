@echo off
set verpy = "1.0.0"
set /p resc = "Resources folder: "

echo " - Building Sol executable" && pyinstaller "Sol.py" -i "resources/img/ico.png" --distpath "build" --workpath "versions/temp" --noconfirm
echo " - Copying files into build"
echo " |-> classes" && xcopy /E /I "classes" "build/classes" /Y
echo " |-> resources (%resc%)" && xcopy /E /I "%resc%" "build/%resc%" /Y
echo " |-> tools" && xcopy /E /I "tools" "build/tools" /Y
echo " |-> mods" && xcopy /E /I "mods" "build/mods" /Y
echo " |-> solgamedata" && xcopy /E /I "game.txt" "build/game.txt" /Y
echo " |-> solgame" && xcopy /E /I "classes/soleng.py" "build/classes/soleng.py" /Y

rmdir "versions/temp"
echo " - Launching"
echo " |-> Going to build directory"
cd build
echo " |-> Launching game.. Output:"
Sol