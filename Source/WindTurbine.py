"""
This module contains everything required to craft the wind turbine.

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
import Source.EngineL.Scene as Scene

class BrokenWindTurbine(Core.Entity):
    """
    A wind turbine, formerly the mysterious find.
    """
    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.setObjectName("KAPUTTES WINDRAD")
        self.description = "EIN KAPUTTES WINDRAD"
        self.activly_usable = True

    def on_used(self, user, other_entity=None):
        if isinstance(other_entity, CopperCoil):
            self.transfer(None)
            other_entity.transfer(None)
            turbine = WindTurbine()
            turbine.transfer(user)
            user.get_window().show_text(turbine.generate_description())
            return True
        else:
            return False

class CopperCoil(Core.Entity):
    """
    The copper coil which is needed to build the wind turbine.
    """
    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.setObjectName("KUPFERSPULE")
        self.description = "EINE KUPFERSPULE"

class WindTurbine(Core.Entity):
    """
    The fixed wind turbine.
    """
    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.setObjectName("WINDRAD")
        self.description = "EIN WINDRAD"

class Signpost(Core.StaticEntity):
    """
    An unused signpost in Ivy's yard, which will be reused as the pole of her wind turbine.
    """
    def __init__(self, parent=None):
        Core.StaticEntity.__init__(self, parent)
        self.setObjectName("WEGWEISER")
        self.activly_usable = True

    def on_used(self, user, other_entity=None):
        if isinstance(other_entity, WindTurbine):
            other_entity.transfer(None)
            self.set_state("turbine mounted", 1)
            self.setObjectName("AUFGESTELLTES WINDRAD")
            Scene.XMLScene("Ending", user).play()
            return True
        else:
            return False

    def get_raw_description(self):
        try:
            turbine_mounted = bool(self.get_state("turbine mounted"))
        except KeyError:
            turbine_mounted = False

        if turbine_mounted:
            return "DAS WINDRAD PRODUZIERT STROM."
        else:
            return "DAS IST EIN WEGWEISER"

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([BrokenWindTurbine, CopperCoil, WindTurbine, Signpost])
