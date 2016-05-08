from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication,  QPushButton,
    QHBoxLayout, QVBoxLayout, QFrame, QSplitter)
from PyQt5.QtGui import QIcon, QFont, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect
from FactoryView import FactoryView

class MainWindow(QWidget):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        self.initUI()


    def initUI(self):

        left = QFrame(self)
        right = FactoryView(self)

        left.setFrameShape(QFrame.StyledPanel)
        right.setFrameShape(QFrame.StyledPanel)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(left)
        splitter1.addWidget(right)



        hbox1 = QHBoxLayout(self)
        hbox2 = QHBoxLayout(right)

    #    factoryFloor = FactoryView(parent=right)

        hbox1.addWidget(splitter1)
     #   hbox2.addWidget(factoryFloor)
        self.setLayout(hbox1)
       # right.setLayout(hbox2)

        self.setGeometry(300, 300, 400, 220)
        self.setWindowTitle('Tempo Factory Simulator')
        self.setWindowIcon(QIcon('res/tempo_automation_logo.png'))
        self.show()

