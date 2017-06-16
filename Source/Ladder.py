"""
This module contains everything required to craft the ladder (and the ladder itself, of course).

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

class Rungs(Core.Entity):
    """
    The rungs of a ladder.
    """
    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.setObjectName("SPROSSEN")
        self.description = "DAS SIND MEHRERE SPROSSEN"
        self.gender = "f"
        self.show_article = False
        self.activly_usable = True

    def on_used(self, user, other_entity=None):
        if isinstance(other_entity, Stringers):
            self.transfer(None)
            other_entity.transfer(None)
            ladder = LooseLadder()
            ladder.transfer(user)
            user.get_window().show_text(ladder.generate_description())
            return True
        else:
            return False

class Stringers(Core.Entity):
    """
    The stringers of the ladder
    """
    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.setObjectName("HOLME")
        self.description = "DAS SIND ZWEI HOLME"
        self.gender = "m"
        self.show_article = False

class LooseLadder(Core.Entity):
    """
    The loose, unfixed ladder.
    """
    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.setObjectName("WACKELIGE LEITER")
        self.description = "DIESE LEITER IST WACKLIG UND MUSS REPARIERT WERDEN"
        self.gender = "f"
        self.activly_usable = True

    def on_used(self, user, other_entity=None):
        if isinstance(other_entity, LadderTool):
            self.transfer(None)
            other_entity.transfer(None)
            ladder = FixedLadder()
            ladder.transfer(user)
            user.get_window().show_text(ladder.generate_description())
            return True
        else:
            return False

class LadderTool(Core.Entity):
    """
    The tool needed to fix the ladder
    """
    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.setObjectName("WERKZEUG")
        self.description = "MIT DIESEM WERKZEUG KANN MAN DIE LEITER REPARIEREN"
        self.gender = "n"

class FixedLadder(Core.Entity):
    """
    The fixed ladder.
    """
    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.setObjectName("LEITER")
        self.description = "MIT DIESER LEITER KOMMT MAN FAST ÜBERALL HIN"
        self.gender = "f"

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([Rungs, Stringers, LooseLadder, LadderTool, FixedLadder])
