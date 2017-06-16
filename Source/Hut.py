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

class Sofa(Core.StaticEntity):
    """
    the sofa
    """

    def __init__(self, parent=None):
        Core.StaticEntity.__init__(self, parent)
        self.set_state("timesScanned", 0)
        self.activly_usable = True

    def on_used(self, user, other_entity=None):
        """
        This non-constant, overriden method does something.
        """
        if other_entity is None:
            if self.get_state("timesScanned") == 0:
                self.set_state("timesScanned", 1)
                user.get_window().show_text("${game.places.hut.sofa.interaction0}")
                return True
            if self.get_state("timesScanned") == 1:
                user.get_window().show_text("${game.places.hut.sofa.interaction1}")
                jam = Jam()
                jam.transfer(user)
                return True
        return False

class Jam(Core.Entity):
    """
    the jam
    """

    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.setObjectName(Core.get_res_man().get_string("game.places.hut.jam.name"))
        self.set_gender("f")
        self.activly_usable = True

    def on_used(self, user, other_entity=None):
        """
        This non-constant, overriden method does something.
        """
        if isinstance(other_entity, Toast):
            if other_entity.get_state("toasted") == 1:
                other_entity.set_state("coated", 1)
                user.get_window().show_text(other_entity.get_raw_description())
                self.transfer(None)
                return True
            else:
                return False
        else:
            return False

class Oven(Core.StaticEntity):
    """
    the oven
    """

    def __init__(self, parent=None):
        Core.StaticEntity.__init__(self, parent)
        self.set_state("on", 0)
        self.activly_usable = True

    def on_used(self, user, other_entity=None):
        """
        This non-constant, overriden method does something.
        """
        if isinstance(other_entity, Wood):
            if self.get_state("on") == 0:
                self.set_state("on", 1)
                other_entity.transfer(None)
                user.get_window().show_text(self.get_raw_description())
                return True
            else:
                return False
        elif isinstance(other_entity, Toast):
            if other_entity.get_state("toasted") == 0 and self.get_state("on") == 1:
                other_entity.set_state("toasted", 1)
                user.get_window().show_text(other_entity.get_raw_description())
                return True
            else:
                return False
        else:
            return False

    def get_raw_description(self):
        """
        This overriden, constant method returns a new description if the status of an entity has
        changed.
        """
        if self.get_state("on") == 1:
            txt = "Ah endlich ist der Ofen an. Der Raum füllt sich direkt mit der angenehmen Wärme."
            return txt
        else:
            return self.description

class Wood(Core.Entity):
    """
    the wood
    """

    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.setObjectName(Core.get_res_man().get_string("game.places.yard.wood.name"))

class Toast(Core.Entity):
    """
    the Toast
    """

    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.set_state("toasted", 0)
        self.set_state("coated", 0)
        self.setObjectName(Core.get_res_man().get_string("game.places.hut.toast.name"))
        self.activly_usable = True

    def on_used(self, user, other_entity=None):
        """
        This non-constant, overriden method does something.
        """
        if isinstance(other_entity, Oven):
            return other_entity.on_used(user, self)
        elif isinstance(other_entity, Jam):
            return other_entity.on_used(user, self)
        elif other_entity is None and self.get_state("coated") == 1:
            self.transfer(None)
            user.set_state("fed up", 1)
            user.get_window().show_text("Nichts geht über ein Marmeladen-Toast am Morgen.")
            return True
        else:
            return False

    def get_raw_description(self):
        """
        This overriden, constant method returns a new description if the status of an entity has
        changed.
        """
        if self.get_state("coated") == 0 and self.get_state("toasted") == 1:
            return "Der Toast ist jetzt getoasted.\
                So ganz ohne Aufstrich will ich ihn aber nicht essen."
        elif self.get_state("coated") == 1 and self.get_state("toasted") == 1:
            return "Perfekt. Mein Toast hat jetzt eine rot-glänzende Marmeladenschicht drauf.\
                Jetzt muss ich ihn nur noch essen."
        else:
            return self.description

class HoleInRoof(Core.StaticEntity):
    """
    This is the hole in the roof which will be filled with the stopper.
    """
    def __init__(self, parent=None):
        Core.StaticEntity.__init__(self, parent)
        self.activly_usable = True

    def on_used(self, user, other_entity=None):
        """
        This non-constant method takes a stopper, destroys itself and the stopper and returns True.
        If the other_entity is not a stopper, it returns False.
        """
        if isinstance(other_entity, Stopper):
            self.transfer(None)
            other_entity.transfer(None)
            user.get_window().show_text("DAS LOCH IST GESTOPFT.")
            return True
        else:
            return False

class Stopper(Core.Entity):
    """
    This is a stopper which is used to fill the whole in the hut's roof.
    """
    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([Sofa, Jam, Oven, Toast, Wood, HoleInRoof, Stopper])
