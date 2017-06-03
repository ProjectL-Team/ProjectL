"""
This script creates a handy .zip package of the game.
"""
import shutil
import os

shutil.rmtree("package", ignore_errors=True)
try:
    os.remove("ProjectL.zip")
except FileNotFoundError:
    pass

REQUIRED_DIRS = ["Resources", "Source"]
for path in REQUIRED_DIRS:
    shutil.copytree(path, "package/" + path)

REQUIRED_FILES = ["LICENSE", "ProjectL.pyw", "README.md"]
for path in REQUIRED_FILES:
    shutil.copy(path, "package/" + path)

shutil.make_archive("ProjectL", "zip", "package")

shutil.rmtree("package", ignore_errors=True)
