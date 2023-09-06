from PyQt5 import QtCore, QtGui, QtWidgets

import ui_app

class uiMain( ui_app.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(uiMain,self).__init__()
        self.setupUi(self)
        # self.tab.setStyleSheet("background-color: lightgrey;")
        self.set_tab1_background_color()
        self.pushButton.clicked.connect(self.toggle_color)
        self.bg = False

    def set_tab1_background_color(self):
        #st = self.tab.palette().window().color()
        # setStyleSheet("background-color: default;")
        #print(st.name(0))
        #self.tab.setAutoFillBackground(True)
        self.tab.setStyleSheet("color: red;")
        self.bg = True
        # palette = self.tab.palette()
        # prev_color = self.tab.styleSheet()
        # palette.setColor(self.tab.backgroundRole(), QtCore.Qt.red)
        # self.tab.setPalette(palette)

    
    def toggle_color(self):
        print(self.bg)
        if( self.bg == True ):
             print("Set False")
             #self.tab.setAutoFillBackground(False)
             self.tab.setStyleSheet("border-color: lightgray;")
             self.bg = False
        else:
            print("Set True")
            #self.tab.setAutoFillBackground(True)
            self.tab.setStyleSheet("border-color: red;")
            self.bg = True




if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    qt_app = uiMain()
    qt_app.show()
    sys.exit(app.exec_())