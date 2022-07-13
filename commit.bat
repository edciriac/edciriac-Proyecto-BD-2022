@ECHO OFF
git status

:choice
set /P c= Quieres agregar todo al commmit? [Y/N]?
if /I "%c%" EQU "Y" goto :add_all_commit_push
if /I "%c%" EQU "N" goto :stop_script
goto :choice

:add_all_commit_push
echo "Comiteando todo"
git add --all
set /p msg="Commit message: "
echo %msg%
git commit -m "%msg%"


:stop_script
echo "Saliendo sin commits"
pause
