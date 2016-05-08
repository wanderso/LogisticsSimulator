from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication,  QPushButton,
    QHBoxLayout, QVBoxLayout, QFrame, QSplitter, QTableWidget,
    QTableWidgetItem, QSizePolicy, QScrollArea)
from PyQt5.QtGui import QIcon, QFont, QPainter, QColor, QPen, QPixmap
from PyQt5.QtCore import Qt, QRect
import functools




class LogisticsControlPanel(QFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.logistics_window = parent
        self.initUI()

    def initUI(self):

        stock_button = QPushButton("Stock")
        parts_button = QPushButton("Parts List")
        order_button = QPushButton("Start Order")
        clear_button = QPushButton("Clear")

        stock_button.setAccessibleName("Stock")
        stock_button.clicked.connect(self.parent().stockButtonClicked)
        parts_button.clicked.connect(self.parent().partsButtonClicked)

        order_button.clicked.connect(self.parent().orderButtonClicked)

        clear_button.clicked.connect(self.parent().clearButtonClicked)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        vbox.addWidget(stock_button)
        vbox.addWidget(parts_button)

        vbox.addWidget(order_button)
        vbox.addWidget(clear_button)
        vbox.addStretch(1)

        hbox.addLayout(vbox)
        self.setLayout(hbox)


    def setWorld(self,world):
        pass


class StockSourceDisplayPanel:
    def __init__(self,parent,world):
        self.parent = parent
        self.world = world
        self.scrollable_display = 0
        self.button_display = 0
        self.button_list = []
        self.initUI()

    def initUI(self):
        self.scrollable_display = QScrollArea(self.parent)
        self.button_display = QFrame(self.scrollable_display)
        self.scrollable_display.setWidget(self.button_display)
        self.populate_button_list()
        self.scrollable_display.show()
        self.button_display.show()

    def populate_button_list(self):
        stock_list = self.world.get_stock_source_list()
        vbox = QVBoxLayout()
        button_list = []

        i = 0

        for entry in stock_list:
            entry_button = QPushButton(entry.get_name())
            button_list.append(entry_button)
            vbox.addWidget(entry_button)
            entry_button.clicked.connect(functools.partial(self.parent.stockUI,i,stock_target=entry.get_stock()))
            i += 1

        vbox.addStretch(1)
        self.button_display.setLayout(vbox)
        self.resize()

    def destroy(self):
        self.scrollable_display.hide()
        self.button_display.hide()
        self.parent.resize(self.parent.size())
        self.button_display.destroy(False, False)
        self.scrollable_display.destroy(False, False)

    def resize(self):
        self.scrollable_display.resize(self.parent.size())
        frameWidth = self.scrollable_display.lineWidth()
        self.button_display.resize(self.scrollable_display.size().width()-(frameWidth*2),self.scrollable_display.size().height()-(frameWidth*2))


class StockDisplayPanel(QTableWidget):
    def __init__(self,parent,world,stockTarget):
        super().__init__(parent)
        self.stockTarget = stockTarget
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.world = world
        self.initUI()

    def destroy(self):
        self.hide()
        super().destroy(False,False)

    def initUI(self):
        self.setRowCount(len(self.stockTarget))
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Part", "#"])
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.show()


        i = 0
        for entry in self.stockTarget:
            name_item = QTableWidgetItem(entry[0].name)
            count_item = QTableWidgetItem(str(entry[1]))
            name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            count_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.setItem(i, 0, name_item)
            self.setItem(i, 1, count_item)
            i += 1


    def resize(self):
        super().resize(self.parent().size())

class PartsListDisplayPanel(QTableWidget):
    def __init__(self, parent, world):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.world = world
        self.initUI()

    def destroy(self):
        self.hide()
        super().destroy(False, False)

    def initUI(self):
        part_list = self.world.get_part_list()
        self.setRowCount(len(part_list))
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Part", "Odds", "Expected"])
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.show()


        i = 0
        for entry in part_list:
            name_item = QTableWidgetItem(entry.name)
            odds_item = QTableWidgetItem(str(entry.odds))
            count_item = QTableWidgetItem(str(entry.expected_num_per_design))
            name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            odds_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            count_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.setItem(i, 0, name_item)
            self.setItem(i, 1, odds_item)
            self.setItem(i, 2, count_item)
            i += 1

        self.resize()


    def resize(self):
        super().resize(self.parent().size())

class OrderDisplayPanel(QFrame):
    def __init__(self, parent, world):
        super().__init__(parent)
        self.world = world
        self.logistics_window = parent
        self.initUI()

    def initUI(self):
        self.design = self.world.generate_design()
#        self.show()
        self.lbl1 = QLabel(self)
        self.lbl2 = QLabel(self)
        self.lbl1img = QPixmap('res/email.png')
        self.lbl2img = QPixmap('res/tempo_automation_logo.png')

        self.show()
        self.resize()

    def paintEvent(self, e):
        super().paintEvent(e)
        self.showLabels()


#        self.drawLines(qp)

    def drawLines(self, qp):
        pass

    def showLabels(self):
        h = self.height()
        w = self.width()
        margin = 10
        default_size = 100
        email_label = QRect(margin,margin,default_size,default_size)
        tempo_label = QRect(w-(margin+default_size),margin,default_size,default_size)
        text_label = QRect(margin,margin+default_size+margin,default_size,default_size)

        self.lbl1.setScaledContents(True)
        self.lbl1.setGeometry(email_label)
        self.lbl1.setPixmap(self.lbl1img)
        self.lbl1.show()

        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.black, 2, Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine((2 * margin) + default_size, margin + (default_size / 2), w - ((2 * margin) + default_size), margin + (default_size / 2))

        qp.setFont(QFont('Decorative', 10))
        qp.drawText(text_label, Qt.AlignCenter, "A customer is contacting Tempo Automation...")
        qp.end()


        self.lbl2.setScaledContents(True)
        self.lbl2.setGeometry(tempo_label)
        self.lbl2.setPixmap(self.lbl2img)
        self.lbl2.show()

    def destroy(self):
        self.hide()
        super().destroy(False, False)

    def resize(self):
        super().resize(self.parent().size())
#        self.showLabels()


#pic = QtGui.QLabel(window)
#pic.setGeometry(10, 10, 400, 100)
#use full ABSOLUTE path to the image, not relative
#pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/logo.png"))





class LogisticsDisplayPanel(QFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.logistics_window = parent
        self.table_display = []
        self.initUI()
        self.display_list = []
        self.world = []

    def initUI(self):
        pass

    def wipeUI(self):
        if self.display_list != []:
            self.display_list.destroy()
        self.display_list = []

    def orderUI(self):
        self.wipeUI()
        self.display_list = OrderDisplayPanel(self, self.world)
        layout = QVBoxLayout()
        layout.addWidget(self.display_list)
        self.setLayout(layout)
        self.show()

    def partsUI(self):
        self.wipeUI()
        self.display_list = PartsListDisplayPanel(self, self.world)
        layout = QVBoxLayout()
        layout.addWidget(self.display_list)
        self.setLayout(layout)
        self.show()

    def stockUI(self,num=0,stock_target=[]):
        self.wipeUI()
        if stock_target == []:
            self.display_list = StockSourceDisplayPanel(self, self.world)
            layout = QVBoxLayout()
            layout.addWidget(self.display_list.scrollable_display)
            self.setLayout(layout)
            self.show()
        else:
            self.display_list = StockDisplayPanel(self,self.world,stock_target)
            self.display_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.resize(self.size())
            layout = QVBoxLayout()
            layout.addWidget(self.display_list)
            self.setLayout(layout)
            self.show()


    def resize(self, *args):
        super().resize(*args)
        if self.display_list != []:
            self.display_list.resize()


    def partsButtonClicked(self):
        self.partsUI()

    def stockButtonClicked(self):
        self.stockUI()

    def orderButtonClicked(self):
        self.orderUI()

    def clearButtonClicked(self):
        self.wipeUI()

    def setWorld(self,world):
        self.world = world


class LogisticsWindow(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.control_panel = LogisticsControlPanel(self)
        self.display_panel = LogisticsDisplayPanel(self)

        self.control_panel.setFrameShape(QFrame.StyledPanel)
        self.display_panel.setFrameShape(QFrame.StyledPanel)

        self.hbox0 = QHBoxLayout(self)
        self.hbox0.addWidget(self.control_panel)
        self.hbox0.addWidget(self.display_panel)

        self.hbox1 = QHBoxLayout(self)
        self.hbox2 = QHBoxLayout(self.display_panel)

        self.hbox1.addLayout(self.hbox0)
        self.hbox2.addStretch(1)

        self.setLayout(self.hbox1)

        self.setGeometry(300, 300, 400, 220)
        self.setWindowTitle('Tempo Factory Simulator')
        self.setWindowIcon(QIcon('res/tempo_automation_logo.png'))
        self.show()

    def setWorld(self, world):
        self.control_panel.setWorld(world)
        self.display_panel.setWorld(world)


    def stockButtonClicked(self):
        self.display_panel.stockButtonClicked()
        self.setLayout(self.hbox1)

    def orderButtonClicked(self):
        self.display_panel.orderButtonClicked()
        self.setLayout(self.hbox1)


    def partsButtonClicked(self):
        self.display_panel.partsButtonClicked()
        self.setLayout(self.hbox1)

    def clearButtonClicked(self):
        self.display_panel.clearButtonClicked()
        self.setLayout(self.hbox1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.display_panel.resize(self.display_panel.size())
