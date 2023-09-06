import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class combo(QComboBox):
   def __init__(self, title, parent):
      super(combo, self).__init__( parent)
      self.setAcceptDrops(True)

    # These are overloaded events associated with a combo box object
   def dragEnterEvent(self, e):
      print (e)

      if e.mimeData().hasText():
         e.accept()
      else:
         e.ignore()

   def dropEvent(self, e):
      print (e)
      self.addItem(e.mimeData().text())

   def dragMoveEvent(self, event: 'QGraphicsSceneDragDropEvent') -> None:
    {
        print (event)
    }
   def dragLeaveEvent(self, event: 'QGraphicsSceneDragDropEvent') -> None:
    {
       print (event)  
    }

class Example(QWidget):
   def __init__(self):
      super(Example, self).__init__()

      self.initUI()

   def initUI(self):
      lo = QFormLayout()
      lo.addRow(QLabel("Type some text in textbox and drag it into combo box"))
   
      edit = QLineEdit()
      edit.setDragEnabled(True)
      com = combo("Button", self)
      #lo.addRow(edit,com)
      lo.addRow(edit)
      lo.addRow(com)
      self.setLayout(lo)
      self.setWindowTitle('Simple drag and drop')

   def dragEnterEvent(self, e):
    print (e)

   def dropEvent(self, e):
        print(e)
        pass

def main():
   app = QApplication(sys.argv)
   ex = Example()
   ex.show()
   app.exec()

if __name__ == '__main__':
   main()