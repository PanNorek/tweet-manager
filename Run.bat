@echo off

REM If you have Anaconda installed at different location, replace the value of
REM anaconda_root variable with Anaconda root path valid for your system.
REM Edit the line below to set your path (note no leading/trailing spaces)
REM set anaconda_root=c:\Apps\Anaconda3

REM call "%anaconda_root%\Scripts\activate.bat" "%anaconda_root%"
REM cd data
REM "%anaconda_root%\python.exe" "main.py" -c _config.ini

set program_root=C:\Users\Admin\AppData\Local\Programs\Python\Python39\python.exe
call venv\Scripts\activate
cd data
"%program_root%" "main.py" -c _config.ini

pause
exit
REM pause