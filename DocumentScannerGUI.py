import sys
from PyQt5 import QtWidgets, uic,QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap,QImage, QPainter
from document_scanner.scan import ScanImage
import numpy as np
import cv2
import imutils

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('DocumentScanner.ui', self)
        self.saveImageButton = self.findChild(QtWidgets.QPushButton, 'saveImage')
        self.processButton = self.findChild(QtWidgets.QPushButton, 'processImage')
        self.inputButton = self.findChild(QtWidgets.QPushButton, 'selectImage')
        self.inputImage = self.findChild(QtWidgets.QLabel, 'inputImage')
        self.outputImage = self.findChild(QtWidgets.QLabel, 'outputImage')
        self.inputButton.clicked.connect(self.openFileNameDialog)
        self.show()
    def GetImputImage(self):
        print("Clicked");
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Image Files (*.jpg *.png)", options=options)
        if fileName:
            print(fileName)
        self.image = fileName        
        pixmap = QPixmap(fileName)
        pixmap = pixmap.scaled(self.inputImage.frameGeometry().width(), self.inputImage.frameGeometry().height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.inputImage.setGeometry(self.inputImage.frameGeometry().x(), self.inputImage.frameGeometry().y(),
                    self.inputImage.frameGeometry().width(), self.inputImage.frameGeometry().height())
        self.inputImage.setPixmap(pixmap)
        self.processButton.clicked.connect(self.SetProgress)
        
    def SetProgress(self):
        scanImage = ScanImage()
        saveScanImage,scanImage = scanImage.SetImage(self.image)
        self.ProcessSaveImage(saveScanImage)
        height, width = scanImage.shape
        bytesPerLine = 3 * width
        scanImage = cv2.cvtColor(scanImage, cv2.COLOR_GRAY2RGB)
        
        
        
        qImg = QImage(scanImage.data, width, height, bytesPerLine,QImage.Format_RGB888)
        pixmap = QPixmap(qImg)
        
        pixmap = pixmap.scaled(self.outputImage.frameGeometry().width(), self.outputImage.frameGeometry().height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.outputImage.setGeometry(self.outputImage.frameGeometry().x(), self.outputImage.frameGeometry().y(),
                    self.outputImage.frameGeometry().width(), self.outputImage.frameGeometry().height())
        self.outputImage.setPixmap(pixmap)
        self.saveImageButton.clicked.connect(self.SaveIMage)
    
    def ProcessSaveImage(self,image):
        height, width = image.shape
        bytesPerLine = 3 * width
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        saveImage = QImage(image.data, width, height, bytesPerLine,QImage.Format_RGB888)
        self.pixmap = QPixmap(saveImage)

    def SaveIMage(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self,"choose save file name","./ScannedImage.png","PNG (*.png);;JPG (*.jpg)")
        if not name[0] == "":
            self.pixmap.save(name[0])
        else:
            return
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())