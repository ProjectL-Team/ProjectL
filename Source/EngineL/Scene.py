# coding=UTF-8
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
from PyQt5.QtCore import QObject, QCoreApplication, QEvent, pyqtSignal
from Source.EngineL import Core, Gameplay

class Scene(QObject):
    """
    This is the base class for scenes.
    """
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        player_name = Core.get_res_man().get_string("core.player.name")
        self.player = QCoreApplication.instance().findChild(Gameplay.Player, player_name)
        if self.player is None:
            raise Exception("Could not find the player!")
        self.window = self.player.get_window()

    def play(self):
        """
        This abstract method starts the scene. Subclasses should create all elements here and start
        the first one.
        """
        raise NotImplementedError

    def destruct(self):
        """
        This non-constant method destructs the scene and all of it's elements.
        """
        for child in self.children():
            try:
                child.end.disconnect()
            except TypeError:
                pass

            child.setParent(None)
        self.setParent(None)

class SceneElement(QObject):
    """
    Abstract base class for scene elements.
    """
    def __init__(self, parent=None, player=None, window=None, awaited_end=-1):
        QObject.__init__(self, parent)
        self.player = player
        self.window = window
        self.awaited_end = awaited_end

    def set_player(self, player):
        """
        This non-constant method sets our player
        """
        self.player = player

    def get_player(self):
        """
        This constant method returns our player
        """
        return self.player

    def set_window(self, window):
        """
        This non-constant method sets our window
        """
        self.window = window

    def get_window(self):
        """
        This constant method returns our window
        """
        return self.window

    def set_awaited_end(self, awaited_end):
        """
        This non-constant method sets our awaited end
        """
        self.awaited_end = awaited_end

    def get_awaited_end(self):
        """
        This constant method returns our awaited end
        """
        return self.awaited_end

    def play(self, end_number):
        """
        Starts the scene element's action. Subclasses need to override it.
        """
        raise NotImplementedError

    end = pyqtSignal(int)

class ClearCommandRowElement(SceneElement):
    """
    This scene element removes all widgets from the command row.
    """
    def __init__(self, parent=None, player=None, window=None, awaited_end=-1):
        SceneElement.__init__(self, parent, player, window, awaited_end)

    def play(self, end_number):
        if end_number == self.awaited_end:
            self.window.clear_command_row()
            self.end.emit(0)

class ShowCommandLineElement(SceneElement):
    """
    This scene element clears the command row and adds the command line again.
    """
    def __init__(self, parent=None, player=None, window=None, awaited_end=-1):
        SceneElement.__init__(self, parent, player, window, awaited_end)

    def play(self, end_number):
        if end_number == self.awaited_end:
            self.window.clear_command_row()
            self.window.add_command_line()
            self.end.emit(0)

class TextElement(SceneElement):
    """
    A scene element that prints a text when it is played.
    """
    def __init__(self, text=str(), parent=None, player=None, window=None, awaited_end=-1):
        SceneElement.__init__(self, parent, player, window, awaited_end)
        self.text = text

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

    def play(self, end_number):
        if end_number == self.awaited_end:
            self.window.show_text(self.text)
            self.end.emit(0)

class DelayElement(SceneElement):
    """
    This scene element waits for a predefined amount of time and fires it's end_0 when the time is
    over.
    """
    def __init__(self, parent=None, player=None, window=None, awaited_end=-1, time=0):
        SceneElement.__init__(self, parent, player, window, awaited_end)
        self.time = time
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

    def play(self, end_number):
        if end_number == self.awaited_end:
            self.timer_id = self.startTimer(self.time)

    def event(self, event):
        """
        This non-constant method checks for the timer to finish.
        """
        if event.type() == QEvent.Timer:
            self.killTimer(self.timer_id)
            self.end.emit(0)
            return True
        return QObject.event(self, event)

class OptionElement(SceneElement):
    """
    This scene element let's you add options the player can choose from.
    """
    def __init__(self, parent=None, player=None, window=None, awaited_end=-1):
        SceneElement.__init__(self, parent, player, window, awaited_end)
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
        text = Core.get_res_man().decode_string(text)
        self.window.show_command(text)
        self.end.emit(self.down_button_index)

