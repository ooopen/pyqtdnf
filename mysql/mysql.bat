@echo off
cls

echo mysqld ÕýÔÚ¹Ø±Õ ...
ext\Process.exe -k mysqld.exe

echo Starting Mysql
start ext\RunHiddenConsole.exe bin\mysqld.exe
pause