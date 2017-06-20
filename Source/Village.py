"""
All classes required by the tutorial part of ProjectL

Copyright (C) 2017 Jan-Oliver "Janonard" Opdenhövel
Copyright (C) 2017 Jason "J2a0s0o0n" Becker

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
from Source.WindTurbine import CopperCoil

class GerritsHouse(Core.StaticEntity):
    """
    This is the house of Gerrit Alt, Ivy's mentor.
    """
    def __init__(self, parent=None):
        Core.StaticEntity.__init__(self, parent)

    def on_talk_to(self, other_entity):
        try:
            gave_broken_turbine = bool(self.get_state("gave broken turbine"))
        except KeyError:
            gave_broken_turbine = False

        if gave_broken_turbine:
            wind_turbine = other_entity.findChild(CopperCoil)
            if wind_turbine is None:
                Scene.XMLScene("Gerrit/#1 no coil", other_entity).play()
            else:
                Scene.XMLScene("Gerrit/#1 with coil", other_entity).play()
        else:
            find_name = Core.get_res_man().get_string("game.places.yard.mysteriousFind.name")
            find = other_entity.findChild(Core.Entity, find_name)
            if find is None:
                Scene.XMLScene("Gerrit/#0 no find", other_entity).play()
            else:
                Scene.XMLScene("Gerrit/#0 with find", other_entity).play()

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([GerritsHouse])
