"""
test
"""
import EngineL.Core

class Sofa(EngineL.Core.StaticEntity):
    """
    the sofa
    """

    def __init__(self, parent=None):
        EngineL.Core.StaticEntity.__init__(self, parent)
        self.set_state("timesScanned", 0)

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
                Jam(user)
                return True
        return False

class Jam(EngineL.Core.Entity):
    """
    the jam
    """

    def __init__(self, parent=None):
        EngineL.Core.Entity.__init__(self, parent)
        self.setObjectName(EngineL.Core.get_res_man().get_string("game.places.hut.jam.name"))

    def on_used(self, user, other_entity=None):
        """
        This non-constant, overriden method does something.
        """
        if isinstance(other_entity, Toast):
            if other_entity.get_state("toasted") == 1:
                other_entity.set_state("coated", 1)
                self.setParent(None)
                return True
            else:
                return False
        else:
            return False

class Oven(EngineL.Core.StaticEntity):
    """
    the oven
    """

    def __init__(self, parent=None):
        EngineL.Core.StaticEntity.__init__(self, parent)
        self.set_state("on", 0)

    def on_used(self, user, other_entity=None):
        """
        This non-constant, overriden method does something.
        """
        if isinstance(other_entity, Wood):
            if self.get_state("on") == 0:
                self.set_state("on", 1)
                other_entity.setParent(None)
                return True
            else:
                return False
        elif isinstance(other_entity, Toast):
            if other_entity.get_state("toasted") == 0 and self.get_state("on") == 1:
                other_entity.set_state("toasted", 1)
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
            return "DER OFEN IST AN"
        else:
            return self.description

class Wood(EngineL.Core.Entity):
    """
    the wood
    """

    def __init__(self, parent=None):
        EngineL.Core.Entity.__init__(self, parent)
        self.setObjectName(EngineL.Core.get_res_man().get_string("game.places.yard.wood.name"))

    def on_used(self, user, other_entity=None):
        """
        This non-constant, overriden method does something.
        """
        if isinstance(other_entity, Oven):
            return other_entity.on_used(user, self)
        else:
            return False

class Toast(EngineL.Core.Entity):
    """
    the Toast
    """

    def __init__(self, parent=None):
        EngineL.Core.Entity.__init__(self, parent)
        self.set_state("toasted", 0)
        self.set_state("coated", 0)
        self.setObjectName(EngineL.Core.get_res_man().get_string("game.places.hut.toast.name"))

    def on_used(self, user, other_entity=None):
        """
        This non-constant, overriden method does something.
        """
        if isinstance(other_entity, Oven):
            return other_entity.on_used(user, self)
        elif isinstance(other_entity, Jam):
            return other_entity.on_used(user, self)
        elif other_entity is None and self.get_state("coated") == 1:
            self.setParent(None)
            return True
        else:
            return False

    def get_raw_description(self):
        """
        This overriden, constant method returns a new description if the status of an entity has
        changed.
        """
        if self.get_state("coated") == 0 and self.get_state("toasted") == 1:
            return "DAS TOAST IST LECKER GETOASTED"
        elif self.get_state("coated") == 1 and self.get_state("toasted") == 1:
            return "DAS TOAST IST BESTRICHEN"
        else:
            return self.description

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([Sofa, Jam, Oven, Toast, Wood])
