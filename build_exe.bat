@echo off
echo Build the standalone .exe file using pyinstaller
echo xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
pyinstaller --onefile --windowed --name foldercompare.exe -y ./gui.py
echo xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
echo Move the created .exe into the top-level folder
echo xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
move %~dp0dist\foldercompare.exe %~dp0
echo xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
echo Remove the folders left over from building)
echo xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
rd /s /q %~dp0build
rd /s /q %~dp0dist
del %~dp0foldercompare.exe.spec
