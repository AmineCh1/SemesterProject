

import sys
from enum import Enum

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class camMode(Enum):
    OFF = 0
    CAMERA = 1
    CORNER = 2

def read_batch(batch_file):
    fb = open('Batches/'+batch_file,'r').readlines()
    fb = [x.rstrip() for x in fb]
    return list(map(lambda x: x.split(),fb))
class Ui_MainWindow(object):
    cameraMode = 0
    currentQuestion = 0
    initial = 0

    radioButtons = []
    #IMPORTANT : Modify this line to change the current batch and set the answers text file.
    CURRENT_BATCH = ("batch_10.txt","answers_10.txt")
    files = read_batch(CURRENT_BATCH[0])
    answersTab = [None] * len(files)
    rendererLeft = vtk.vtkRenderer()
    rendererRight = vtk.vtkRenderer()
    mapperLeft = vtk.vtkPolyDataMapper()
    mapperRight = vtk.vtkPolyDataMapper()
    readerLeft = vtk.vtkDataSetReader()
    readerRight = vtk.vtkDataSetReader()
    actorLeft = vtk.vtkActor()
    actorRight = vtk.vtkActor()
    rendererLeft.SetActiveCamera(rendererRight.GetActiveCamera())
    interactionStyle = vtk.vtkInteractorStyleSwitch()
    

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2880, 1800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 210, 131, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        for i in range(9):
            self.radioButtons.append(QtWidgets.QRadioButton(self.verticalLayoutWidget))
            self.radioButtons[i].setObjectName("radioButton_%d" % i)
            self.verticalLayout.addWidget(self.radioButtons[i])
            self.radioButtons[i].setChecked(False)
            self.radioButtons[i].setStyleSheet('QRadioButton{font: 10pt Helvetica MS;} QRadioButton::indicator { width: 10px; height: 10px;};')
            self.radioButtons[i].clicked.connect(self.enablenext)
        self.commandLinkButton = QtWidgets.QCommandLinkButton(
            self.centralwidget)
        self.commandLinkButton.setGeometry(QtCore.QRect(0, 360, 131, 41))
        self.commandLinkButton.setObjectName("commandLinkButton")

        self.labelLeft = QtWidgets.QLabel(MainWindow)
        self.labelRight = QtWidgets.QLabel(MainWindow)
        #IMPORTANT: MODIFY THIS LINE WHEN DEALING WITH EVEN/ODD SUBJECT NUMBERS.
        self.imgref = QtGui.QPixmap('DIST2.png')
        self.imgdist =QtGui.QPixmap('REF2.png')

        
        self.labelLeft.setPixmap(self.imgref)
        self.labelRight.setPixmap(self.imgdist)
        self.labelLeft.setFixedSize(self.imgref.size())
        self.labelRight.setFixedSize(self.imgdist.size())

        self.labelLeft.move(QtCore.QPoint(150,0))
        self.labelRight.move(QtCore.QPoint(795,0))


        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 150, 70))
        self.textBrowser.setObjectName("textBrowser")

        #self.frame = QtWidgets.QFrame(MainWindow)
        self.vtkSection = QVTKRenderWindowInteractor(MainWindow)
        
        self.rendererLeft.GetActiveCamera().ParallelProjectionOn()
        self.rendererRight.GetActiveCamera().ParallelProjectionOn()
        #self.frame.setGeometry(QtCore.QRect(131, 0, 2880, 1800))
        self.vtkSection.setGeometry(QtCore.QRect(150, 40, 1290,860))
        self.commandLinkButton.clicked.connect(self.registerAnswer)
        self.commandLinkButton.setEnabled(False)


      
        # b =map(lambda x: str(x),self.files)
        # print('\n'.join(b))
        # print("-------------------------")
        
        
        self.iren = self.vtkSection.GetRenderWindow().GetInteractor()
        if (self.initial == 0):
            self.dispContents(0,camMode.OFF)
            self.initial = 1
       
        
        self.iren.ReInitialize()


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def enablenext(self):
        self.commandLinkButton.setEnabled(True)

    def writeAnswers(self):
        with open("Results/"+self.CURRENT_BATCH[1], 'w') as f:
            for idx,item in enumerate(self.answersTab):
                f.write(str(self.files[idx]) + " " +"%s\n" % item)

    def endOfExp(self):
        self.writeAnswers()
        sys.exit()

    def registerAnswer(self):
        a = np.argwhere([elem.isChecked() for elem in self.radioButtons]).flatten()[0]
        self.answersTab[self.currentQuestion] =  9 -(a)
        self.changeQuestion()

    def changeQuestion(self):
        if (self.currentQuestion == len(self.files) - 1):
            self.endOfExp()

        else:
            for elem in self.radioButtons:
                elem.setChecked(False)
            self.currentQuestion += 1
            self.dispContents(self.currentQuestion,camMode.OFF)

    def dispContents(self,current,cameraMode):
        self.interactionStyle.SetCurrentStyleToTrackballActor()
        self.rendererLeft.SetViewport(0,0,0.5,1)
        self.rendererRight.SetViewport(0.5,0,1,1)

        self.vtkSection.GetRenderWindow().AddRenderer(self.rendererLeft)
        self.vtkSection.GetRenderWindow().AddRenderer(self.rendererRight)

        self.readerLeft.SetFileName(self.files[current][0])
        self.readerRight.SetFileName(self.files[current][1])
        self.readerLeft.Update()
        self.readerRight.Update()

        self.mapperLeft.SetInputConnection(self.readerLeft.GetOutputPort())
        self.mapperRight.SetInputConnection(self.readerRight.GetOutputPort())

        self.actorLeft.SetMapper(self.mapperLeft)
        self.actorRight.SetMapper(self.mapperRight)

        self.rendererLeft.AddActor(self.actorLeft)
        self.rendererRight.AddActor(self.actorRight)

        if (cameraMode == camMode.OFF):
            self.actorLeft.GetProperty().LightingOff()
            self.actorRight.GetProperty().LightingOff()

        self.actorLeft.GetProperty().SetInterpolationToPhong()
        

        self.rendererLeft.ResetCamera()
        self.rendererRight.ResetCamera()
        self.iren.ReInitialize()
        self.commandLinkButton.setEnabled(False)
        print(self.answersTab[self.currentQuestion-1])
        print(self.files[current][0]+' '+  self.files[current][1])
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        self.radioButtons[0].setText(_translate("MainWindow"," 9 - Imperceptible"))
        self.radioButtons[1].setText(_translate("MainWindow","8"))
        self.radioButtons[2].setText(_translate("MainWindow","7 - Perceptible but not  \n annoying"))
        self.radioButtons[3].setText(_translate("MainWindow","6"))
        self.radioButtons[4].setText(_translate("MainWindow","5 - Slightly Annoying"))
        self.radioButtons[5].setText(_translate("MainWindow","4"))
        self.radioButtons[6].setText(_translate("MainWindow","3 - Annoying "))
        self.radioButtons[7].setText(_translate("MainWindow","2"))
        self.radioButtons[8].setText(_translate("MainWindow","1 - Very Annoying"))
       
        self.commandLinkButton.setText(_translate("MainWindow", "Next"))

        self.textBrowser.setHtml(
            _translate(
                "MainWindow",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Noto Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Welcome !</p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">How would you rate the level of impairment of the distorted content with respect to the reference? </p></body></html>"
            ))
