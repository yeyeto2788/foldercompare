@echo off
echo(Build the standalone .exe file using pyinstaller)
pyinstaller --onefile --windowed --name foldercompare.exe -y ./gui.py

echo(Move the created .exe into the top-level folder)
move %~dp0dist\foldercompare.exe %~dp0

echo(Remove the folders left over from building)
rd /s /q %~dp0build
rd /s /q %~dp0dist
del %~dp0foldercompare.exe.spec
