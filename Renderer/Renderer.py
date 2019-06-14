
from PyQt5.QtWidgets import (QWidget, QLabel, 
    QComboBox, QApplication, QSplitter,QHBoxLayout, QPushButton, QFileDialog)
from PyQt5.QtCore import Qt, QRect
from PyQt5 import Qt as Qt_2
import Console as pc
import numpy as np
import sys
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class Example(QWidget):
    #Intalization of global variables used throughout the program
    filetab=[]
    programtab=[]
    outputfilestab=[]
    renderers= []
    actors= []
    mappers = []
    readers = []
    cameras=[]
    viewPortOffsetsX = []
    viewPortOffsetsY = []
    vtkTab =[]
    plyTab = []
    colors = vtk.vtkNamedColors()
    frame = ''
    vtkSection = ''
    light ='On'
    
        
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      

        ## menu panel setup
        ## _____________________________________________
        self.storagePart = QSplitter(Qt.Horizontal)


        self.renderButton = QPushButton('Render ')
        self.renderButton.setEnabled(False)
        self.renderButton.clicked.connect(self.disp)

        self.getFileButton = QPushButton('Get file(s) to render ...')
        self.getFileButton.clicked.connect(self.openDialog)
        self.text = ""

        self.convertButton = QPushButton('Convert ')
        self.convertButton.setEnabled(False)
        self.convertButton.clicked.connect(self.convert)

        self.vtkButton = QPushButton("Store in VTK")
        self.vtkButton.clicked.connect(self.store)
        self.vtkButton.setEnabled(False)
        
        self.plyButton = QPushButton("Store in PLY")
        self.plyButton.clicked.connect(self.store)
        self.plyButton.setEnabled(False)

        
        
        
        self.primitiveList = QComboBox(self)
        
        
        
        self.primitiveList.addItem('Sphere - Adaptive / PCD -> PLY')
        self.primitiveList.addItem('Cube - Adaptive / PCD -> PLY')
        self.primitiveList.addItem( 'Square - Adaptive / PCD -> PLY')
        self.primitiveList.addItem( 'Disk - Adaptive / PCD -> PLY')
        self.primitiveList.addItem('Square - Fixed / PCD -> PLY')
        self.primitiveList.addItem('Disk - Fixed / PCD -> PLY')
        self.primitiveList.setEnabled(False)
        self.primitiveList.activated[str].connect(self.setCommandLine)
        
        self.lightingButton = QComboBox(self)
        self.lightingButton.addItem('On')
        self.lightingButton.addItem('Off')
        self.lightingButton.setEnabled(False)
        self.lightingButton.activated[str].connect(self.setLighting)

        self.sharedInteractionButton= QPushButton("Simultaenous Control") 
        self.sharedInteractionButton.clicked.connect(self.changeShared)
        self.sharedInteractionButton.setEnabled(False)
        self.shared = False

        testButton = QPushButton('Test')
        testButton.clicked.connect(self.disp2)
        
    
        self.filestoRender = QLabel("Files to render: ",self.storagePart)
        self.currentText=["Files to Render :"]
        
        
        self.hBoxLayout= QHBoxLayout(self)

        self.splitterh = QSplitter(Qt.Horizontal)
        self.splitterv = QSplitter(Qt.Vertical)
        self.splitterh_action = QSplitter(Qt.Horizontal)
        self.splitterv_files= QSplitter(Qt.Vertical)
        self.splitter_h_lists=QSplitter(Qt.Horizontal)
        
        self.splitterh.addWidget(self.splitterv)
        
        self.splitterv.addWidget(self.getFileButton)
        self.splitterv.addWidget(self.filestoRender)
        self.splitterv.addWidget(self.splitter_h_lists)
        self.splitter_h_lists.addWidget(self.primitiveList)
        self.splitter_h_lists.addWidget(self.lightingButton)
        self.splitterv.addWidget(self.splitterh_action)
        self.splitterv.addWidget(self.splitterv_files)
        self.splitterv.addWidget(self.sharedInteractionButton)
        self.splitterv_files.addWidget(self.vtkButton)
        self.splitterv_files.addWidget(self.plyButton)
        self.splitterh_action.addWidget(self.convertButton)
        self.splitterh_action.addWidget(self.renderButton)
##__________________end menu panel setup
        self.frame = Qt_2.QFrame()

        
        self.vtkSection = QVTKRenderWindowInteractor(self.frame)
    
        ##example renderer(s)
        self.iren = self.vtkSection.GetRenderWindow().GetInteractor()
        
        self.hBoxLayout.addWidget(self.splitterh)
        
        
        self.setLayout(self.hBoxLayout)
              
        self.splitterh.addWidget(self.frame)
        self.setGeometry(0,0,1920,1080)
        
        
        self.setWindowTitle('Renderer')
        self.show()
        self.iren.Initialize()
        self.vtkSection.setGeometry(0,0,self.splitterh.sizes()[1],1080)
        
        
        
        
    def changeShared(self):
        self.shared= not(self.shared)
        for i in range(1,len(self.renderers)):
            if (self.shared):
                self.renderers[i].SetActiveCamera(self.cameras[0])
            elif not(self.shared):
                self.renderers[i].SetActiveCamera(self.cameras[i])

    def setLighting(self,text):
        self.light = text
    def disp(self):
        viewPortOffsetX = np.linspace(0,1,len(self.outputfilestab)+1).tolist()
        viewPortsOffsetY = (0,1)
        for j in range(0,len(self.outputfilestab)):
            self.renderers.append(vtk.vtkRenderer())
            self.cameras.append(self.renderers[len(self.renderers)-1].GetActiveCamera())
            self.renderers[j].SetViewport(viewPortOffsetX[j],viewPortsOffsetY[0],viewPortOffsetX[j+1],viewPortsOffsetY[1])
        for i in range(0,len(self.outputfilestab)):
            
            self.vtkSection.GetRenderWindow().AddRenderer(self.renderers[i])  
            
        for i in range(0,len(self.outputfilestab)):
           
            self.readers.append(vtk.vtkPLYReader())
            self.readers[i].SetFileName(self.outputfilestab[i])
            self.readers[i].Update()
           
            self.mappers.append(vtk.vtkPolyDataMapper())
            self.mappers[i].SetInputConnection(self.readers[i].GetOutputPort())

            self.actors.append(vtk.vtkActor())
            self.actors[i].SetMapper(self.mappers[i])
            self.actors[i].GetProperty().SetColor(self.colors.GetColor3d('Tan'))
            
            self.renderers[i].SetBackground(self.colors.GetColor3d('Black'))
            if(self.light=='Off'):
                self.actors[i].GetProperty().LightingOff()
            self.renderers[i].AddActor(self.actors[i])
            self.renderers[i].ResetCamera()
            
            

        self.vtkButton.setEnabled(True)
        self.plyButton.setEnabled(True)
        self.renderButton.setEnabled(False)
        self.sharedInteractionButton.setEnabled(True)
            
    def openDialog(self):
        f = QFileDialog.getOpenFileName(self, "Open File", "~", "Point cloud Files (*.pcd *.ply)")
        if f!='': 
            self.filetab.append(f[0])
            self.primitiveList.setEnabled(True)
            self.lightingButton.setEnabled(True)
                        
    def setCommandLine(self,text):
        sender = self.sender()
        
        
        if text == 'Square - Adaptive / PCD -> PLY':
            self.programtab.append(("./pcl_preprocessing_adaptive", self.filetab[len(self.filetab) -1], "square", "output(%d).ply" % len(self.outputfilestab),"nl"))
        elif text == 'Disk - Adaptive / PCD -> PLY':
             self.programtab.append(("./pcl_preprocessing_adaptive", self.filetab[len(self.filetab)-1], "disk", "output(%d).ply" % len(self.outputfilestab),"nl"))
        if text == 'Square - Fixed / PCD -> PLY':
            self.programtab.append(("./pcl_preprocessing", self.filetab[len(self.filetab) -1], "squaref", "output(%d).ply" % len(self.outputfilestab),"nl"))
        elif text == 'Disk - Fixed / PCD -> PLY':
             self.programtab.append(("./pcl_preprocessing", self.filetab[len(self.filetab)-1], "diskf", "output(%d).ply" % len(self.outputfilestab),"nl"))
        elif text == 'Sphere - Adaptive / PCD -> PLY':
            self.programtab.append(("./pcl_preprocessing_adaptive", self.filetab[len(self.filetab)-1], "sphere", "output(%d).ply" % len(self.outputfilestab)))
        elif text == 'Cube - Adaptive / PCD -> PLY':
            self.programtab.append(("./pcl_preprocessing_adaptive", self.filetab[len(self.filetab)-1], "cube", "output(%d).ply" % len(self.outputfilestab)))
        
        
        self.outputfilestab.append("output(%d).ply" % len(self.outputfilestab))
        
        self.currentText.append(self.filetab[len(self.filetab)-1]+" | "+text)
        textToDisplay = "\n".join(self.currentText)
        self.filestoRender.setText(textToDisplay)
        self.convertButton.setEnabled(True)

    def convert(self):
        self.convertButton.setEnabled(False)
        
        pc.main(self.programtab)
        
        self.filetab=[]
        self.programtab=[]
        self.renderButton.setEnabled(True)
        self.primitiveList.setEnabled(False)
        self.lightingButton.setEnabled(False)
        
    def store(self,text):
        
        wb = self.sender().text()
        dialog = QFileDialog()
        path = dialog.getExistingDirectory(self,"Select Directory")
        if wb == "Store in VTK":
            self.ply2vtk(path)
        elif wb == "Store in PLY":
            self.ply2ply(path)
            
    def ply2vtk(self,text): 
        for elem in self.outputfilestab:
            self.vtkTab.append(("pcl_ply2vtk",elem,text+"/output(%d).vtk" % self.outputfilestab.index(elem)))
        pc.main(self.vtkTab)
        self.vtkTab=[]

    def ply2ply(self,text):
        for elem in self.outputfilestab:
             self.plyTab.append(("cp",elem,text+"/output(%d).ply" % self.outputfilestab.index(elem)))
             
        pc.main(self.plyTab)
        self.plyTab=[]

  
 
                 
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())