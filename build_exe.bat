@echo off
echo Build the standalone .exe file using pyinstaller
echo xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
pyinstaller --onefile --windowed --icon=./assets/images/icons/icon_bk.ico --name foldercompare.exe -y ./gui.py
echo xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
echo Creating .exe file from the spec file
echo xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
pyinstaller final_foldercompare.exe.spec
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
