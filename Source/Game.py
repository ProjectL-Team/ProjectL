"""
EngineL Game Template
"""
import EngineL.Core as Core
import EngineL.Gameplay as Gameplay

class Game(Core.SinglePlayerApp):
    """
    EngineL Game Class
    """
    def __init__(self, argv):
        Core.SinglePlayerApp.__init__(self, argv)

        try:
            Gameplay.register_entity_classes(self)

            self.restore_world()

            self.connect_places()
        except Exception as err:
            self.crash(str(err))

if __name__ == "__main__":
    import sys
    GAME_INSTANCE = Game(sys.argv)
    sys.exit(GAME_INSTANCE.exec_())
