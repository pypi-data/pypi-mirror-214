from __future__ import annotations
from io import TextIOWrapper

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QLabel, QGroupBox, QTextEdit, QLineEdit, QApplication, QWidget,\
                            QHBoxLayout, QVBoxLayout, QCheckBox, QComboBox, QDesktopWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from HarmonyDecoder.rules import rule_manager
from HarmonyDecoder.program import program
from HarmonyDecoder.strdecoder import str_symbol
from HarmonyDecoder.scale import scale, modes
from HarmonyDecoder.logger import logger
from datetime import datetime
from HarmonyDecoder.drawing import drawing
from tkinter import filedialog

import sys

arial_12:QFont = QFont('Arial', 12)
arial_24:QFont = QFont('Arial', 24)

class ui_solution(QWidget):
    def __init__(self, parent:ui_program) -> None:
        super().__init__()

        self.__parent:ui_program = parent        
        self.__drawing:drawing = drawing(self.__parent.program.tonation)
        self.__solutions:tuple[list[function]] = parent.program.solution

        self.setWindowTitle("Harmony decoder - solutions")
        self.setGeometry(0, 0, 300, 400)
        self.setWindowIcon(QtGui.QIcon('Images/Icon.png'))

        self.__title_label:QLabel = QLabel("Solutions")
        self.__subtitle_label:QLabel = QLabel(f"{len(self.__solutions)} solutions were generated.")
        self.__solution_label:QLabel = QLabel("Choose solution:")

        self.__solution_combo:QComboBox = QComboBox()
        
        self.__draw_solution_button:QPushButton = QPushButton("Draw")
        self.__cancel_button:QPushButton = QPushButton("Cancel")
        self.__save_button:QPushButton = QPushButton("Save")

        for item in range(len(self.__solutions)):
            self.__solution_combo.addItem(str(item))

        self.__up_box:QGroupBox = QGroupBox()
        self.__up_box.setLayout(QVBoxLayout())
        self.__up_box.layout().addWidget(self.__title_label)
        self.__up_box.layout().addWidget(self.__subtitle_label)

        self.__solution_box:QGroupBox = QGroupBox("Choose solution")
        self.__solution_box.setLayout(QHBoxLayout())
        self.__solution_box.layout().addWidget(self.__draw_solution_button)
        self.__solution_box.layout().addWidget(self.__solution_combo)
        self.__solution_box.setMaximumHeight(100)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.__up_box)
        self.layout().addWidget(self.__solution_box)
        self.layout().addWidget(self.__save_button)
        self.layout().addWidget(self.__cancel_button)

        self.__title_label.setFont(arial_24)
        self.__subtitle_label.setFont(arial_12)
        self.__solution_label.setFont(arial_12)

        self.__draw_solution_button.setFont(arial_12)
        self.__cancel_button.setFont(arial_12)
        self.__save_button.setFont(arial_12)

        self.__title_label.setAlignment(Qt.AlignCenter)
        self.__subtitle_label.setAlignment(Qt.AlignCenter)

        self.__draw_solution_button.clicked.connect(self.__draw)
        self.__cancel_button.clicked.connect(self.closeEvent)
        self.__save_button.clicked.connect(self.__save)

# public:
    def closeEvent(self, event: QCloseEvent) -> None:
        self.__parent.close_solution()

# private:
    def __draw(self) -> None:        
        self.__drawing.clear()

        if self.__parent.program.task == []:
            self.__parent.program.program_logger.log("Cannot draw empty solution.")
            return
        
        if self.__parent.program.solution != ():
            solution:list[function] = self.__solutions[int(self.__solution_combo.currentText())]
            index:int = 0

            for function in solution:
                self.__drawing.draw_function(function, x=index)
                index += 1

        self.__parent.program.program_logger.log("Drawing solution...")

        self.__drawing.draw_staff()

        self.__parent.program.program_logger.log("Solution drawn...")
        self.__parent.program.program_logger.log("Showing  solution...")

        self.__drawing.show()

        self.__parent.program.program_logger.log("Solution shown.")

    def __save(self) -> None:
        path:str = filedialog.askdirectory(
            initialdir=self.__parent.last_save_directory,
            mustexist=True,
            title="Choose save directory"
        )

        if len(path) >= 1:
            filename:str = f"{datetime.now().time().strftime('%H_%M_%S')}_Solution_{self.__solution_combo.currentText()}.png"
            self.__drawing.save(f"{path}/{filename}")
            self.__parent.last_save_directory = path
            self.__parent.program.program_logger.log(f"File {filename} saved to {path}")
        else:
            self.__parent.program.program_logger.log("Saving canceled.")


class ui_rules(QWidget):
    def __init__(self, rules:rule_manager, parent:ui_program) -> None:
        super().__init__()

        self.__parent:ui_program = parent
        self.rules:rule_manager = rules

        self.setWindowTitle("Harmony decoder - rules")
        self.setGeometry(0, 0, 300, 400)
        self.setWindowIcon(QtGui.QIcon('Images/Icon.png'))

        self.__voice_crossing_checkbox:QCheckBox = QCheckBox("Voice crossing checking")
        self.__parallel_fifth_checkbox:QCheckBox = QCheckBox("Parallel fifths checking")
        self.__parallel_octave_checkbox:QCheckBox = QCheckBox("Parallel octaves checking")
        self.__one_direction_checkbox:QCheckBox = QCheckBox("One direction checking")
        self.__seventh_down_checkbox:QCheckBox = QCheckBox("Seventh down checking")
        self.__third_up_checkbox:QCheckBox = QCheckBox("Third up checking")
        self.__ninth_down_checkbox:QCheckBox = QCheckBox("Ninth down checking")
        self.__fifth_on_one_checkbox:QCheckBox = QCheckBox("Fifth on the first beat checking")
        self.__ninth_as_root_checkbox:QCheckBox = QCheckBox("Ninth as root checking")

        self.__save_button:QPushButton = QPushButton("Save and quit")
        self.__cancel_button:QPushButton = QPushButton("Cancel")

        self.__save_button.setFont(arial_12)
        self.__cancel_button.setFont(arial_12)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.__voice_crossing_checkbox)
        self.layout().addWidget(self.__parallel_fifth_checkbox)
        self.layout().addWidget(self.__parallel_octave_checkbox)
        self.layout().addWidget(self.__one_direction_checkbox)
        self.layout().addWidget(self.__seventh_down_checkbox)
        self.layout().addWidget(self.__third_up_checkbox)
        self.layout().addWidget(self.__ninth_down_checkbox)
        self.layout().addWidget(self.__fifth_on_one_checkbox)
        self.layout().addWidget(self.__ninth_as_root_checkbox)
        self.layout().addWidget(self.__save_button)
        self.layout().addWidget(self.__cancel_button)

        self.__save_button.clicked.connect(self.__save_and_quit)
        self.__cancel_button.clicked.connect(self.__cancel)

        self.__get_state()

# public:
    def closeEvent(self, event: QCloseEvent) -> None:        
        self.__parent.refresh_rules()
        self.__parent.show()

# private:
    def __save_and_quit(self) -> None:
        checkboxes:list[QCheckBox] = [
            self.__voice_crossing_checkbox,
            self.__parallel_fifth_checkbox,
            self.__parallel_octave_checkbox,
            self.__one_direction_checkbox,
            self.__seventh_down_checkbox,
            self.__third_up_checkbox,
            self.__ninth_down_checkbox,
            self.__fifth_on_one_checkbox,
            self.__ninth_as_root_checkbox
        ]

        for index in range(len(checkboxes)):
            if checkboxes[index].isChecked():
                self.rules.active_rules[index].active = True
            else:
                self.rules.active_rules[index].active = False

        self.close()

    def __cancel(self) -> None:
        self.close()

    def __get_state(self) -> None:
        checkboxes:list[QCheckBox] = [
            self.__voice_crossing_checkbox,
            self.__parallel_fifth_checkbox,
            self.__parallel_octave_checkbox,
            self.__one_direction_checkbox,
            self.__seventh_down_checkbox,
            self.__third_up_checkbox,
            self.__ninth_down_checkbox,
            self.__fifth_on_one_checkbox,
            self.__ninth_as_root_checkbox
        ]

        for index in range(len(checkboxes)):
            if self.rules.active_rules[index].active:
                checkboxes[index].setChecked(True)
            else:
                checkboxes[index].setChecked(False)


class ui_function_creator(QWidget):
    def __init__(self, parent:ui_program) -> None:
        super().__init__()

        self.__parent:ui_program = parent

        self.__major_symbols:tuple[str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str] = \
            ("T", "Sii", "mSii", "Tiii", "mDiii", "Diii", "S", "mS", "D", "mD", "Tvi", "Svi", "mSvi", "Dvii", "Svii", "mDvii", "mSvii")
        self.__minor_symbols:tuple[str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str] = \
            ("mT", "Sii", "mSii", "mTiii", "mDiii", "Diii", "S", "mS", "D", "mD", "mTvi", "Svi", "mSvi", "Dvii", "Svii", "mDvii", "mSvii")
        self.__addable_symbols:tuple[str, str, str, str, str, str, str] = ("6", "6>", "7>", "7", "7<", "9>", "9")
        self.__deletable_symbols:tuple[str, str] = ("1", "5")
        self.__alerable_symbols:tuple[str, str, str] = ("1", "3", "5")
        self.__alterations:tuple[str, str] = ("#", "b")

        self.__symbol:str = ""
        self.__added:str = ""
        self.__deleted:str = ""
        self.__altered1:str = ""
        self.__altered2:str = ""
        self.__altered3:str = ""
        self.__altered4:str = ""
        self.__suspended:str = ""
        self.__root:str = ""
        self.__position:str = ""        

        self.setWindowTitle("Harmony decoder - function creator")
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setGeometry(0, 0, 600, 800)
        self.setWindowIcon(QtGui.QIcon('Images/Icon.png'))

        self.__raw_label:QLabel = QLabel("Raw input (if you know the format):")
        self.__symbols_label:QLabel = QLabel("Symbols:")
        self.__title_label:QLabel = QLabel("Function Creator")
        self.__addable_label:QLabel = QLabel("Addable:")
        self.__deletable_label:QLabel = QLabel("Deletable:")
        self.__sign_label_1:QLabel = QLabel("Altered note 1:")
        self.__sign_label_2:QLabel = QLabel("Altered note 2:")
        self.__sign_label_3:QLabel = QLabel("Altered note 3:")
        self.__sign_label_4:QLabel = QLabel("Altered note 4:")
        self.__position_label:QLabel = QLabel("Position:")
        self.__root_label:QLabel = QLabel("Root:")
        self.__current_label:QLabel = QLabel("Current:")

        self.__add_button:QPushButton = QPushButton("Create and add")
        self.__cancel_button:QPushButton = QPushButton("Cancel")
        self.__add_raw_button:QPushButton = QPushButton("Create and add")
        
        self.__symbols_combo:QComboBox = QComboBox()
        self.__addable_combo:QComboBox = QComboBox()
        self.__deletable_combo:QComboBox = QComboBox()
        self.__root_combo:QComboBox = QComboBox()
        self.__position_combo:QComboBox = QComboBox()

        self.__alter_combo_1:QComboBox = QComboBox()
        self.__alter_combo_2:QComboBox = QComboBox()
        self.__alter_combo_3:QComboBox = QComboBox()
        self.__alter_combo_4:QComboBox = QComboBox()

        self.__sign_combo_1:QComboBox = QComboBox()
        self.__sign_combo_2:QComboBox = QComboBox()
        self.__sign_combo_3:QComboBox = QComboBox()
        self.__sign_combo_4:QComboBox = QComboBox()        

        self.__raw_text:QLineEdit = QLineEdit("T^/++--**==")
        self.__current_text:QLineEdit = QLineEdit()

        self.__current_text.setReadOnly(True)

        self.__add_button.setFont(arial_12)
        self.__cancel_button.setFont(arial_12)
        self.__add_raw_button.setFont(arial_12)

        if self.__parent.program.tonation.mode == "major":
            for item in self.__major_symbols:
                self.__symbols_combo.addItem(item)
        else:
            for item in self.__minor_symbols:
                self.__symbols_combo.addItem(item)

        self.__addable_combo.addItem("")

        for item in self.__addable_symbols:
            self.__addable_combo.addItem(item)

        self.__deletable_combo.addItem("")

        for item in self.__deletable_symbols:
            self.__deletable_combo.addItem(item)
        
        for component in [self.__alter_combo_1, self.__alter_combo_2, self.__alter_combo_3, self.__alter_combo_4]:
            component.addItem("")

            for item in self.__alerable_symbols:
                component.addItem(item)

        for component in [self.__sign_combo_1, self.__sign_combo_2, self.__sign_combo_3, self.__sign_combo_4]:
            component.addItem("")

            for item in self.__alterations:
                component.addItem(item)

        self.__position_combo.addItem("")

        for item in ["1", "3", "5", "7", "9"]:
            self.__position_combo.addItem(item)

        self.__root_combo.addItem("")

        for item in ["1", "3", "5", "7"]:
            self.__root_combo.addItem(item)

        self.__raw_label.setFont(arial_12)
        self.__deletable_label.setFont(arial_12)
        self.__addable_label.setFont(arial_12)
        self.__symbols_label.setFont(arial_12)
        self.__sign_label_1.setFont(arial_12)
        self.__sign_label_2.setFont(arial_12)
        self.__sign_label_3.setFont(arial_12)
        self.__sign_label_4.setFont(arial_12)
        self.__position_label.setFont(arial_12)
        self.__root_label.setFont(arial_12)
        self.__current_label.setFont(arial_12)

        self.__title_label.setFont(arial_24)
        self.__title_label.setAlignment(Qt.AlignCenter)

        self.__sign_box_1:QGroupBox = QGroupBox()
        self.__sign_box_1.setLayout(QHBoxLayout())
        self.__sign_box_1.layout().addWidget(self.__sign_label_1)
        self.__sign_box_1.layout().addWidget(self.__alter_combo_1)
        self.__sign_box_1.layout().addWidget(self.__sign_combo_1)

        self.__sign_box_2:QGroupBox = QGroupBox()
        self.__sign_box_2.setLayout(QHBoxLayout())
        self.__sign_box_2.layout().addWidget(self.__sign_label_2)
        self.__sign_box_2.layout().addWidget(self.__alter_combo_2)
        self.__sign_box_2.layout().addWidget(self.__sign_combo_2)

        self.__sign_box_3:QGroupBox = QGroupBox()
        self.__sign_box_3.setLayout(QHBoxLayout())
        self.__sign_box_3.layout().addWidget(self.__sign_label_3)
        self.__sign_box_3.layout().addWidget(self.__alter_combo_3)
        self.__sign_box_3.layout().addWidget(self.__sign_combo_3)

        self.__sign_box_4:QGroupBox = QGroupBox()
        self.__sign_box_4.setLayout(QHBoxLayout())
        self.__sign_box_4.layout().addWidget(self.__sign_label_4)
        self.__sign_box_4.layout().addWidget(self.__alter_combo_4)
        self.__sign_box_4.layout().addWidget(self.__sign_combo_4)

        self.__all_signs_box:QGroupBox = QGroupBox()
        self.__all_signs_box.setLayout(QVBoxLayout())
        self.__all_signs_box.layout().addWidget(self.__sign_box_1)
        self.__all_signs_box.layout().addWidget(self.__sign_box_2)
        self.__all_signs_box.layout().addWidget(self.__sign_box_3)
        self.__all_signs_box.layout().addWidget(self.__sign_box_4)

        self.__small_raw_box:QGroupBox = QGroupBox()
        self.__small_raw_box.setLayout(QHBoxLayout())
        self.__small_raw_box.layout().addWidget(self.__raw_label)
        self.__small_raw_box.layout().addWidget(self.__raw_text)

        self.__raw_box:QGroupBox = QGroupBox()
        self.__raw_box.setLayout(QVBoxLayout())
        self.__raw_box.layout().addWidget(self.__small_raw_box)
        self.__raw_box.layout().addWidget(self.__add_raw_button)        

        self.__symbols_box:QGroupBox = QGroupBox()
        self.__symbols_box.setLayout(QHBoxLayout())
        self.__symbols_box.layout().addWidget(self.__symbols_label)
        self.__symbols_box.layout().addWidget(self.__symbols_combo)

        self.__addable_box:QGroupBox = QGroupBox()
        self.__addable_box.setLayout(QHBoxLayout())
        self.__addable_box.layout().addWidget(self.__addable_label)
        self.__addable_box.layout().addWidget(self.__addable_combo)

        self.__deletable_box:QGroupBox = QGroupBox()
        self.__deletable_box.setLayout(QHBoxLayout())
        self.__deletable_box.layout().addWidget(self.__deletable_label)
        self.__deletable_box.layout().addWidget(self.__deletable_combo)

        self.__buttons_box:QGroupBox = QGroupBox()
        self.__buttons_box.setLayout(QHBoxLayout())
        self.__buttons_box.layout().addWidget(self.__add_button)
        self.__buttons_box.layout().addWidget(self.__cancel_button)

        self.__root_box:QGroupBox = QGroupBox()
        self.__root_box.setLayout(QHBoxLayout())
        self.__root_box.layout().addWidget(self.__root_label)
        self.__root_box.layout().addWidget(self.__root_combo)

        self.__position_box:QGroupBox = QGroupBox()
        self.__position_box.setLayout(QHBoxLayout())
        self.__position_box.layout().addWidget(self.__position_label)
        self.__position_box.layout().addWidget(self.__position_combo)

        self.__current_box:QGroupBox = QGroupBox()
        self.__current_box.setLayout(QHBoxLayout())
        self.__current_box.layout().addWidget(self.__current_label)
        self.__current_box.layout().addWidget(self.__current_text)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.__title_label)
        self.layout().addWidget(self.__raw_box)
        self.layout().addWidget(self.__root_box)
        self.layout().addWidget(self.__position_box)
        self.layout().addWidget(self.__symbols_box)
        self.layout().addWidget(self.__addable_box)
        self.layout().addWidget(self.__deletable_box)
        self.layout().addWidget(self.__all_signs_box)
        self.layout().addWidget(self.__current_box)
        self.layout().addWidget(self.__buttons_box)

        self.__cancel_button.clicked.connect(self.__cancel)
        self.__add_raw_button.clicked.connect(self.__add_raw_symbol)
        self.__add_button.clicked.connect(self.__add_symbol)

        self.__alter_combo_1.activated[str].connect(self.__set_alterated_1)
        self.__alter_combo_2.activated[str].connect(self.__set_alterated_2)
        self.__alter_combo_3.activated[str].connect(self.__set_alterated_3)
        self.__alter_combo_4.activated[str].connect(self.__set_alterated_4)

        self.__sign_combo_1.activated[str].connect(self.__set_alterated_1)
        self.__sign_combo_2.activated[str].connect(self.__set_alterated_2)
        self.__sign_combo_3.activated[str].connect(self.__set_alterated_3)
        self.__sign_combo_4.activated[str].connect(self.__set_alterated_4)

        self.__symbols_combo.activated[str].connect(self.__set_symbol)
        self.__addable_combo.activated[str].connect(self.__set_additional)
        self.__deletable_combo.activated[str].connect(self.__set_deleted)

        self.__position_combo.activated[str].connect(self.__set_position)
        self.__root_combo.activated[str].connect(self.__set_root)

        self.__set_symbol()
        self.__set_deleted()
        self.__set_additional()
        self.__set_alterated_1()
        self.__set_alterated_2()
        self.__set_alterated_3()
        self.__set_alterated_4()

# private:
    def __add_raw_symbol(self) -> None:
        if len(self.__raw_text.text()) >= 11:
            symbol = self.__raw_text.text()
        else:
            return

        try:
            to_add:str_symbol = str_symbol(symbol)  

            self.__parent.program.add_to_task(to_add)
            self.__cancel_button.click()          
        except ValueError:
            self.__parent.program.program_logger.log("Parser error")
            return

    def __add_symbol(self) -> None:
        try:
            symbol:str = self.__get_current_state()
            to_add:str_symbol = str_symbol(symbol)

            self.__parent.program.add_to_task(to_add)
            self.__cancel_button.click()
        except ValueError:
            self.__parent.program.program_logger.log("Parse error")
            return

    def __set_symbol(self) -> None:
        self.__symbol = self.__symbols_combo.currentText()
        self.__refresh_current()

    def __set_additional(self) -> None:
        self.__added = self.__addable_combo.currentText()
        self.__refresh_current()

    def __set_deleted(self) -> None:
        self.__deleted = self.__deletable_combo.currentText()
        self.__refresh_current()

    def __set_alterated_1(self) -> None:
        self.__altered1 = f"{self.__alter_combo_1.currentText()}{self.__sign_combo_1.currentText()}"
        self.__refresh_current()

    def __set_alterated_2(self) -> None:
        self.__altered2 = f"{self.__alter_combo_2.currentText()}{self.__sign_combo_2.currentText()}"
        self.__refresh_current()

    def __set_alterated_3(self) -> None:
        self.__altered3 = f"{self.__alter_combo_3.currentText()}{self.__sign_combo_3.currentText()}"
        self.__refresh_current()

    def __set_alterated_4(self) -> None:
        self.__altered4 = f"{self.__alter_combo_4.currentText()}{self.__sign_combo_4.currentText()}"
        self.__refresh_current()

    def __set_root(self) -> None:
        self.__root = self.__root_combo.currentText()
        self.__refresh_current()

    def __set_position(self) -> None:
        self.__position = self.__position_combo.currentText()
        self.__refresh_current()

    def __cancel(self) -> None:
        self.__parent.show()
        self.__parent.refresh_functions()
        self.close()

    def __refresh_current(self) -> None:
        self.__current_text.setText(self.__get_current_state())

    def __get_current_state(self) -> str:
        symbol:str = f"{self.__symbol}^{self.__position}/{self.__root}+{self.__added}+-{self.__deleted}-*"

        if self.__altered1 != "":
            symbol += self.__altered1 + ","

        if self.__altered2 != "":
            symbol += self.__altered2 + ","

        if self.__altered3 != "":
            symbol += self.__altered3 + ","

        if self.__altered4 != "":
            symbol += self.__altered4 + ","

        if symbol[-1] == ',':
            symbol = symbol[:-1]

        symbol += '*=='

        return symbol


class ui_program(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle("Harmony decoder")
        self.setGeometry(0, 0, 600, 400)       
        self.showMaximized()
        self.setWindowIcon(QtGui.QIcon('Images/Icon.png'))

        self.__title_label:QLabel = QLabel("Workspace")
        self.__rules_label:QLabel = QLabel("Active rules:")
        self.__tonation_label:QLabel = QLabel("Tonation:")
        self.__measure_length_label:QLabel = QLabel("Measure length:")
        self.__logs_label:QLabel = QLabel("Logs:")

        self.__tonation_combo:QComboBox = QComboBox()
        self.__mode_combo:QComboBox = QComboBox()
        self.__measure_length_combo:QComboBox = QComboBox()

        self.__rules_text:QTextEdit = QTextEdit()
        self.__input_text:QTextEdit = QTextEdit()
        self.__logs_text:QTextEdit = QTextEdit()

        self.__solve_button:QPushButton = QPushButton("Solve")
        self.__add_function_button:QPushButton = QPushButton("Add function")
        self.__show_rules_button:QPushButton = QPushButton("Show rules")
        self.__clear_logs_button:QPushButton = QPushButton("Clear logs")
        self.__clear_functions_button:QPushButton = QPushButton("Clear functions")
        self.__read_from_file_button:QPushButton = QPushButton("Load task")

        self.__rules_label.setFont(arial_12)
        self.__tonation_label.setFont(arial_12)
        self.__measure_length_label.setFont(arial_12)
        self.__logs_label.setFont(arial_12)

        self.__logs_label.setMaximumHeight(30)

        self.__title_label.setFont(arial_24)
        self.__title_label.setAlignment(Qt.AlignCenter)

        self.__input_text.setReadOnly(True)
        self.__rules_text.setReadOnly(True)
        self.__logs_text.setReadOnly(True)

        self.__logs_text.setMaximumHeight(200)

        self.__show_rules_button.setFont(arial_12)
        self.__solve_button.setFont(arial_12)
        self.__add_function_button.setFont(arial_12)
        self.__clear_logs_button.setFont(arial_12)
        self.__clear_functions_button.setFont(arial_12)
        self.__read_from_file_button.setFont(arial_12)

        for item in ('C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'Fb', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B', 'B#', 'Cb'):
            self.__tonation_combo.addItem(item)
        
        for item in modes:
            self.__mode_combo.addItem(item)

        for item in ['2', '3', '4', '6']:
            self.__measure_length_combo.addItem(item)

        self.__tonation_box:QGroupBox = QGroupBox()
        self.__tonation_box.setLayout(QHBoxLayout())
        self.__tonation_box.layout().addWidget(self.__tonation_label)
        self.__tonation_box.layout().addWidget(self.__tonation_combo)
        self.__tonation_box.layout().addWidget(self.__mode_combo)

        self.__measure_length_box:QGroupBox = QGroupBox()
        self.__measure_length_box.setLayout(QHBoxLayout())       
        self.__measure_length_box.layout().addWidget(self.__measure_length_label)
        self.__measure_length_box.layout().addWidget(self.__measure_length_combo) 

        self.__settings_box:QGroupBox = QGroupBox()
        self.__settings_box.setLayout(QVBoxLayout())
        self.__settings_box.layout().addWidget(self.__tonation_box)
        self.__settings_box.layout().addWidget(self.__measure_length_box)

        self.__right_box:QGroupBox = QGroupBox()
        self.__right_box.setLayout(QVBoxLayout())
        self.__right_box.layout().addWidget(self.__rules_label)
        self.__right_box.layout().addWidget(self.__rules_text)
        self.__right_box.layout().addWidget(self.__show_rules_button)
        self.__right_box.layout().addWidget(self.__settings_box)

        self.__left_box:QGroupBox = QGroupBox()
        self.__left_box.setLayout(QVBoxLayout())
        self.__left_box.layout().addWidget(self.__add_function_button)
        self.__left_box.layout().addWidget(self.__read_from_file_button)
        self.__left_box.layout().addWidget(self.__input_text)
        self.__left_box.layout().addWidget(self.__solve_button)
        self.__left_box.layout().addWidget(self.__clear_functions_button)

        self.__down_box:QGroupBox = QGroupBox()
        self.__down_box.setLayout(QHBoxLayout())
        self.__down_box.layout().addWidget(self.__left_box)
        self.__down_box.layout().addWidget(self.__right_box)

        self.__logs_box:QGroupBox = QGroupBox()
        self.__logs_box.setLayout(QVBoxLayout())
        self.__logs_box.layout().addWidget(self.__logs_label)
        self.__logs_box.layout().addWidget(self.__logs_text)
        self.__logs_box.layout().addWidget(self.__clear_logs_button)
        self.__logs_box.setMaximumHeight(270)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.__title_label)
        self.layout().addWidget(self.__down_box)
        self.layout().addWidget(self.__logs_box)

        self.__show_rules_button.clicked.connect(self.__show_rules)
        self.__solve_button.clicked.connect(self.__solve)
        self.__add_function_button.clicked.connect(self.__add_function)
        self.__clear_logs_button.clicked.connect(self.__clear_logs)
        self.__clear_functions_button.clicked.connect(self.__clear_functions)
        self.__read_from_file_button.clicked.connect(self.__read_from_file)

        self.__tonation_combo.activated[str].connect(self.__change_scale)
        self.__mode_combo.activated[str].connect(self.__change_scale)
        self.__measure_length_combo.activated[str].connect(self.__change_measure_length)

        self.program:program = program(logger(self.__logs_text), tonation=scale("C", "major"))
        self.rules:(ui_rules | None) = None
        self.solutions:(ui_solution | None) = None
        self.creator:(ui_function_creator | None) = None
        self.__last_input:str = ""
        self.__last_tonation:(scale | None) = None
        self.__rules_changed:bool = True
       
        self.last_save_directory:str = str('/')
        self.last_load_directory:str = str('/')

        self.refresh_rules()
        self.refresh_functions()
        self.__change_measure_length()
        self.__change_scale()

# public:
    def closeEvent(self, event:QCloseEvent) -> None:
        for window in QApplication.topLevelWidgets():
            window.close()

    def close_solution(self) -> None:
        self.solutions = None

    def refresh_functions(self) -> None:
        self.creator = None
        self.__input_text.clear()
        self.__input_text.append(self.program.input)

    def refresh_rules(self) -> None:
        self.__rules_text.clear()
        self.rules = None

        for rule in self.program.rules.active_rules:
            if rule.active:
                self.__rules_text.append(str(rule))
                self.program.program_logger.log(f"Rule {str(rule)} activated.")
            else:
                self.program.program_logger.log(f"Rule {str(rule)} deactivated.")

        self.program.solution = ()
        self.program.beginning = []
        self.program.input = self.__input_text.toPlainText()
        self.__rules_changed = True

# private:
    def __solve(self) -> None:
        start:datetime = datetime.now()
        self.program.program_logger.log(f"Started solving {str(self.program.input)}")

        self.__solve_button.setEnabled(False)

        if self.__last_input != self.program.input or self.__last_tonation is None or self.__last_tonation != self.program.tonation or self.__rules_changed:
            self.program.solve()
            self.program.evaluate_all_solutions()
            self.__rules_changed = False

        self.__last_input = self.program.input
        self.__last_tonation = self.program.tonation
        self.__solve_button.setEnabled(True)

        end:datetime = datetime.now()
        self.program.program_logger.log(f"Finished solving {self.program.input}")
        self.program.program_logger.log(f"Total duration: {(end - start).total_seconds()}.\n")

        self.__show_solutions()

    def __clear_functions(self) -> None:
        self.__input_text.clear()
        self.program.clear()

    def __add_function(self) -> None:
        if self.creator is None:
            self.creator = ui_function_creator(self)
            self.creator.show()
            self.hide()
        else:
            self.creator = None

    def __show_rules(self) -> None:
        if self.rules is None:
            self.rules = ui_rules(self.program.rules, self)
            self.rules.show()
        else:
            self.rules = None

    def __show_solutions(self) -> None:
        if self.solutions is None:
            self.solutions = ui_solution(self)
            self.solutions.show()
        else:
            self.rules = None

    def __clear_logs(self) -> None:
        self.__logs_text.clear()

    def __change_scale(self) -> None:
        try:
            to_set:scale = scale(self.__tonation_combo.currentText(), self.__mode_combo.currentText())            
        except ValueError:
            self.program.program_logger.log(f"Tonation {self.__tonation_combo.currentText()} {self.__mode_combo.currentText()} not found.")
            return
        
        self.program.tonation = to_set
        self.program.solution = ()
        self.program.beginning = []
        self.program.input = self.__input_text.toPlainText()

        self.program.program_logger.log(f"Tonation set to {self.__tonation_combo.currentText()} {self.__mode_combo.currentText()}.")

    def __change_measure_length(self) -> None:
        self.program.measure_length = int(self.__measure_length_combo.currentText())
        self.program.program_logger.log(f"Measure length set to {self.__measure_length_combo.currentText()}.")

    def __read_from_file(self) -> None:
        filename:str = filedialog.askopenfilename(
            initialdir=self.last_load_directory,
            title="Select a file",
            filetypes=(("Harmony files", "*.harm"), ("Text files", "*.txt"))
        )

        self.last_load_directory = ""
        for item in filename.split('/')[:-1]:
            self.last_load_directory += item + '/'

        try:
            file:TextIOWrapper = open(filename, 'r')
        except FileNotFoundError:
            self.program.program_logger.log("File or directory not found")
            return
        
        text:str = ""

        for line in file.readlines():
            for item in line.split(' '):
                if len(item) < 11:
                    self.program.program_logger.log("Invalid file format")
                    file.close()
                    return
                
            text += line + " "

        text = text.strip()
        self.__input_text.setText(text)
        self.program.clear()

        if text != "":
            for item in text.split(' '):
                try:
                    self.program.add_to_task(str_symbol(item))
                except ValueError:
                    self.program.program_logger.log("Invalud function syntax")
                    return


class ui_about(QWidget):
    def __init__(self, menu:ui_menu) -> None:
        super().__init__()
        self.__menu:ui_menu = menu

        self.__title_label:QLabel = QLabel("About")
        self.__about_text:QTextEdit = QTextEdit("This program is essentialy a harmony task decoder.\
        It takes input as function symbols and gives output as notes drawn on staff.\n\nHappy using!")

        self.__about_text.setReadOnly(True)
        self.__title_label.setAlignment(Qt.AlignCenter)
        self.__title_label.setFont(arial_24)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.__title_label)
        self.layout().addWidget(self.__about_text)

        self.setWindowTitle("Harmony decoder - about")
        self.setGeometry(0, 0, 300, 400)
        self.setWindowIcon(QtGui.QIcon('Images/Icon.png'))

        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

    def closeEvent(self, event: QCloseEvent) -> None:
        self.__menu.close_about()


class ui_menu(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Harmony decoder - menu")
        self.setGeometry(0, 0, 300, 200)
        self.setWindowIcon(QtGui.QIcon('Images/Icon.png'))
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

        self.program:(ui_program | None) = None
        self.__about:(ui_about | None) = None

        self.__title_label:QLabel = QLabel("Harmony Decoder")
        self.__title_label.setAlignment(Qt.AlignCenter)
        self.__title_label.setFont(arial_24)

        self.__start_button:QPushButton = QPushButton("Begin")
        self.__exit_button:QPushButton = QPushButton("Exit")
        self.__about_button:QPushButton = QPushButton("About")        

        self.__about_button.setFont(arial_12)
        self.__start_button.setFont(arial_12)
        self.__exit_button.setFont(arial_12)

        self.__up_box:QGroupBox = QGroupBox()
        self.__up_box.setLayout(QHBoxLayout())
        self.__up_box.layout().addWidget(self.__title_label)

        self.__all_box:QGroupBox = QGroupBox()
        self.__all_box.setLayout(QVBoxLayout())
        self.__all_box.setMaximumHeight(150)
        self.__all_box.layout().addWidget(self.__start_button)
        self.__all_box.layout().addWidget(self.__about_button)
        self.__all_box.layout().addWidget(self.__exit_button)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.__up_box)
        self.layout().addWidget(self.__all_box)

        self.__exit_button.clicked.connect(self.__exit)
        self.__start_button.clicked.connect(self.__run)
        self.__about_button.clicked.connect(self.__show_about)

# public:
    def close_about(self) -> None:
        self.__about = None

# private:
    def __exit(self) -> None:
        self.close()

    def __run(self) -> None:
        if self.program is None:
            self.program = ui_program()
            self.program.show()
            self.hide()
        else:
            self.program.close()
            self.program = None
            self.show()

    def __show_about(self) -> None:
        if self.__about is None:
            self.__about = ui_about(self)
            self.__about.show()
        else:
            self.__about.close()
            self.__about = None    


class app:
    def __init__(self) -> None:
        self.__app:QApplication = QApplication(sys.argv)
        self.__menu:ui_menu = ui_menu()        

        self.__menu.show()
        sys.exit(self.__app.exec())
