import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

q_app : QApplication = None
rb : QRadioButton = None
cb : QComboBox = None

def window():
   app = QApplication(sys.argv)
   global q_app
   q_app = app
   win = QDialog()
   menu = QMenuBar(win)
   menu.show()

   b1 = QPushButton(win)
   b1.setText("Button1")
   b1.move(50,20)
   b1.clicked.connect(b1_clicked)

   
   b2 = QPushButton(win)
   b2.setText("Button2")
   b2.move(50,50)
   b2.clicked.connect(b2_clicked)

   rb1 = QRadioButton(win)
   rb1.setText("RadioButton")
   rb1.move(50,80)
   rb1.clicked.connect(rb1_clicked)
   global rb
   rb = rb1
   rb.isChecked

   qb1 = QComboBox(win)
   qb1.move(50,120)
   qb1.addItems(["Item1","Item2", "Item3"])
   qb1.currentIndexChanged.connect(cb1_text_changed)
   global cb
   cb = qb1
   
   win.setGeometry(100,100,500,500)

   win.setWindowTitle("PyQt5")
   win.show()
   sys.exit(app.exec_())

def b1_clicked():
   print ("Button 1 clicked")

def b2_clicked():
   print ("Button 2 clicked")

def rb1_clicked():
   print("Radio Button Checked = ", rb.isChecked())

def cb1_text_changed():
   global cb
   print("ComboBox text =", cb.currentText())
   i = QInputDialog()
   i.exec()

if __name__ == '__main__':
   window()