"""
This minigame takes place at the road to the habour. To clear the by trash stowed river, Ivy has to
get rid of the big heap and the trash coming from the mountain. If she finally breaks the dam she is
able to cross the river and can go the habour.

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

class BigHeap(Core.StaticEntity):
    """
    The big Heap
    """

    def __init__(self, parent=None):
        Core.StaticEntity.__init__(self, parent)
        self.setObjectName("großer Haufen")
        self.description = "Dieser große Haufen verstopft den Fluss, er macht den Weg zum Hafen\
        unzugängig und bedroht das Dorf!"
        self.gender = "m"
        self.activly_usable = True
        self.set_state("used", 0)

    def on_used(self, user, other_entity=None):
        if other_entity is None and self.get_state("used") == 0:
            user.get_window().show_text("Ach nein! Der Müll steckt ziemlich fest, es tut sich\
            einfach überhaupt nichts. Ich versuch' es gleich nochmal.")
            self.set_state("used", 1)
            return True
        if other_entity is None and self.get_state("used") == 1:
            user.get_window().show_text("Es tut sich was! Ich glaub ich hab die Schwachstelle\
            gefunden. Ein präziser Tritt und das Dorf ist gerettet.")
            self.set_state("used", 2)
            return True
        if other_entity is None and self.get_state("used") == 2:
            user.get_window().show_text("WOAH!!! Ich sollte vorsichtiger sein, fast hätte mich die\
            Strömung mit gerissen. Frei ist der Fluss jetzt auch noch nicht, aber ich glaub' da\
            hat sich was getan.")
            self.set_state("used", 3)
            return True
        if other_entity is None and self.get_state("used") == 3:
            user.get_window().show_text("Jawoll, der Wasserspiegel senkt sich, jedoch wird noch\
            immer Müll angespült, der in der Lage ist, den Fluss in einen riesigen Damm zu\
            verwandeln. Ich sollte schnell was dagegen, unternehmen bevor sich erneut was ansammeln\
            kann!")
            rth_name = Core.get_res_man().get_string("game.places.roadToHabour.name")
            road_to_habour = Core.SinglePlayerApp.instance().findChild(Core.Place, rth_name)
            road_to_habour.spawn("trash")
            self.transfer(None)
            return True
        return False

class Trash(Core.StaticEntity):
    """
    The big Heap
    """

    def __init__(self, parent=None):
        Core.StaticEntity.__init__(self, parent)
        self.setObjectName("Müll")
        self.description = "Der Müll muss noch immer vom Berg bis hierhin angespült worden sein."
        self.gender = "m"
        self.activly_usable = True
        self.set_state("used", 0)
        self.show_article = False
    def on_used(self, user, other_entity=None):
        if other_entity is None and self.get_state("used") == 0:
            user.get_window().show_text("Schön langsam, Ivy. Nur weil du den Müll ans Ufer ziehst\
            musst du nicht gleich im Fluss baden gehen.")
            self.set_state("used", 1)
            return True
        if other_entity is None and self.get_state("used") == 1:
            user.get_window().show_text("Wie viel Müll kommt da denn noch! Irgendwie habe ich mir\
            den Tag anders vorgestellt.")
            self.set_state("used", 2)
            return True
        if other_entity is None and self.get_state("used") == 2:
            user.get_window().show_text("Wir sollten aufhören unseren Müll auf dem Berg zu lagern,\
            denn das was hier angespült wird, muss schon mehrere Jahrer dort oben liegen")
            self.set_state("used", 3)
            return True
        if other_entity is None and self.get_state("used") == 3:
            user.get_window().show_text("Moment mal. Das könnte sich vielleicht als nützlich\
            erweisen und mir die Arbeit erleich... AUFPASSEN! Ich hab wohl gepennt und nicht\
            gesehen, dass noch immer Müll angeschwemmt wird und erneut ist der Fluss verstopft!")
            rth_name = Core.get_res_man().get_string("game.places.roadToHabour.name")
            road_to_habour = Core.SinglePlayerApp.instance().findChild(Core.Place, rth_name)
            road_to_habour.spawn("shovel")
            road_to_habour.spawn("dam")
            self.transfer(None)
            return True
        return False

class Shovel(Core.Entity):
    """
    The shovel
    """
    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.setObjectName("Schaufel")
        self.description = "Eine alte Schaufel. Jemand muss sie bei der Suche nach Ressourcen oben\
        auf dem Berg vergessen haben."
        self.gender = "f"

class Dam(Core.StaticEntity):
    """
    The dam
    """

    def __init__(self, parent=None):
        Core.StaticEntity.__init__(self, parent)
        self.setObjectName("Damm")
        self.description = "Dieser Damm ist noch größer als der Haufen an Müll von vorhin. Jetzt\
        zählt jede Sekunde!"
        self.gender = "m"
        self.activly_usable = True
        self.set_state("used", 0)

    def on_used(self, user, other_entity=None):
        if other_entity is None and self.get_state("used") == 0:
            user.get_window().show_text("Mit meinen bloßen Händen kann das eine Weile dauern.")
            self.set_state("used", 1)
            return True
        if other_entity is None and self.get_state("used") == 1:
            user.get_window().show_text("Ok, ok. Bis auf den Schmerz in meinen Armen und die\
            Tatsache, dass das Wasser gleich das Dorf erreicht, ist doch alles bestens.")
            self.set_state("used", 2)
            return True
        if other_entity is None and self.get_state("used") == 2:
            user.get_window().show_text("Meine Hände sind nicht gerade so effektiv, wie eine\
            Schaufel, doch zumindest ist der Damm jetzt fast gebrochen.")
            self.set_state("used", 3)
            return True
        if other_entity is None and self.get_state("used") == 3:
            user.get_window().show_text("GESCHAFFT! Das Dorf ist nicht mehr bedroht und ich kann\
            endlich wieder zum Hafen, aber warum habe ich nicht die Schaufel von da drüben\
            benutzt?")
            rth_name = Core.get_res_man().get_string("game.places.roadToHabour.name")
            road_to_habour = Core.SinglePlayerApp.instance().findChild(Core.Place, rth_name)
            road_to_habour.set_state("flooded", 0)
            self.transfer(None)
            return True
        if isinstance(other_entity, Shovel) and self.get_state("used") <= 1:
            user.get_window().show_text("Mit der Schaufel geht das ja kinderleicht, nicht viel mehr\
            und der Damm ist gebrochen!")
            self.set_state("used", (self.get_state("used"))+2)
            return True
        if isinstance(other_entity, Shovel) and self.get_state("used") >= 2:
            user.get_window().show_text("GESCHAFFT! Das Dorf ist nicht mehr bedroht und ich kann\
            endlich wieder zum Hafen. Die Schaufel ist jedoch hinüber.")
            other_entity.transfer(None)
            rth_name = Core.get_res_man().get_string("game.places.roadToHabour.name")
            road_to_habour = Core.SinglePlayerApp.instance().findChild(Core.Place, rth_name)
            road_to_habour.set_state("flooded", 0)
            return True
        return False

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([BigHeap, Trash, Shovel, Dam])
