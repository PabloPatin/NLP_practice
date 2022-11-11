from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
# from oldUI.TestUI1 import Ui_MainWindow
from geo_UI import Ui_MainWindow
# from oldUI.GUI import Point_st
import sys


class CountRow:
    def __init__(self):
        pass


class DistBox:
    def __init__(self, i, row):
        self.row = row
        self.lineEdit = QLineEdit()
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMaximumSize(QtCore.QSize(160, 16777215))
        self.lineEdit.setObjectName(f"horiz{i}")



class AlgleBox:
    def __init__(self, i):
        # Задаём поля для ввода данных
        self.box = QHBoxLayout()
        self.box.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.box.setSpacing(1)
        self.box.setObjectName(f"angle{i}")

    def fillBox(self, i):
        self.degrees = QLineEdit()
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.degrees.sizePolicy().hasHeightForWidth())
        self.degrees.setSizePolicy(sizePolicy)
        self.degrees.setMinimumSize(QtCore.QSize(20, 0))
        self.degrees.setMaximumSize(QtCore.QSize(60, 16777215))
        self.degrees.setObjectName(f"degrees{i}")
        self.minutes = QLineEdit()
        self.minutes.setSizePolicy(sizePolicy)
        self.minutes.setMinimumSize(QtCore.QSize(20, 0))
        self.minutes.setMaximumSize(QtCore.QSize(60, 16777215))
        self.minutes.setObjectName(f"minutes{i}")
        self.label_1 = QLabel()
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_1.sizePolicy().hasHeightForWidth())
        self.label_1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_1.setFont(font)
        self.label_1.setObjectName(f"label{i}_1")
        self.label_1.setText('° ')
        self.label_2 = QLabel()
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setFont(font)
        self.label_2.setObjectName(f"label{i}_2")
        self.label_2.setText("\'")
        self.box.addWidget(self.degrees)
        self.box.addWidget(self.label_1)
        self.box.addWidget(self.minutes)
        self.box.addWidget(self.label_2)


class PointStr:
    def __init__(self, i, row):
        # Именуем строку
        self.punkt = QLabel(f'Измерительный пункт {i + 1}')
        self.punkt.setObjectName(f"punkt{i}")
        self.row = row
        print(i)

        # Задаём поля для ввода данных
        self.angle = AlgleBox(i)
        self.x = QLineEdit()
        self.sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(self.x.sizePolicy().hasHeightForWidth())
        self.x.setSizePolicy(self.sizePolicy)
        self.x.setMinimumSize(QtCore.QSize(65, 0))
        self.x.setMaximumSize(QtCore.QSize(80, 16777215))
        self.x.setObjectName(f"x{i}")
        self.y = QLineEdit()
        self.y.setSizePolicy(self.sizePolicy)
        self.y.setMinimumSize(QtCore.QSize(65, 0))
        self.y.setMaximumSize(QtCore.QSize(80, 16777215))
        self.y.setObjectName(f"y{i}")


class MyWindow(QMainWindow):
    i = 1

    def __init__(self):
        super(MyWindow, self).__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.punkts = []
        self.distanses = []
        # self.setStartUI()
        # self.retranslateUi()
        self.gui.clearButton.clicked.connect(self.clearAllData)
        self.gui.addButton.clicked.connect(self.addNewPoint)
        # self.ui.datascreen.addWidget(QLabel('asldalsjldjalkjskdjkalksjkdlaksdasd'), 1, 1)
        # self.ui.datascreen.addWidget(QLabel('HelloWorld!'), 1, 2)
        # self.ui.i = self.ui.datascreen.cellRect(1, 1)
        # self.ui.j = self.ui.datascreen.cellRect(1, 2)


    # def setStartUI(self):
    #     self.setObjectName("MainWindow")
    #     self.resize(1127, 948)
    #     self.centralwidget = QWidget(self)
    #     self.centralwidget.setObjectName("centralwidget")
    #     self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
    #     self.horizontalLayout_3.setObjectName("horizontalLayout_3")
    #     self.fullscreen = QHBoxLayout()
    #     self.fullscreen.setSizeConstraint(QLayout.SetMaximumSize)
    #     self.fullscreen.setObjectName("fullscreen")
    #     self.workzone = QVBoxLayout()
    #     self.workzone.setObjectName("workzone")
    #     self.header = QLabel(self.centralwidget)
    #     font = QtGui.QFont()
    #     font.setPointSize(15)
    #     font.setBold(True)
    #     font.setWeight(75)
    #     self.header.setFont(font)
    #     self.header.setObjectName("header")
    #     self.workzone.addWidget(self.header)
    #     self.datascreen = QGridLayout()
    #     self.datascreen.setSizeConstraint(QLayout.SetNoConstraint)
    #     self.datascreen.setContentsMargins(3, -1, -1, -1)
    #     self.datascreen.setObjectName("datascreen")
    #     self.fullscreen.addLayout(self.workzone)
    #     self.column3 = QLabel(self.centralwidget)
    #     sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
    #     sizePolicy.setHorizontalStretch(0)
    #     sizePolicy.setVerticalStretch(0)
    #     sizePolicy.setHeightForWidth(self.column3.sizePolicy().hasHeightForWidth())
    #     self.column3.setSizePolicy(sizePolicy)
    #     self.column3.setMinimumSize(QtCore.QSize(40, 0))
    #     self.column3.setAlignment(QtCore.Qt.AlignCenter)
    #     self.column3.setObjectName("column3")
    #     self.datascreen.addWidget(self.column3, 0, 4, 1, 1)
    #     self.column6 = QLabel(self.centralwidget)
    #     self.column6.setAlignment(QtCore.Qt.AlignCenter)
    #     self.column6.setObjectName("column6")
    #     self.datascreen.addWidget(self.column6, 0, 7, 1, 1)
    #     self.column5 = QLabel(self.centralwidget)
    #     self.column5.setAlignment(QtCore.Qt.AlignCenter)
    #     self.column5.setObjectName("column5")
    #     self.datascreen.addWidget(self.column5, 0, 6, 1, 1)
    #     self.punkt1 = QLabel(self.centralwidget)
    #     self.punkt1.setObjectName("punkt1")
    #     self.datascreen.addWidget(self.punkt1, 1, 0, 1, 1)
    #     self.column1 = QLabel(self.centralwidget)
    #     self.column1.setAlignment(QtCore.Qt.AlignCenter)
    #     self.column1.setObjectName("column1")
    #     self.datascreen.addWidget(self.column1, 0, 1, 1, 1)
    #     self.column2 = QLabel(self.centralwidget)
    #     self.column2.setAlignment(QtCore.Qt.AlignCenter)
    #     self.column2.setObjectName("column2")
    #     self.datascreen.addWidget(self.column2, 0, 2, 1, 1)
    #     self.column4 = QLabel(self.centralwidget)
    #     self.column4.setMinimumSize(QtCore.QSize(40, 0))
    #     self.column4.setAlignment(QtCore.Qt.AlignCenter)
    #     self.column4.setObjectName("column4")
    #     self.datascreen.addWidget(self.column4, 0, 5, 1, 1)
    #     self.horizontalLayout_3.addLayout(self.fullscreen)
    #
    #
    #
    #
    # def retranslateUi(self):
    #     _translate = QtCore.QCoreApplication.translate
    #     self.setWindowTitle(_translate("MainWindow", "Калькулятор теодолитного хода"))
    #     self.header.setText(_translate("MainWindow", "Входные данные"))
    #     # self.label_9.setText(_translate("MainWindow", "° "))
    #     # self.label_10.setText(_translate("MainWindow", "\'"))
    #     # self.punkt2.setText(_translate("MainWindow", "Измерительный пункт 2"))
    #     self.column3.setText(_translate("MainWindow", "∆X, m"))
    #     self.column6.setText(_translate("MainWindow", "Y"))
    #     self.column5.setText(_translate("MainWindow", "X"))
    #     # self.punkt1.setText(_translate("MainWindow", "Измерительный пункт 1"))
    #     self.column1.setText(_translate("MainWindow", "Угол"))
    #     self.column2.setText(_translate("MainWindow", "Дирекционный угол"))
    #     self.column4.setText(_translate("MainWindow", "∆Y, m"))
    #     # self.label.setText(_translate("MainWindow", "Горизонтальное расстояние, m"))
    #     # self.addButton.setText(_translate("MainWindow", "Добавить"))
    #     # self.inputButton.setText(_translate("MainWindow", "Ввести данные"))
    #     # self.clearButton.setText(_translate("MainWindow", "Очистить"))
    #     # self.menu.setTitle(_translate("MainWindow", "Файл"))
    #     # self.menu_2.setTitle(_translate("MainWindow", "Импортировать из..."))
    #     # self.newFile.setText(_translate("MainWindow", "Новый файл"))
    #     # self.openFile.setText(_translate("MainWindow", "Открыть..."))
    #     # self.saveFile.setText(_translate("MainWindow", "Сохранить"))
    #     # self.savwFileAs.setText(_translate("MainWindow", "Сохранить как..."))
    #     # self.deleteFile.setText(_translate("MainWindow", "Удалить файл"))
    #     # self.actionExcel.setText(_translate("MainWindow", "Excel"))
    #     # self.actionjson.setText(_translate("MainWindow", ".json"))
    #     # self.action_gora.setText(_translate("MainWindow", ".gora"))


    def clearAllData(self):
        '''перезапускает окно рассчётов и граф'''
        # print('hui')
        # try:
        # print(self.punkts[0].)
        # self.punkts[1].x.setText('somethink')
        # except:
        #     Exception

    def count(self):
        '''запускает подсчёт значений'''

    def draph(self):
        '''строит граф'''

    def addNewPoint(self):
        '''добовляет пункт измерений'''
        datascreen = self.gui.datascreen
        row = PointStr(self.i // 2, self.i)
        row.angle.fillBox(row.row)
        spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        datascreen.addItem(spacerItem, row.row-1, 0, 1, 1)
        datascreen.addLayout(row.angle.box, row.row, 1, 1, 1)
        datascreen.addWidget(row.punkt, row.row, 0)
        datascreen.addWidget(row.x, row.row, 6)
        datascreen.addWidget(row.y, row.row, 7)
        datascreen.addWidget(self.gui.addButton, self.i + 1, 0)
        dist = DistBox((self.i-1)//2, self.i-1)
        # datascreen.addWidget(dist, dist.row, 3, 1, 1)
        self.punkts.append(row)
        self.i += 2

    def addNewAngle(self, place):
        '''добавляет новый угол'''


if __name__ == "__main__":
    app = QApplication([])
    application = MyWindow()
    application.show()
    sys.exit(app.exec())
