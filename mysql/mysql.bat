@echo off
cls

echo mysqld ���ڹر� ...
ext\Process.exe -k mysqld.exe

echo Starting Mysql
start ext\RunHiddenConsole.exe bin\mysqld.exe
pause