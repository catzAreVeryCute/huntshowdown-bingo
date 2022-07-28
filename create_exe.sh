# This command won't work by itself. I need to figure out why
# To create the executable, launch this command from the virtualenv if you're using one
# Pyinstaller will create a "dist" and "build" folder
# Afterwards, put a copy of the "assets" folder inside the "dist" folder.
pyinstaller --noconsole --onefile --add-data="./assets;./assets" main.py