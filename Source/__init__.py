# coding=UTF-8
"""
ProjectL Source Module

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
import Source.EngineL
import Source.Hut
import Source.Roads
import Source.Village
import Source.Ladder
import Source.Mountain

class Game(Source.EngineL.Core.SinglePlayerApp):
    """
    EngineL Game Class
    """
    def __init__(self, argv):
        Source.EngineL.Core.SinglePlayerApp.__init__(self, argv)

        try:
            Source.EngineL.Gameplay.register_entity_classes(self)
            Source.Hut.register_entity_classes(self)
            Source.Roads.register_entity_classes(self)
            Source.Village.register_entity_classes(self)
            Source.Ladder.register_entity_classes(self)
            Source.Mountain.register_entity_classes(self)

            self.restore_world()

            self.connect_places()
        except Exception as err:
            self.crash(str(err))

        for child in self.children():
            if issubclass(child.__class__, Source.EngineL.Core.Entity):
                child.on_game_launched()
