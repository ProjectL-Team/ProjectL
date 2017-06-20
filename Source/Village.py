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
from Source.EngineL.Gameplay import Player
import Source.EngineL.Scene as Scene
from Source.WindTurbine import CopperCoil

class Village(Core.Place):
    """
    This is the village itself.
    """
    def on_transfer(self, subject, parent, target):
        Core.Place.on_transfer(self, subject, parent, target)

        if target == self and isinstance(subject, Player):
            habour_road_name = Core.get_res_man().get_string("game.places.roadToHabour.name")
            habour_road = self.parent().findChild(Core.Entity, habour_road_name)
            if habour_road is not None:
                try:
                    habour_road_flooded = bool(habour_road.get_state("flooded"))
                except KeyError:
                    habour_road_flooded = False
            else:
                habour_road_flooded = False

            if habour_road_flooded:
                try:
                    dialogue_triggered = bool(self.get_state("dialogue triggered"))
                except KeyError:
                    dialogue_triggered = False

                if not dialogue_triggered:
                    Scene.XMLScene("Village0", subject).play()
                    self.set_state("dialogue triggered", 1)


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

        return True

class House1(Core.StaticEntity):
    """
    This is the house of family 1.
    """
    def __init__(self, parent=None):
        Core.StaticEntity.__init__(self, parent)
        self.scene = "House1"

    def on_talk_to(self, other_entity):
        try:
            visited_habour = bool(other_entity.get_state("visited habour"))
        except KeyError:
            visited_habour = False
        try:
            visited = bool(self.get_state("visited"))
        except KeyError:
            visited = False

        if visited_habour and not visited:
            self.set_state("visited", 1)
            Scene.XMLScene(self.scene, other_entity).play()
            return True
        else:
            return False

class House2(House1):
    """
    This is the house of family 2.
    """
    def __init__(self, parent=None):
        House1.__init__(self, parent)
        self.scene = "House2"

class House3(House1):
    """
    This is the house of family 3.
    """
    def __init__(self, parent=None):
        House1.__init__(self, parent)
        self.scene = "House3"

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([Village, GerritsHouse, House1, House2, House3])
