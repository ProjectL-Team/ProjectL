"""
This script creates a handy .zip package of the game.

Copyright (C) 2017 Jan-Oliver "Janonard" Opdenhövel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
