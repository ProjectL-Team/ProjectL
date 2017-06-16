"""
This module contains the entities of the habour.

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
import Source.EngineL.Core as Core
from Source.Ladder import FixedLadder
from Source.WindTurbine import CopperCoil

class HabourWall(Core.Entity):
    """
    The wall that holds the copper coil.
    """
    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)

    def on_used(self, user, other_entity=None):
        if isinstance(other_entity, FixedLadder):
            coil = CopperCoil()
            coil.transfer(user)
            return True
        else:
            return False

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([HabourWall])
