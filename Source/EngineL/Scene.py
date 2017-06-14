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
from PyQt5.QtCore import Qt, QObject, QCoreApplication, QEvent, pyqtSignal
from Source.EngineL import Core

class XMLScene(QObject):
    """
    This is the base class for scenes designed in XML
    """

    def __init__(self, scene_name, player):
        QObject.__init__(self, player)

        self.player = player

        try:
            self.xml_tree = ElementTree.parse("Resources/" + scene_name + ".xml")
        except ElementTree.ParseError as error:
            QCoreApplication.instance().crash(str(error))

        self.elements = [ClearCommandRowElement(self)]
        self.elements = generate_scene_element_path(self, self.xml_tree.getroot(), self.elements)

        previous_element = self.elements[-1]
        self.elements.append(ShowCommandLineElement(self))
        previous_element.end.connect(self.elements[-1].play)

    def identify_element(self, xml_element):
        """
        This non-constant method identifies which scene element is meant with the xml_element and
        returns a configured instance of it. If the scene element could not be identified, the game
        will be saved and crashes.
        """
        if xml_element.tag == "text":
            return TextElement(self, xml_element)
        elif xml_element.tag == "delay":
            return DelayElement(self, xml_element)
        elif xml_element.tag == "choice":
            return ChoiceElement(self, xml_element)
        elif xml_element.tag == "transfer":
            return TransferElement(self, xml_element)
        elif xml_element.tag == "changeState":
            return ChangeStateElement(self, xml_element)
        else:
            error_message = "Illegal scene element " + xml_element.tag + "! The game was saved!"
            QCoreApplication.instance().crash(error_message, True)

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

def generate_scene_element_path(scene, xml_root, path=None):
    """
    This function generates and returns a scene element path based upon an xml_root element for a
    scene. If you want to, you can give it a partly built path which will be extended.
    """
    if path is None:
        path = []
    for xml_element in list(xml_root):
        if len(path) > 0:
            previous_element = path[-1]
        else:
            previous_element = None

        path.append(scene.identify_element(xml_element))

        if previous_element is not None:
            previous_element.end.connect(path[-1].play)
    return path

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

class TransferElement(SceneElement):
    """
    This element transfers a subject to a target if it's possible.
    """
    def __init__(self, scene, xml_element):
        SceneElement.__init__(self, scene)
        self.subject_name = xml_element.get("subject", str())
        self.target_name = xml_element.get("target", str())

        no_subject_root = xml_element.find("noSubject")
        if no_subject_root is not None:
            self.no_subject_path = generate_scene_element_path(self.parent(), no_subject_root)
        else:
            self.no_subject_path = []

        no_target_root = xml_element.find("noTarget")
        if no_target_root is not None:
            self.no_target_path = generate_scene_element_path(self.parent(), no_target_root)
        else:
            self.no_target_path = []

        no_transfer_root = xml_element.find("noTransfer")
        if no_transfer_root is not None:
            self.no_transfer_path = generate_scene_element_path(self.parent(), no_transfer_root)
        else:
            self.no_transfer_path = []

    def play(self):
        app = QCoreApplication.instance()

        subject = app.findChild(Core.Entity, self.subject_name, Qt.FindChildrenRecursively)
        if subject is None:
            if len(self.no_subject_path) > 0:
                self.no_subject_path[0].play()
            else:
                self.end.emit()
                return

        if self.target_name == "None":
            target = None
        else:
            target = app.findChild(Core.Entity, self.target_name, Qt.FindChildrenRecursively)
            if target is None:
                if len(self.no_target_path) > 0:
                    self.no_target_path[0].play()
                else:
                    self.end.emit()
                    return

        if not subject.transfer(target):
            if len(self.no_transfer_path) > 0:
                self.no_subject_path[0].play()

        self.end.emit()

class ChangeStateElement(SceneElement):
    """
    This scene element changes an entitie's state to a given value.
    """
    def __init__(self, scene, xml_element):
        SceneElement.__init__(self, scene)
        self.subject_name = xml_element.get("subject", str())
        self.state = xml_element.get("state", str())
        self.value = int(xml_element.get("value", str()))

        no_subject_root = xml_element.find("noSubject")
        if no_subject_root is not None:
            self.no_subject_path = generate_scene_element_path(self.parent(), no_subject_root)
        else:
            self.no_subject_path = []

    def play(self):
        app = QCoreApplication.instance()

        subject = app.findChild(Core.Entity, self.subject_name, Qt.FindChildrenRecursively)
        if subject is None:
            if len(self.no_subject_path) > 0:
                self.no_subject_path[0].play()
            else:
                self.end.emit()
                return

        subject.set_state(self.state, self.value)

        self.end.emit()

class ChoiceElement(SceneElement):
    """
    This scene element gives the player a choice on how to proced in the dialogue.
    """
    def __init__(self, scene, xml_choice_root):
        SceneElement.__init__(self, scene)

        self.option_texts = []
        self.option_paths = []
        self.buttons = []
        self.down_button_index = -1

        for xml_option in xml_choice_root.findall("option"):
            self.option_texts.append(xml_option.get("text", str()))
            path = generate_scene_element_path(self.parent(), xml_option)
            path[-1].end.connect(self.end)
            self.option_paths.append(path)

    def play(self):
        if len(self.option_texts) == 0:
            self.end.emit()
        else:
            for text in self.option_texts:
                new_button = self.parent().get_player().get_window().add_option_button(text)
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
        text = self.option_texts[self.down_button_index]
        self.parent().get_player().get_window().show_text(text)
        self.parent().get_player().get_window().clear_command_row()
        self.option_paths[self.down_button_index][0].play()
