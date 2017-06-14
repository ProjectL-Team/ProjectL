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

class GerritsHouse(Core.StaticEntity):
    """
    This is the house of Gerrit Alt, Ivy's mentor.
    """
    def __init__(self, parent="None"):
        Core.StaticEntity.__init__(self, parent)

    def on_talk_to(self, other_entity):
        Scene.XMLScene("Gerrit0", other_entity).play()

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([GerritsHouse])
