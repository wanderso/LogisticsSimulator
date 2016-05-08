from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication,  QPushButton,
    QHBoxLayout, QVBoxLayout, QFrame)
from PyQt5.QtGui import QIcon, QFont, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRect

class FactorySquare():
    width = 20
    height = 20

    def __init__(self):
        pass

class FactoryGrid(QWidget):
    def __init__(self,parent):
        super().__init__(parent)

        self.factory_size = (10,10)

        self.initUI()

    def initUI(self):
        self.width_height_grid_measure()

    def width_height_grid_measure(self):
        size = self.size()
        w = size.width()
        h = size.height()

        self.width_fit = int(w/FactorySquare.width)
        self.height_fit = int(h/FactorySquare.width)

        #print(str(self.width_fit) + " " + str(self.height_fit))



    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()
        super().paintEvent(e)

    def drawWidget(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)

        qp.drawLine(0, 0, w, 0)
        qp.drawLine(0, 0, 0, h)

        for i in range(0,self.height_fit+1):
            line_height = i*FactorySquare.height
            qp.drawLine(0, line_height, w, line_height)
            pass

        for i in range(0,self.width_fit+1):
            line_height = i*FactorySquare.width
            qp.drawLine(line_height, 0, line_height, h)
            pass

    def resize(self, *args):
        print("Resizing")

        super().resize(*args)
        self.width_height_grid_measure()




class FactoryView(QFrame):

    def __init__(self,parent):
        super().__init__(parent)
        self.grid = FactoryGrid(self)
#        self.addWidget(self.grid)

        self.initUI()


    def initUI(self):
        self.setMinimumSize(30, 30)


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        self.drawWidget(qp)
        qp.end()
        super().paintEvent(e)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.grid.resize(event.size().width(),event.size().height())

#        size = self.size()
#        w = size.width()
#        h = size.height()
#        self.grid.resize(w,h)


    def drawWidget(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()

        pen = QPen(Qt.black, 2, Qt.SolidLine)

        #self.grid.resize(w,h)

#        qp.setPen(pen)
#        qp.drawLine(0, 0, 250, 250)


