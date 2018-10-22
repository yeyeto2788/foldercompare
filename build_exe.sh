# Build the standalone .exe file using pyinstaller
pyinstaller --onefile --windowed --icon=./Docs/images/icons/ICO/icon_bk.ico --name foldercompare.exe -y ./gui.py

# Move the created .exe into the top-level folder
mv ./dist/foldercompare.exe .

# Create the exe file from the spec file
pyinstaller final_foldercompare.exe.spec

# Remove the folders left over from building
rm -rf ./build
rm -rf ./dist
rm -rf ./foldercompare.exe.spec
