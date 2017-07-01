"""
This module contains the scrap heap on the mountain, which also happens to be a fountain.

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
from Source.EngineL.Gameplay import Player
from  Source.Ladder import LadderTool

class CoveredFountain(Core.Entity):
    """
    This is a scrap heap which also holds the tools to fix up the ladder. When the player uses it,
    it also floods the road to the habour.
    """
    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.activly_usable = True

    def on_transfer(self, subject, parent, target):
        """
        This non-constant, overriden method floods the habour road if the given subject is the
        ladder tool and the target is the player (which means that the player took the tools).
        """
        Core.Entity.on_transfer(self, subject, parent, target)
        if isinstance(subject, LadderTool):
            rth_name = Core.get_res_man().get_string("game.places.roadToHabour.name")
            road_to_habour = Core.SinglePlayerApp.instance().findChild(Core.Place, rth_name)
            road_to_habour.set_state("flooded", 1)
            road_to_habour.spawn("bigheap")

            player_name = Core.get_res_man().get_string("core.player.name")
            player = Core.SinglePlayerApp.instance().findChild(Player, player_name)
            if player is not None:
                player.get_window().show_text("EINE QUELLE HAT SICH GEÖFFNET UND EIN FLUSS FLIEßT")

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([CoveredFountain])
