"""
This module contains all roads in the game since they belong to any other module.

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
        try:
            fed_up = bool(subject.get_state("fed up"))
        except KeyError:
            fed_up = False

        if fed_up:
            return True
        else:
            try:
                subject.get_window().show_text("DU BIST NOCH HUNGRIG")
            except AttributeError:
                pass
            return False

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([RoadToIvy])
