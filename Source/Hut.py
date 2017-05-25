"""
the Hut
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
                return True
            if self.get_state("timesScanned") == 1:
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

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([Sofa, Jam])
