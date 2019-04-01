import sys
try:
    from PySide import QtCore
    from PySide import QtWidgets
    from PySide import QtGui
except:
    from PyQt5.QtCore import ( pyqtSlot as Slot, pyqtSignal as Signal,
                               QSize, QMimeData, QByteArray)
    from PyQt5 import QtCore
    from PyQt5.QtWidgets import(  QApplication, QWidget, QShortcut,
                                  QBoxLayout, QVBoxLayout,  QHBoxLayout, QGridLayout,
                                  QGroupBox, QPushButton, QListWidget, QListWidgetItem, QAbstractItemView,
                                  QLabel, QLineEdit,
                                  QStyle, QStylePainter, QStyleOption )
    from PyQt5.QtGui import (QIcon, QPalette, QColor, QPixmap, QIntValidator,
                             QDrag,  QKeySequence)


NORTH_ID = "NORTH"
SOUTH_ID = "SOUTH"
WEST_ID = "WEST"
EAST_ID = "EAST"

ICON_SIZE = {'w': 30, 'h': 30}
BUTTON_SIZE = {'w': 40, 'h': 40}
IMAGES_FILES = "images/"


class DirectionPushButton(QPushButton):

    def __init__(self, direction, icon=None, str= None, parent=None):
        super(DirectionPushButton, self).__init__(parent)
        self.direction = direction
        if self.direction["image"] is not None:
            self.setIcon(icon)
            self.setIconSize(QSize(ICON_SIZE['w'], ICON_SIZE['h']))
        self.setFixedSize(QSize(BUTTON_SIZE['w'], BUTTON_SIZE['h']))



class StepListWidget(QListWidget):

    def __init__(self, parent=None):
        super(StepListWidget, self).__init__(parent)
        self.setStyleSheet(open('ViewList_fusion.css').read())
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.proposal = []

    def addStepWidgetItem(self, step_widget):
        item = StepWidgetListItem(step_widget)
        self.addItem(item)
        row = step_widget
        item.setSizeHint(row.minimumSizeHint())
        self.setItemWidget(item, row)

    def initGame(self):
        self.reinitProposal()
        self.clear()

    def reinitProposal(self):
        self.proposal = []

    def getProposal(self):
        self.reinitProposal()
        for i in range(self.count()):
            self.proposal.append(self.item(i).retrieveDataFromStepItem())
        #@TODO remove after debug
        print(self.proposal)

class StepWidgetListItem(QListWidgetItem):
    def __init__(self, step_widget, parent=None):
        super(StepWidgetListItem, self).__init__(parent)
        self.step_widget = step_widget
        #flags = self.flags()

        # @TODO remove after debug
        #if flags & QtCore.Qt.ItemIsDragEnabled:
            #print("OK")
        #else:
            #print("KO")
        #print(self.retrieveDataFromStepItem())

    def retrieveDataFromStepItem(self):
        return {'direction': self.step_widget.direction['id'], 'nbStep': self.step_widget.nb_step}



class StepWidget(QWidget):
    def __init__(self,  direction, step_item = None,  parent = None):
        super(StepWidget, self).__init__(parent)
        self.direction = direction
        self.row = QHBoxLayout()
        self.step_input = QLineEdit()
        self.step_input.setValidator(QIntValidator())
        self.step_input.textChanged.connect(lambda: self.updateStep())
        self.nb_step = 1
        self.initUI()

    def initUI(self):
        self.step_input.setFixedSize(25, 25)
        self.step_input.setText(str(self.nb_step))
        self.row.addWidget(self.step_input)
        self.row.addWidget(QLabel(" pas " + self.direction['label']))
        self.setMinimumSize(150, 15)
        #self.setStyleSheet(open('StepWidget.css').read())
        self.setLayout(self.row)

    def updateStep(self):
        self.nb_step = self.step_input.text()

class GUI(QWidget):
    def __init__(self, parent = None):
        super(GUI, self).__init__(parent)

        self.directions = {
            NORTH_ID:    {"id": NORTH_ID, "action": "up", "add": "addNorthStep", "label": "en haut", "image": IMAGES_FILES + "north.png"},
            SOUTH_ID:    {"id": SOUTH_ID, "action": "down", "add": "addSouthStep", "label": "en bas", "image": IMAGES_FILES + "south.png"},
            WEST_ID:     {"id": WEST_ID, "action": "left", "add": "addWestStep", "label": "à gauche", "image": IMAGES_FILES + "west.png"},
            EAST_ID:     {"id": EAST_ID, "action": "right", "add": "addEastStep", "label": "à droite", "image": IMAGES_FILES + "east.png"}
        }
        self.buttons = {}
        self.icons_area = QVBoxLayout()
        self.icons = QGroupBox('Actions')
        self.icons.setAcceptDrops(True)

        self.actions_area = QBoxLayout(QBoxLayout.TopToBottom)
        self.actions = QGroupBox('Programme')

        self.proposal_viewer = StepListWidget()
        self.initUI()

    def initUI(self):
        main = QHBoxLayout()

        rules = QHBoxLayout()
        main.addLayout(rules)

        self.createIcons()
        self.createActionsList()
        game = QGridLayout()
        game.addWidget(self.icons, 0, 0)
        game.addWidget(self.actions, 0, 1)

        main.addLayout(game)

        terminal = QHBoxLayout()
        main.addLayout(terminal)
        self.setStyleSheet(open('StepWidget.css').read())

        self.setLayout(main)
        self.setGeometry(30, 30, 450, 600)
        self.setWindowTitle('Icare')
        self.show()

    def createIcons(self):
        icon_grid = QGridLayout()
        for id, direction in self.directions.items():
            #print(id)
            icon = QIcon(direction['image'])
            self.buttons[id] = DirectionPushButton(direction, icon, '')
            # @TODO check why the call results of the last method
            #method_to_call = getattr(self, direction['add'])
            #self.buttons[id].clicked.connect(lambda: method_to_call(self.buttons[id]))

        #activating control
        icon_grid.addWidget(self.buttons[NORTH_ID], 0, 1)
        self.buttons[NORTH_ID].clicked.connect(lambda: self.addStepWidget(self.buttons[NORTH_ID]))
        north_shortcut = QShortcut(QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_Up), self)
        north_shortcut.activated.connect(lambda: self.addStepWidget(self.buttons[NORTH_ID]))

        icon_grid.addWidget(self.buttons[SOUTH_ID], 2 , 1)
        self.buttons[SOUTH_ID].clicked.connect(lambda: self.addStepWidget(self.buttons[SOUTH_ID]))
        south_shortcut = QShortcut(QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_Down), self)
        south_shortcut.activated.connect(lambda: self.addStepWidget(self.buttons[SOUTH_ID]))

        icon_grid.addWidget(self.buttons[WEST_ID], 1, 0)
        self.buttons[WEST_ID].clicked.connect(lambda: self.addStepWidget(self.buttons[WEST_ID]))
        west_shortcut = QShortcut(QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_Left), self)
        west_shortcut.activated.connect(lambda: self.addStepWidget(self.buttons[WEST_ID]))

        icon_grid.addWidget(self.buttons[EAST_ID], 1, 2)
        self.buttons[EAST_ID].clicked.connect(lambda: self.addStepWidget(self.buttons[EAST_ID]))
        east_shortcut = QShortcut(QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_Right), self)
        east_shortcut.activated.connect(lambda: self.addStepWidget(self.buttons[EAST_ID]))

        self.icons_area.addLayout(icon_grid)
        self.icons.setLayout(self.icons_area)

    def createActionsList(self):
        button_submit = QPushButton('Submit')
        button_submit.clicked.connect(lambda: self.submitProposal())
        self.actions_area.addWidget(button_submit)

        button_clear = QPushButton('Clear')
        button_clear.clicked.connect(lambda: self.clearGame())
        self.actions_area.addWidget(button_clear)
        self.actions_area.addWidget(self.proposal_viewer)
        self.actions.setLayout(self.actions_area)

    def addStepWidget(self, button):
        step = StepWidget(button.direction)
        self.proposal_viewer.addStepWidgetItem(step)

    #@TODO remove after debug
    def witchBtnConnect(self, b):
        print("clicked button" + b.direction["action"])

    def submitProposal(self):
        #@TODO complete with solution compare
        self.proposal_viewer.getProposal()

    def clearGame(self):
        self.proposal_viewer.initGame()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    gui = GUI()
    sys.exit(app.exec_())


