from .PaIRS_pypacks import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PIL import Image, ImageQt

#https://www.pythonguis.com/tutorials/pyqt-layouts/
class Calvi(QWidget):

  def __init__(self, *args, **kwargs):
    super(Calvi, self).__init__(*args, **kwargs)

    self.buttonBar = QWidget()
    self.graphWidget = pg.PlotWidget()
    self.imgWidget = pg.ImageView()
    self.gv = pg.GraphicsView()
    
    self.label = QtWidgets.QLabel()
  




    self.mainLayout = QVBoxLayout()
    #self.mainLayout.addWidget(self.label)
    #self.draw_something()
    
    #self.mainLayout.addWidget(self.graphWidget)
    #self.mainLayout.addWidget(self.buttonBar)
    self.mainLayout.addWidget(self.gv)
    
    #self.mainLayout.addWidget(self.imgWidget)

    self.setLayout(self.mainLayout)

    self.buttonLayout = QHBoxLayout()
    self.buttonBar.setLayout(self.buttonLayout)
    self.buttonSpacer=QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.buttonLayout.addItem(self.buttonSpacer)

    self.buttons=[]

    self.addButton('Hello, world!',lambda: print('Hello, world!'))
    self.addButton('How are you?',lambda: print('How are you?'))
    self.addButton('How are you?',lambda: print('How are you?'))
    self.proxyMouseMove = pg.SignalProxy(self.gv.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
    #self.proxyMouseDrag = pg.SignalProxy(self.gv.scene().sigMouseDrag, rateLimit=60, slot=self.mouseDrag)
    self.proxy = pg.SignalProxy(self.gv.scene().sigMouseClicked, rateLimit=60, slot=self.mouseClick)
    #self.gv.scene().sigMouseClicked.connect(self.mouseClick)  #si può usare anche questa (con accesso direttamente alla variabile al posto della lista) ma quale è la differenza?
    
    
    self.examplePlot()
  def draw_something(self):
    canvas = QtGui.QPixmap(400, 300)
    nomeImg='C:/Dati/Dropbox/DATI/Piv/calvi/CalVi/img/-2mm_cam0.tif'
    #nomeImg='C:/desk/OneDrive - Unina/Personali/foto/22-02-2013_Defence committee_1.jpg'
    data=ImageQt.ImageQt(Image.open(nomeImg))
    #canvas.fill(Qt.white)
    canvas=QtGui.QPixmap.fromImage(data)
    painter = QtGui.QPainter(canvas)
    painter.drawLine(10, 10, 300, 200)
    painter.end()
    self.label.setPixmap(canvas)

  def mouseMoved(self,evt):
    #mousePoint = self.gv.vb.mapSceneToView(evt[0])
    mousePoint =self.img.mapFromScene(evt[0])
    #print(" x = %0.2f y = %0.2f" % (mousePoint.x(), mousePoint.y()))
  def mouseClick(self,evt):
    #MouseClickEvent  :https://pyqtgraph.readthedocs.io/en/latest/api_reference/graphicsscene/mouseclickevent.html#pyqtgraph.GraphicsScene.mouseEvents.MouseClickEvent
    
    #mousePoint =self.img.mapFromScene(evt[0].pos())# se si preme fuori dall'img da errore
    mousePoint =self.img.mapFromScene(evt[0].scenePos() ) # sembra uguale a quella precedente ma non da errore
    print(f"Mouse click ({mousePoint.x()},{mousePoint.y()})  {evt[0].button()}  {evt[0].buttons()} double {evt[0].double()}")
    
  def mouseDrag(self,evt):
    #MouseClickEvent  :https://pyqtgraph.readthedocs.io/en/latest/api_reference/graphicsscene/mouseclickevent.html#pyqtgraph.GraphicsScene.mouseEvents.MouseClickEvent
    #mousePoint =self.img.mapFromScene(evt[0].pos())
    mousePointUp =self.img.mapFromScene(evt[0].buttonDownPos() ) 
    mousePointDown =self.img.mapFromScene(evt[0].scenePos() ) 
    print(f"Mouse down ({mousePointDown.x()},{mousePointDown.y()}) Mouse Up ({mousePointUp.x()},{mousePointUp.y()}) {evt[0].button()}  {evt[0].buttons()} double {evt[0].double()}")
      

  def examplePlot(self):
    hour = [1,2,3,4,5,6,7,8,9,10]
    temperature = [30,32,34,32,33,31,29,32,35,45]
    # plot data: x, y values
    self.graphWidget.plot(hour, temperature)
    exampleFolder='../_examples/'
    nomeImg=exampleFolder+'synthetic00010.jpg'
    nomeImg='C:/Dati/Dropbox/DATI/Piv/calvi/CalVi/img/-2mm_cam0.tif'
    #nomeImg='C:/desk/OneDrive - Unina/Personali/foto/22-02-2013_Defence committee_1.jpg'
    data=np.ascontiguousarray(Image.open(nomeImg))

    
    #self.img=pg.ImageItem(data)
    self.img=pg.ImageItem(data.T)
    tr = QtGui.QTransform()  # prepare ImageItem transformation:
    tr.scale(.25, .25)  # scale horizontal and vertical axes
    #tr.translate(-50, 50) # move 3x3 image to locate center at axis origin
    self.img.setTransform(tr)
    #self.img.setRect(0,0,600,350)
    self.gv.addItem(self.img)
    #self.imgWidget.setImage(data)


    


  def addButton(self,label,callback):
    b=QPushButton(label,self)
    self.buttons.append(b)
    self.buttonLayout.removeItem(self.buttonSpacer)
    self.buttonLayout.addWidget(b)
    self.buttonLayout.addItem(self.buttonSpacer)
    
    b.clicked.connect(callback)
#p = Calvi()
#proxy = pg.SignalProxy(p.graphWidget.scene().sigMouseMoved, rateLimit=60, slot=p.mouseMoved)


def main():
  app = QtWidgets.QApplication(sys.argv)
  main = Calvi()
  main.show()
  sys.exit(app.exec())


if __name__ == '__main__':
  main()
