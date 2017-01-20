from PyQt4 import QtGui, QtCore, Qt
import time
import math

class FenixGui(QtGui.QWidget):

    def mousePressEvent(self, event):
        print "test 1"
        self.offset = event.pos()
        QtGui.QWidget.mousePressEvent(self, event)


    def mouseMoveEvent(self, event):
        print "test 2"
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)
        QtGui.QWidget.mousePressEvent(self, event)

    def __init__(self):
        super(FenixGui, self).__init__()

        # setting layout type
        hboxlayout = QtGui.QHBoxLayout(self)
        self.setLayout(hboxlayout)

        # hiding title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # setting window size and position
        self.setGeometry(200, 200, 862, 560)
        self.setAttribute(Qt.Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

        # creating background window label
        backgroundpixmap = QtGui.QPixmap("fenixbackground.png")
        self.background = QtGui.QLabel(self)
        self.background.setPixmap(backgroundpixmap)
        self.background.setGeometry(0, 0, 862, 560)

        # fenix logo
        logopixmap = QtGui.QPixmap("fenixlogo.png")
        self.logo = QtGui.QLabel(self)
        self.logo.setPixmap(logopixmap)
        self.logo.setGeometry(100, 100, 400, 150)

def main():
    app = QtGui.QApplication([])
    exm = FenixGui()
    exm.show()
    app.exec_()

if __name__ == '__main__':
    main()