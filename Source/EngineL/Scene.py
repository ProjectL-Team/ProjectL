"""
The Scene module contains everything you need to create scenes (cutscenes and dialogues).

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
from xml.etree import ElementTree
from PyQt5.QtCore import QObject, QEvent, pyqtSignal

class XMLScene(QObject):
    """
    This is the base class for scenes designed in XML
    """

    def __init__(self, scene_name, player):
        QObject.__init__(self, player)

        self.player = player

        self.elements = [ClearCommandRowElement(self)]

        self.xml_tree = ElementTree.parse("Resources/" + scene_name + ".xml")

        for xml_element in list(self.xml_tree.getroot()):
            previous_element = self.elements[-1]
            if xml_element.tag == "text":
                self.elements.append(TextElement(self, xml_element))
            elif xml_element.tag == "delay":
                self.elements.append(DelayElement(self, xml_element))
            else:
                raise Exception()
            previous_element.end.connect(self.elements[-1].play)

        previous_element = self.elements[-1]
        self.elements.append(ShowCommandLineElement(self))
        previous_element.end.connect(self.elements[-1].play)

    def get_player(self):
        """
        This constant method returns our player.
        """
        return self.player

    def play(self):
        """
        This non-constant method starts the scene.
        """
        self.elements[0].play()

class SceneElement(QObject):
    """
    Abstract base class for scene elements.
    """
    def __init__(self, scene):
        QObject.__init__(self, scene)

    def play(self):
        """
        Starts the scene element's action. Subclasses need to override it.
        """
        raise NotImplementedError

    end = pyqtSignal()

class ClearCommandRowElement(SceneElement):
    """
    This scene element removes all widgets from the command row.
    """
    def __init__(self, scene):
        SceneElement.__init__(self, scene)

    def play(self):
        self.parent().get_player().get_window().clear_command_row()
        self.end.emit()

class ShowCommandLineElement(SceneElement):
    """
    This scene element clears the command row and adds the command line again.
    """
    def __init__(self, scene):
        SceneElement.__init__(self, scene)

    def play(self):
        self.parent().get_player().get_window().clear_command_row()
        self.parent().get_player().get_window().add_command_line()
        self.end.emit()

class TextElement(SceneElement):
    """
    A scene element that prints a text when it is played.
    """
    def __init__(self, scene, xml_element):
        SceneElement.__init__(self, scene)
        self.text = xml_element.text

    def set_text(self, text):
        """
        Sets our text
        """
        self.text = text

    def get_text(self):
        """
        This constant method returns our text.
        """
        return self.text

    def play(self):
        self.parent().get_player().get_window().show_text(self.text)
        self.end.emit()

class DelayElement(SceneElement):
    """
    This scene element waits for a predefined amount of time and fires it's end_0 when the time is
    over.
    """
    def __init__(self, scene, xml_element):
        SceneElement.__init__(self, scene)
        self.time = int(xml_element.get("time"))
        self.timer_id = -1

    def set_time(self, time):
        """
        This non-constant method sets our waiting time.
        """
        self.time = time

    def get_time(self):
        """
        This constant method returns our waiting time.
        """
        return self.time

    def play(self):
        self.timer_id = self.startTimer(self.time)

    def event(self, event):
        """
        This non-constant method checks for the timer to finish.
        """
        if event.type() == QEvent.Timer:
            self.killTimer(self.timer_id)
            self.end.emit()
            return True
        return QObject.event(self, event)
'''
class OptionElement(SceneElement):
    """
    This scene element let's you add options the player can choose from.
    """
    def __init__(self, scene, awaited_end):
        SceneElement.__init__(self, scene, awaited_end)
        self.options = []
        self.buttons = []
        self.down_button_index = -1

    def add_option(self, option_text):
        """
        This non-constant method adds one option the player can choose. The option_text may contain
        unresolved resource string keys, but no HTML tags.
        """
        self.options.append(option_text)

    def play(self, end_number):
        if end_number == self.awaited_end:
            if len(self.options) == 0:
                self.end.emit(0)
                return
            for text in self.options:
                new_button = self.window.add_option_button(text)
                new_button.pressed.connect(self.button_pressed)
                self.buttons.append(new_button)

    def button_pressed(self):
        """
        This non-constant method checks which button is currently pressed and connects it's
        'clicked' signal to our 'button_clicked' method, which will emit our end.
        """
        for i in range(0, len(self.buttons)):
            if self.buttons[i].isDown():
                self.buttons[i].clicked.connect(self.button_clicked)
                self.down_button_index = i

    def button_clicked(self):
        """
        This non-constant method prints the chosen option text and emits our end signal.
        """
        text = self.options[self.down_button_index]
        self.parent().get_player().get_window().show_command(text)
        self.end.emit(self.down_button_index)
'''