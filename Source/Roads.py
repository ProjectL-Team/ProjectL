"""
This module contains all roads in the game since they belong to any other module.

Copyright (C) 2017 Jan-Oliver "Janonard" Opdenhövel
Copyright (C) 2017 David "Flummi3" Waelsch

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
from Source.Habour import Habour
import Source.Minigame as Minigame

class RoadToIvy(Core.Place):
    """
    This is the road between Ivy's hut and the village.
    """

    def __init__(self, parent=None):
        Core.Place.__init__(self, parent)

    def check_transfer_as_target(self, subject):
        """
        This non-constant, overriden method checks whether the target has the state "fed up" set to
        1 and only returns True if this is the case. If not, it will post a message that Ivy can not
        when she is still hungry and return False.
        """
        if Core.Place.check_transfer_as_target(self, subject):
            try:
                fed_up = bool(subject.get_state("fed up"))
            except KeyError:
                fed_up = False

            if fed_up:
                return True
            else:
                try:
                    txt = "Ich sollte wohl vorher etwas frühstücken bevor ich ins Dorf gehe. In der\
                    Hütte ist bestimmt noch was zu essen."
                    subject.get_window().show_text(txt)
                except AttributeError:
                    pass
        return False


class RoadToHabour(Core.Place):
    """
    This is the road betwen the Habour and the village.
    """
    def __init__(self, parent=None):
        Core.Place.__init__(self, parent)
        self.set_state("flooded", 0)
    def on_transfer(self, subject, parent, target):
        """
        This non-constant, overriden method starts the scene 'Hex0' if Ivy hadn't met her before.
        """
        if target == self:
            try:
                met_hex = bool(subject.get_state("met Hex"))
            except KeyError:
                met_hex = False

            if not met_hex:
                hex_entity = Core.Entity(self)
                hex_entity.setObjectName("Hex")
                hex_entity.set_gender("f")
                hex_entity.show_article = True
                hex_entity.use_definite_article = True

                Core.Place.on_transfer(self, subject, parent, target)
                Scene.XMLScene("Hex0", subject).play()
                return
        Core.Place.on_transfer(self, subject, parent, target)

    def check_transfer_as_parent(self, subject, target):
        """
        This overriden, constant, semi-abstract method checks whether the planned transfer is ok. If
        the new parent is a place, it tries to find a connection from us to it using a breadth-first
        search. If not, it uses the default behaviour. Returns True if the transfer is okay, False
        if not.
        """
        if Core.Place.check_transfer_as_parent(self, subject, target):
            if isinstance(target, Habour):
                if self.get_state("flooded") == 0:
                    return True
                else:
                    subject.get_window().show_text("Ich komme nicht an dem Fluss vorbei!")
                    return False
            else:
                return True

        return False

    def spawn(self, entity):
        """
        This non-constant method spawns different things at road to the habour.
        """
        if entity == "bigheap":
            Minigame.BigHeap(self)
            return True
        if entity == "trash":
            Minigame.Trash(self)
            return True
        if entity == "shovel":
            Minigame.Shovel(self)
            return True
        if entity == "dam":
            Minigame.Dam(self)
            return True
        return False

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([RoadToIvy, RoadToHabour])
