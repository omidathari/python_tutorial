import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
def window():
   app = QApplication(sys.argv)
   w = QWidget()
   b = QLabel(w)
   b.setText("Hello World!")
   w.setGeometry(500,500,500,100)
   b.move(50,20)
   w.setWindowTitle("Hello GUI")
   w.show()
   sys.exit(app.exec_())
if __name__ == '__main__':
   window()