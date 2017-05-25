# coding=UTF-8
"""
All classes that extend the Core module to a playable game are found in the Gameplay module.

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
from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit
from PyQt5.QtWidgets import QMenuBar, QPushButton
from EngineL import Core

class ClientWindow(QMainWindow):
    """
    This is the game's main window. It abstracts the single elements of the window into single
    methods one can call and use.
    """

    return_pressed = pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)

        self.setObjectName("client_window")
        self.setWindowModality(Qt.NonModal)
        self.resize(800, 600)
        self.setDocumentMode(False)
        title = Core.get_res_man().get_string("core.windowTitle")
        self.setWindowTitle(title)

        central_widget = QWidget(self)
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)

        vertical_layout = QVBoxLayout(central_widget)
        vertical_layout.setObjectName("vertical_layout")
        central_widget.setLayout(vertical_layout)

        self.text_area = QTextEdit(central_widget)
        self.text_area.setReadOnly(True)
        self.text_area.setObjectName("text_area")
        vertical_layout.addWidget(self.text_area)

        self.command_row = QWidget(central_widget)
        self.command_row.setObjectName("command_row")
        vertical_layout.addWidget(self.command_row)

        command_row_layout = QHBoxLayout(self.command_row)
        command_row_layout.setObjectName("command_row_layout")
        command_row_layout.setContentsMargins(0, 0, 0, 0)
        command_row_layout.setSpacing(0)
        self.command_row.setLayout(command_row_layout)

        self.add_command_line()

        menu_bar = QMenuBar(self)
        menu_bar.setObjectName("menubar")
        self.setMenuBar(menu_bar)

    def get_text_area(self):
        """
        This constant method returns our text area widget.
        """
        return self.text_area

    def get_command_text(self, show_command=False, clear_prompt=False):
        """
        This non-constant method Returns the text of the command prompt widget. If show_command is
        True, it will also show the entered text in the text area and if clear_prompt is True, it
        will also clear the prompt.
        """
        if self.command_line is not None:
            text = self.command_line.text()
            if show_command and len(text) > 0:
                self.show_command(text)
            if clear_prompt:
                self.command_line.clear()
            return text
        else:
            return str()

    def show_text(self, text, emplace_res_strings=True, add_html_tags=True):
        """
        Thi non-constant method prints the given text in the text area as it's own paragraph.
        If emplace_res_strings is True (default), it will also decode resource string keys in
        it and if add_html_tags is True (default), it will add tags to the text that indicate that
        it should be handled as an HTML snippet.
        """
        self.text_area.setTextColor(QColor(0, 0, 0))
        if emplace_res_strings:
            text = Core.get_res_man().decode_string(text)
        if add_html_tags:
            text = '<html><body>' + text + '</body></html>'
        self.text_area.append(text)

    def show_command(self, text):
        """
        This non-constant method shows the given text to the user, but displays it in a grey color
        and adds a "> " to show that the given text is a command or something else the user said or
        did.
        """
        self.text_area.setTextColor(QColor(125, 125, 125))
        self.text_area.append("> " + text)

    def clear_command_row(self):
        """
        This non-constant method removes all widgets from our command row.
        """
        while self.command_row.layout().count() > 0:
            self.command_row.layout().takeAt(0).widget().setParent(None)

    def add_command_line(self):
        """
        This non-constant method adds a command line to our command row.
        """
        self.command_line = QLineEdit(self.command_row)
        child_number = len(self.command_row.children())
        self.command_line.setObjectName("command_line_" + str(child_number))
        self.command_row.layout().addWidget(self.command_line)
        self.command_line.returnPressed.connect(self.return_pressed)

    def add_option_button(self, text):
        """
        This non-constant method adds an option button with the given text to the command row and
        returns it. The text may contain unresolved resource string keys as they will be resolved
        inside this method.
        """
        text = Core.get_res_man().decode_string(text)
        button = QPushButton(text, self.command_row)
        child_number = len(self.command_row.children())
        button.setObjectName("option_button_" + str(child_number))
        self.command_row.layout().addWidget(button)
        return button

    def closeEvent(self, event):
        """
        This overriden non-constant method gets called when the window is closed and saves the game.
        """
        QCoreApplication.instance().save_world()
        event.accept()

class GameplayParser(QObject):
    """
    The GameplayParser takes entered commands and interprets them.
    """

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.setObjectName("GameplayParser")
        self.window = parent.get_window()
        self.split_text = []
        self.used_words = 0

    def command_entered(self):
        """
        This non-constant method gets called when a command was entered and starts the parsing
        process.
        """
        self.window = self.parent().get_window()

        self.split_text = self.window.get_command_text(True, True).split()

        self.filter_ignored_words()

        self.identify_command()

    def filter_ignored_words(self):
        """
        This non-constant method gets all ignored words from the resources manager and removes
        every appearence from our split_text.
        """
        parsers_root = Core.get_res_man().get_element("core.gameplayParser")
        ignored_words = []
        for word in parsers_root.findall("ignoreWord"):
            ignored_words.append(word.text)

        index = 0
        while index < len(self.split_text):
            if self.split_text[index] in ignored_words:
                del self.split_text[index]
            else:
                index += 1

    def identify_command(self):
        """
        This non-constant method identifies and executes the previously read command.
        """
        string_collection = Core.get_res_man().get_element("core.gameplayParser")

        if len(self.split_text) == 0:
            pass
        elif self.compare_commands_with_text(string_collection.find("lookAt").findall("command")):
            self.exec_look_at()
        elif self.compare_commands_with_text(string_collection.find("walkTo").findall("command")):
            self.exec_walk_to()
        elif self.compare_commands_with_text(string_collection.find("pickUp").findall("command")):
            self.exec_pick_up()
        elif self.compare_commands_with_text(string_collection.find("drop").findall("command")):
            self.exec_drop()
        elif self.compare_commands_with_text(string_collection.find("combine").findall("command")):
            self.exec_combine()
        elif self.compare_commands_with_text(string_collection.find("talk").findall("command")):
            self.exec_talk()
        else:
            self.exec_invalid_command()

    def compare_commands_with_text(self, commands):
        """
        This non-constant method iterates through the given etree elements (commands) and compares
        their text with the beginning of our split_text. If one of those commands is equal to the
        beginning of our split_text, it returns True and False if not.
        """
        for command in commands:
            command = command.text.split()
            if len(command) > len(self.split_text):
                continue
            matches = True
            for i in range(0, len(command)):
                if self.split_text[i] != command[i]:
                    matches = False
            if matches:
                self.used_words = len(command)
                return True
        return False

    def get_argument(self):
        """
        This constant method returns a list containing all words that weren't used before, which
        is the argument of our command.
        """
        if len(self.split_text) == self.used_words:
            return []
        else:
            return self.split_text[self.used_words:len(self.split_text)]

    def get_argument_as_string(self):
        """
        This constant method takes the return value of get_argument and patches it into one string,
        which resembles the argument before it was split.
        """
        if len(self.split_text) == self.used_words:
            return str()
        else:
            argument = str()
            raw_argument = self.get_argument()
            for word in raw_argument[:-1]:
                argument += word + " "
            argument += raw_argument[-1]
            return argument

    def exec_invalid_command(self):
        """
        This non-constant method shows the player that he/she had entered an invalid command.
        """
        self.window.show_text("${core.gameplayParser.invalidCommandMessage}")

    def exec_look_at(self):
        """
        This non-constant method executes the "look at" command: First, it finds out which entity
        is meant, which can be the place we are at, another entity at our place or even ourselves!
        If it couldn't find the requested entity, it the user so. Then, it receives the description
        of the targeted entity and displays it.
        """
        target_name = self.get_argument_as_string()
        place = self.parent().parent()
        keyword_place = Core.get_res_man().get_string("core.gameplayParser.lookAt.keyword.place")
        key_inventory = "core.gameplayParser.lookAt.keyword.inventory"
        keyword_inventory = Core.get_res_man().get_string(key_inventory)

        if len(target_name) == 0:
            self.window.show_text(place.get_description())
        elif target_name == keyword_place or target_name == place.objectName():
            self.window.show_text(place.get_description())
        elif target_name == keyword_inventory:
            self.window.show_text(self.parent().generate_inventory_list(empty_note=True) + ".")
        else:
            target = place.findChild(Core.Entity, target_name)
            if target is None:
                self.window.show_text("${core.gameplayParser.invalidTargetMessage}")
            else:
                self.window.show_text(target.get_description())

    def exec_walk_to(self):
        """
        This non-constant method executes the "walk to" command, which is done by calling the
        Entity's move_to_place method. If this failed, it tells the user so.
        """
        target_name = self.get_argument_as_string()
        if not self.parent().move_to_place(target_name):
            self.window.show_text("${core.gameplayParser.invalidTargetMessage}")

    def exec_pick_up(self):
        """
        This non-constant method executes the "pick up" command, which is done by calling the
        Entity's pick_up_entity method. If this failed, it tells the user so.
        """
        target_name = self.get_argument_as_string()
        if not self.parent().pick_up_entity(target_name):
            self.window.show_text("${core.gameplayParser.invalidTargetMessage}")

    def exec_drop(self):
        """
        This non-constant method executes the "drop" command, which is done by calling the
        Entity's lay_down_entity method. If this failed, it tells the user so.
        """
        target_name = self.get_argument_as_string()
        if not self.parent().lay_down_entity(target_name):
            self.window.show_text("${core.gameplayParser.invalidTargetMessage}")

    def exec_combine(self):
        """
        This non-constant method executes the "combine" command: First, it searches for the
        argument separator in our argument, then it extracts the two arguments from the list and
        connects them into two strings. The next step is that it tries the find the entities with
        the given names and to lookup the class of combination result. When this is all done, it
        creates the product and deletes the old entities, in this order. If anything went wrong in
        this process, it tells the user that he/she messed up and ends without changing anything.
        """
        # Get the whole argument text
        argument = self.get_argument()

        # Find the combination argument separator, usually 'with'.
        separator = Core.get_res_man().get_string("core.gameplayParser.combine.argumentSeparator")
        separator_position = -1
        for i in range(0, len(argument)):
            if argument[i] == separator:
                separator_position = i
                break

        arg_a = None
        arg_b = None
        arg_a_name = str()
        arg_b_name = str()
        if separator_position == -1:
            # If there is only one argument, patch it's name together
            for word in argument[0:-1]:
                arg_a_name += word + " "
            arg_a_name += argument[-1]
        else:
            # If there are two arguments, patch both names together
            for word in argument[0:separator_position-1]:
                arg_a_name += word + " "
            arg_a_name += argument[separator_position-1]

            for word in argument[separator_position+1: len(argument)-1]:
                arg_b_name += word + " "
            arg_b_name += argument[len(argument)-1]

            # Find entity B, which is only if an entity B is mentioned
            arg_b = self.parent().parent().findChild(Core.Entity, arg_b_name)
            if arg_b is None:
                text = "${core.gameplayParser.invalidTargetMessage}"
                self.window.show_text(text)
                return

        # Find entity A, which is always needed.
        arg_a = self.parent().parent().findChild(Core.Entity, arg_a_name)
        if arg_a is None:
            text = "${core.gameplayParser.invalidTargetMessage}"
            self.window.show_text(text)
            return

        # Call the player's "use" method.
        if not arg_a.on_used(self.parent(), arg_b):
            text = "${core.gameplayParser.combine.invalidCombination}"
            self.window.show_text(text)
            return

    def exec_talk(self):
        """
        This non-constant method executes the "talk" command by calling the talk_to method. If
        something gets wrong, it tells the user so.
        """
        target_name = self.get_argument_as_string()

        if not self.parent().talk_to(target_name):
            self.window.show_text("${core.gameplayParser.invalidTargetMessage}")

class Player(Core.Entity):
    """
    The entity that represents the player in the game's world.
    """

    def __init__(self, parent=None):
        Core.Entity.__init__(self, parent)
        self.setObjectName(Core.get_res_man().get_string("core.player.name"))
        self.description = "${core.player.description}"

        self.window = ClientWindow()
        self.window.show()

        self.gameplay_parser = GameplayParser(self)

        self.window.return_pressed.connect(self.gameplay_parser.command_entered)

    def get_window(self):
        """
        This constant method returns our window.
        """
        return self.window

    def get_gameplay_parser(self):
        """
        This constant method returns our gameplay parser.
        """
        return self.gameplay_parser

def register_entity_classes(app):
    """
    This function registers all of our new Entity classes to the given application instance.
    """
    app.register_entity_classes([Player])
