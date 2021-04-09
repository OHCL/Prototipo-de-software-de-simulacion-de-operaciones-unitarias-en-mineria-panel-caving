
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QColor, QPolygon, QCursor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu, QAction, QFileDialog, QLabel,
                             QGraphicsView, QStatusBar, QGraphicsScene, QInputDialog, QLineEdit)
from PyQt5.QtCore import Qt, QPoint
import sys
import threading
import itertools as it
import numpy as np
import matplotlib.pyplot as plt
from AStar import *

d=0
class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setMouseTracking (True)
        self.greenList = []
        self.blueList = []
        self.LHDdict = dict()
        self.PEdict = dict()
        self.PVdict = dict()
        self.RutaDict = dict()
        self.tiempoSim = 120

        top = 400
        left = 400
        width = 800
        height = 600

        icon = "Gopher Underground.png"
        self.setWindowTitle("Gopher Underground")
        self.setGeometry(top, left, width, height)
        self.setWindowIcon(QIcon(icon))

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.brushSize = 1
        self.brushColor = Qt.black

        self.lastPoint = QPoint()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        brushMenu = mainMenu.addMenu("Brush Size")
        brushColor = mainMenu.addMenu("Brush Color")
        startSim = mainMenu.addMenu("Start Simulation")
        panelBuilder = mainMenu.addMenu("Panel Builder")
        Charts = mainMenu.addMenu("Charts")
        Config = mainMenu.addMenu("Config.")

        saveAction = QAction(QIcon("Save.png"), "Guardar", self)
        #saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction(QIcon("Clear.png"), "Limpiar", self)
        #clearAction.setShortcut("Ctrl+L")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        onepxAction = QAction("1 px.", self)
        #onepxAction.setShortcut("Ctrl+O")
        brushMenu.addAction(onepxAction)
        onepxAction.triggered.connect(self.onePx)

        threepxAction = QAction("3 px.", self)
        #threepxAction.setShortcut("Ctrl+T")
        brushMenu.addAction(threepxAction)
        threepxAction.triggered.connect(self.threePx)

        fivepxAction = QAction("5 px.", self)
        #fivepxAction.setShortcut("Ctrl+F")
        brushMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivePx)

        sevenpxAction = QAction("7 px.", self)
        #sevenpxAction.setShortcut("Ctrl+E")
        brushMenu.addAction(sevenpxAction)

        ninepxAction = QAction("9 px.", self)
        #ninepxAction.setShortcut("Ctrl+N")
        brushMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninePx)

        blackAction = QAction("Black", self)
        #blackAction.setShortcut("Ctrl+B")
        brushColor.addAction(blackAction)
        blackAction.triggered.connect(self.blackBrush)

        greenAction = QAction("Green", self)
        #greenAction.setShortcut("Ctrl+B")
        brushColor.addAction(greenAction)
        greenAction.triggered.connect(self.greenBrush)

        blueAction = QAction("Blue", self)
        #blueAction.setShortcut("Ctrl+B")
        brushColor.addAction(blueAction)
        blueAction.triggered.connect(self.blueBrush)

        whiteAction = QAction("White", self)
        #whiteAction.setShortcut("Ctrl+W")
        brushColor.addAction(whiteAction)
        whiteAction.triggered.connect(self.whiteBrush)

        Comenzar = QAction("Demostracion", self)
        #Comenzar.setShortcut("Ctrl+O")
        startSim.addAction(Comenzar)
        Comenzar.triggered.connect(self.simStart)

        # LenghtPath = QAction("Lenght", self)
        # #LenghtPath.setShortcut("Ctrl+L")
        # startSim.addAction(LenghtPath)
        # LenghtPath.triggered.connect(self.EstLenght)

        ConectarMultiple = QAction("Crear rutas",self)
        startSim.addAction(ConectarMultiple)
        ConectarMultiple.triggered.connect(self.ConMul)

        SimLHD = QAction ("Simulacion LHD", self)
        startSim.addAction (SimLHD)
        SimLHD.triggered.connect (self.LHDSim)

        RevisarRutas = QAction ("Revisar rutas", self)
        startSim.addAction (RevisarRutas)
        RevisarRutas.triggered.connect (self.RevRutas)

        Teniente = QAction("Teniente",self)
        #Teniente.setShortcut("Ctrl+T")
        panelBuilder.addAction(Teniente)
        Teniente.triggered.connect(self.TenientePanel)

        CamTiempoSim = QAction ("Cambiar tiempo simulacion", self)
        Charts.addAction (CamTiempoSim)
        CamTiempoSim.triggered.connect (self.CambioTiempo)

        PrMxTotal = QAction("Prod. min. total",self)
        Charts.addAction(PrMxTotal)
        PrMxTotal.triggered.connect(self.GrProdTotal)

        PrMxLHD = QAction("Prod. min. LHDs",self)
        Charts.addAction(PrMxLHD)
        PrMxLHD.triggered.connect(self.GrProdLHD)

        PrCuTotal = QAction("Prod. cu total",self)
        Charts.addAction (PrCuTotal)
        PrCuTotal.triggered.connect(self.GrProdCuTotal)

        PrCuLHD = QAction("Prod. cu LHDs",self)
        Charts.addAction (PrCuLHD)
        PrCuLHD.triggered.connect(self.GrProdCuLHD)

        PunExtSim = QAction("Puntos de extraccion",self)
        Charts.addAction (PunExtSim)
        PunExtSim.triggered.connect(self.GrPunExt)

        FuelLHDSim = QAction("Combustible",self)
        Charts.addAction (FuelLHDSim)
        FuelLHDSim.triggered.connect(self.GrFuel)

        ChLHDMaxSpeed = QAction("LHD Vel Max", self)
        Config.addAction(ChLHDMaxSpeed)
        ChLHDMaxSpeed.triggered.connect(self.c_LHDMaxSpeed)

        ChLHDaccel = QAction("LHD Acel.", self)
        Config.addAction(ChLHDaccel)
        ChLHDaccel.triggered.connect(self.c_LHDaccel)

        ChLHDdesaccel = QAction("LHD Desacel.", self)
        Config.addAction(ChLHDdesaccel)
        ChLHDdesaccel.triggered.connect(self.c_LHDdesaccel)

        ChLHDcapacity = QAction("LHD Capacidad", self)
        Config.addAction(ChLHDcapacity)
        ChLHDcapacity.triggered.connect(self.c_LHDcapacity)

        ChLHDMax_PEwaitTime = QAction("LHD T. Esp. PE", self)
        Config.addAction(ChLHDMax_PEwaitTime)
        ChLHDMax_PEwaitTime.triggered.connect(self.c_LHD_PEwaitTime)

        ChLHDMax_PVwaitTime = QAction("LHD T. Esp. PV", self)
        Config.addAction(ChLHDMax_PVwaitTime)
        ChLHDMax_PVwaitTime.triggered.connect(self.c_LHD_PVwaitTime)

        ChLHDFuelCap = QAction("LHD Fuel Max", self)
        Config.addAction(ChLHDFuelCap)
        ChLHDFuelCap.triggered.connect(self.c_LHDFuelCap)

        ChLHDRefuelDistance = QAction("LHD Fuel Dist.", self)
        Config.addAction(ChLHDRefuelDistance)
        ChLHDRefuelDistance.triggered.connect(self.c_LHDRefuelDistance)

        ChLHDRefuelWaitTime = QAction("LHD Fuel T. Espera", self)
        Config.addAction(ChLHDRefuelWaitTime)
        ChLHDRefuelWaitTime.triggered.connect(self.c_LHDRefuelWaitTime)

        ChPEMaterial = QAction("PE Material", self)
        Config.addAction(ChPEMaterial)
        ChPEMaterial.triggered.connect(self.c_PE_Material)

        ChPE_cu_ore = QAction("PE Ley cu", self)
        Config.addAction(ChPE_cu_ore)
        ChPE_cu_ore.triggered.connect(self.c_PEcu_ore)

        allLHD = QAction("Todos los LHD", self)
        Config.addAction(allLHD)
        allLHD.triggered.connect(self.todosLHDs)

        allPE = QAction("Todos los PE", self)
        Config.addAction(allPE)
        allPE.triggered.connect(self.todosPE)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

            print(self.lastPoint)

    def mouseMoveEvent(self, event):
        self.setMouseTracking (True)
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

        x = event.pos().x()
        y = event.pos().y()
        #print ([x,y])
        self.statusBar ().showMessage (" Mouse: %d / %d " % (x, y))
        self.update()


    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False
        if self.brushColor == Qt.green:
            self.drawing = True
            print("nowGreen")
            #print (self.lastPoint)
            paint = QPainter(self.image)
            paint.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            clickedpointx = event.pos().x()
            clickedpointy = event.pos().y()
            #print ([clickedpointx,clickedpointy])
            #self.chosen_points.append(cursor_event.pos())
            paint.drawPoint(QPoint(clickedpointx,clickedpointy))
            self.update()
            try:
                i = self.greenList[-1][0]+1
            except:
                IndexError
                i = 0
            self.greenList.append([i,clickedpointx,clickedpointy])
            print (self.greenList)

        if self.brushColor == Qt.blue:
            self.drawing = True
            print("nowBlue")
            #print (self.lastPoint)
            paint = QPainter(self.image)
            paint.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            clickedpointx = event.pos().x()
            clickedpointy = event.pos().y()
            #print ([clickedpointx,clickedpointy])
            #self.chosen_points.append(cursor_event.pos())
            paint.drawPoint(QPoint(clickedpointx,clickedpointy))
            self.update()
            try:
                i = self.blueList[-1][0]+1
            except:
                IndexError
                i = 0
            self.blueList.append([i,clickedpointx,clickedpointy])
            print (self.blueList)

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        filePath, _= QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)")
        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def onePx(self):
        self.brushSize = 1

    def threePx(self):
        self.brushSize = 3

    def fivePx(self):
        self.brushSize = 5

    def ninePx(self):
        self.brushSize = 9

    def blackBrush(self):
        self.brushColor = Qt.black

    def greenBrush(self):
        self.brushColor = Qt.green

    def blueBrush(self):
        self.brushColor = Qt.blue

    def whiteBrush(self):
        self.brushColor = Qt.white

    def simStart(self):
        rows = self.image.height()
        columns = self.image.width()
        fid = open("newBlockModel.txt", "w+")
        maze = [[0 for x in range(columns)] for y in range(rows)]
        start = ()
        end = ()
        for i in range(rows):
            for j in range(columns):
                if (self.image.pixel(j, i) == 4294967295):
                    n = int(1)
                else:
                    n = int(0)
                    if self.image.pixel(j, i) == 4278255360:
                        start = (i, j)
                    if self.image.pixel(j, i) == 4278190335:
                        end = (i, j)

                #fid.write(str(n) + ":" + str(self.image.pixel(j,i)) + ", ")
                maze[i][j] = n
        path = astar(maze,start,end)

        print ("ok")
        d = 0
        ap = 0

        for a, b in path:
            # print(a,b)
            # pixel = (a,b)
            if ap == 0:
                d += 0
            elif ap != a and bp != b:
                d += np.sqrt(2)
            else:
                d += 1.0
            QImage.setPixel (self.image, b + 1, a + 1, QColor (255, 0, 0, 255).rgb ())
            QImage.setPixel (self.image, b - 1, a - 1, QColor (255, 0, 0, 255).rgb ())
            QImage.setPixel (self.image, b + 1, a - 1, QColor (255, 0, 0, 255).rgb ())
            QImage.setPixel (self.image, b - 1, a + 1, QColor (255, 0, 0, 255).rgb ())
            # QPainter.drawPoint(self.image,b,a)
            ap = a
            bp = b
        self.update ()

        # print(maze)
        fid.close ()
        print ("ended")
        print ("Pixeles de ruta: ", len (path))
        print ("Distancia de ruta:", d)

            #fid.write("\n")
        #Pathfinding.maze = maze
        #pf.start = start
        #pf.end = end
    #def getMaze(self,start,end,maze):

    def ConMul(self):
        rows = self.image.height ()
        columns = self.image.width ()
        fid = open ("newBlockModel.txt", "w+")
        maze = [[0 for x in range (columns)] for y in range (rows)]
        start = ()
        end = ()
        for i in range (rows):
            for j in range (columns):
                if (self.image.pixel (j, i) == 4294967295):
                    n = int (1)
                else:
                    if self.image.pixel (j, i) == 4278255360:
                        start = (i, j)
                        n = int (0)

                    elif self.image.pixel (j, i) == 4278190335:
                        end = (i, j)
                        n = int (0)

                    else:
                        n = int (0)

                maze[i][j] = n
        print(start)
        print(end)


        for i in self.greenList:
            PERe = PuntoExtraccion('PE: ' + str(i[0]), i[1], i[2])
            # print (i, LHDRe)
            self.PEdict[i[0]] = PERe

        print(self.PEdict)

        for i in self.blueList:
            PVRe = PuntoVaciado ('PV: ' + str(i[0]), i[1], i[2])
            # print (record, PVRe)
            self.PVdict[i[0]] = PVRe

        print(self.PVdict)

        AllRoutes = []

        print ("startPath")

        print(PuntoExtraccion._registry)
        print(PuntoVaciado._registry)

        record = 0
        for i in PuntoExtraccion._registry:
            for j in PuntoVaciado._registry:
                print ("Objeto PE, PV:",i,j)
                start = (i.coordY,i.coordX)
                print (i.coordX,i.coordY)
                end = (j.coordY,j.coordX)
                path = astar (maze, start, end)
                RutaRe = Ruta (i, j, 'Ruta: ' + str (record))
                self.RutaDict[record] = RutaRe
                record = record + 1

                AllRoutes.append(path)

        print("All routes:", AllRoutes)

        record = 0
        for route in AllRoutes:
            print ("Route:",route)
            d = 0
            ap = 0

            for a, b in route:
                # print(a,b)
                # pixel = (a,b)
                if ap == 0:
                    d += 0
                elif ap != a and bp != b:
                    d += np.sqrt (2)
                else:
                    d += 1.0
                QImage.setPixel (self.image, b + 1, a + 1, QColor (255, 0, 0, 255).rgb ())
                QImage.setPixel (self.image, b - 1, a - 1, QColor (255, 0, 0, 255).rgb ())
                QImage.setPixel (self.image, b + 1, a - 1, QColor (255, 0, 0, 255).rgb ())
                QImage.setPixel (self.image, b - 1, a + 1, QColor (255, 0, 0, 255).rgb ())
                ap = a
                bp = b
            self.update ()
            print (d)
            self.RutaDict[record].Distance = d
            record = record + 1

        print ("Con. Multiple Done")


    def LHDSim(self):
        printRutas ()
        nRutas = len(Ruta._registry) - 1

        nLHD, ok = QInputDialog.getInt (self, "Input", "¿Cuantos LHD quiere simular?", 1, 1, 100, 1)

        if ok:
            for record in range (nLHD):
                LHDRe = LHD ('LHD: ' + str (record))
                #print (record, LHDRe)
                self.LHDdict[record] = LHDRe

            for LHDobject in LHD._registry:
                Q = 0
                cicloLHD = []
                while Q != "n":
                    sRuta, ok = QInputDialog.getInt (self, LHDobject.name, "Seleccione una ruta para agregar al ciclo del LHD", 0, 0, nRutas, 1)
                    if ok:
                        items = ["Punto de vaciado", "Punto de extraccion"]
                        item, ok = QInputDialog.getItem (self, LHDobject.name,
                                                         "¿A punto de vaciado o de extracción?", items, 0, False)
                        if ok:
                            print (LHDobject.name, " Ruta:", sRuta, " ", item)
                            # print (items[0])
                            # print (items[1])
                            VoE = 0
                            if item == items[0]:
                                VoE = "v"
                            if item == items[1]:
                                VoE = "e"
                            CompCiclo = [self.RutaDict[sRuta], VoE]
                            cicloLHD.append(CompCiclo)
                            items2 = ["Si","No"]
                            item, ok = QInputDialog.getItem (self, LHDobject.name,
                                                                 "¿Agregar otro destino al ciclo del LHD?", items2, 0,
                                                                 False)
                            if item == items2[1]:
                                Q = "n"
                LHDobject.routeList = cicloLHD
                print (LHDobject.routeList)

        for LHDobject in LHD._registry:
            LHDobject.cicleSpeed ()

        print ("registry success!")

    def RevRutas(self):
        printRutas()

    def TenientePanel(self, event):
        self.drawing = True
        self.brushColor = Qt.black
        paint = QPainter(self.image)
        paint.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        iniciox = 50
        inicioy = 50
        ha = 80
        b = 30
        a = 30
        x1,y1 = iniciox, inicioy
        x2,y2 = iniciox+a, inicioy+ha
        x3,y3 = iniciox+a+b, inicioy+ha
        x4,y4 = iniciox+b, inicioy
        points = QPolygon([QPoint(x1, y1), QPoint(x2, y2), QPoint(x3, y3), QPoint(x4, y4)])
        paint.drawPolygon(points)

        rh = 16
        rv = 6

        for i in range(0,rv,1):
            for j in range(0,rh,1):
                inicioxS = iniciox + (b * j) + (a * i)
                inicioyS = inicioy + (ha * i)
                x1, y1 = inicioxS, inicioyS
                x2, y2 = inicioxS + a, inicioyS + ha
                x3, y3 = inicioxS + a + b, inicioyS + ha
                x4, y4 = inicioxS + b, inicioyS
                points = QPolygon([QPoint(x1, y1), QPoint(x2, y2), QPoint(x3, y3), QPoint(x4, y4)])
                paint.drawPolygon(points)

        self.update()
        self.drawing = False

    def CambioTiempo(self):
        tSim, ok = QInputDialog.getInt (self, "Gopher Underground", "Tiempo de simulacion (minutos).\nMax: 1440:", 120, 0, 1440, 1)
        if ok:
            self.tiempoSim = tSim

    def GrProdTotal(self):
        tiempo = self.tiempoSim
        ProdTotal(tiempo)

    def GrProdLHD(self):
        tiempo = self.tiempoSim
        ProdLHDindividual(tiempo)

    def GrProdCuTotal(self):
        tiempo = self.tiempoSim
        ProdTotalCu(tiempo)

    def GrProdCuLHD(self):
        tiempo = self.tiempoSim
        ProdLHDindividualCu(tiempo)

    def GrPunExt(self):
        tiempo = self.tiempoSim
        SimPuntoExt(tiempo)

    def GrFuel(self):
        tiempo = self.tiempoSim
        fuelSim(tiempo)

    def EstLenght(self,event):
        call = d
        print(call)

    def c_LHDMaxSpeed(self):
        nLHD = len (LHD._registry) - 1
        sLHD, ok = QInputDialog.getInt (self, "Gopher Underground", "Seleccione el LHD: ", 0,
                                         0, nLHD, 1)
        if ok:
            string = "Nuevo valor de Vel. Maxima (m/s):"
            new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 16, 1, 100, 1)
            self.LHDdict[sLHD].max_speed = new

    def c_LHDaccel(self):
        nLHD = len (LHD._registry) - 1
        sLHD, ok = QInputDialog.getInt (self, "Gopher Underground", "Seleccione el LHD: ", 0,
                                         0, nLHD, 1)
        if ok:
            string = "Nuevo valor de aceleracion (m/s):"
            new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 2, 1, 100, 1)
            self.LHDdict[sLHD].accel = new

    def c_LHDdesaccel(self):
        nLHD = len (LHD._registry) - 1
        sLHD, ok = QInputDialog.getInt (self, "Gopher Underground", "Seleccione el LHD: ", 0,
                                        0, nLHD, 1)
        if ok:
            string = "Nuevo valor de desaceleracion (m/s):"
            new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 2, 1, 100, 1)
            self.LHDdict[sLHD].desaccel = new

    def c_LHDcapacity(self):
        nLHD = len (LHD._registry) - 1
        sLHD, ok = QInputDialog.getInt (self, "Gopher Underground", "Seleccione el LHD: ", 0,
                                        0, nLHD, 1)
        if ok:
            string = "Nuevo valor de capacidad (tons.):"
            new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 20, 1, 100, 1)
            self.LHDdict[sLHD].capacity = new

    def c_LHD_PEwaitTime(self):
        nLHD = len (LHD._registry) - 1
        sLHD, ok = QInputDialog.getInt (self, "Gopher Underground", "Seleccione el LHD: ", 0,
                                        0, nLHD, 1)
        if ok:
            string = "Nuevo valor de espera en puntos de extaccion (segs.):"
            new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 20, 1, 500, 1)
            self.LHDdict[sLHD].PEwaitTime = new

    def c_LHD_PVwaitTime(self):
        nLHD = len (LHD._registry) - 1
        sLHD, ok = QInputDialog.getInt (self, "Gopher Underground", "Seleccione el LHD: ", 0,
                                        0, nLHD, 1)
        if ok:
            string = "Nuevo valor de espera en puntos de vaciado (segs.):"
            new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 10, 1, 500, 1)
            self.LHDdict[sLHD].PVwaitTime = new

    def c_LHDFuelCap(self):
        nLHD = len (LHD._registry) - 1
        sLHD, ok = QInputDialog.getInt (self, "Gopher Underground", "Seleccione el LHD: ", 0,
                                        0, nLHD, 1)
        if ok:
            string = "Nuevo valor de capacidad de combustible (mts.):"
            new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 3500, 1, 10000, 1)
            self.LHDdict[sLHD].FuelCap = new

    def c_LHDRefuelDistance(self):
        nLHD = len (LHD._registry) - 1
        sLHD, ok = QInputDialog.getInt (self, "Gopher Underground", "Seleccione el LHD: ", 0,
                                        0, nLHD, 1)
        if ok:
            string = "Nuevo valor de distancia para reabastecimiento de combustible (mts.):"
            new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 200, 1, 10000, 1)
            self.LHDdict[sLHD].refuelDistance = new

    def c_LHDRefuelWaitTime(self):
        nLHD = len (LHD._registry) - 1
        sLHD, ok = QInputDialog.getInt (self, "Gopher Underground", "Seleccione el LHD: ", 0,
                                        0, nLHD, 1)
        if ok:
            string = "Nuevo valor de tiempo de espera para reabastecimiento de combustible (segs.):"
            new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 200, 1, 5000, 1)
            self.LHDdict[sLHD].refuelWaitTime = new


    def c_PE_Material(self):
        nPE = len (PuntoExtraccion._registry) - 1
        sPE, ok = QInputDialog.getInt (self, "Gopher Underground", "Seleccione el Punto de Extraccion: ", 0,
                                         0, nPE, 1)
        if ok:
            string = "Nuevo valor de material (tons.):"
            new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 500, 1, 50000, 1)
            self.PEdict[sPE].setMaterial(new)

    def c_PEcu_ore(self):
        nPE = len (PuntoExtraccion._registry) - 1
        sPE, ok = QInputDialog.getInt (self, "Gopher Underground", "Seleccione el Punto de Extraccion: ", 0,
                                         0, nPE, 1)
        if ok:
            string = "Nuevo valor de ley de cobre (%):"
            new, ok = QInputDialog.getDouble(self, "Gopher Underground", string, 0.5, 0, 100, 2)
            self.PEdict[sPE].cu_ore = new

    def todosLHDs(self):
        items = ["Vel. maxima", "Aceleracion", "Desaceleracion", "Capacidad", "Tiempo de espera en puntos de extraccion",
                 "Tiempo de espera en puntos de vaciado", "Combustible (mts)", "Distancia de recarga de combustible",
                 "Tiempo de espera recarga de combustible"]
        item, ok = QInputDialog.getItem (self, "Gopher Underground",
                                         "¿Que desea cambiar?:", items, 0, False)
        if ok:
            if item == items[0]:
                string = "Nuevo valor de Vel. Maxima (m/s):"
                new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 16, 1, 100, 1)
                for LHDobject in LHD._registry:
                    LHDobject.max_speed = new

            if item == items[1]:
                string = "Nuevo valor de aceleracion (m/s):"
                new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 2, 1, 100, 1)
                for LHDobject in LHD._registry:
                    LHDobject.accel = new

            if item == items[2]:
                string = "Nuevo valor de desaceleracion (m/s):"
                new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 2, 1, 100, 1)
                for LHDobject in LHD._registry:
                    LHDobject.desaccel = new

            if item == items[3]:
                string = "Nuevo valor de capacidad (tons.):"
                new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 20, 1, 100, 1)
                for LHDobject in LHD._registry:
                    LHDobject.capacity = new

            if item == items[4]:
                string = "Nuevo valor de espera en puntos de extaccion (segs.):"
                new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 20, 1, 500, 1)
                for LHDobject in LHD._registry:
                    LHDobject.PEwaitTime = new

            if item == items[5]:
                string = "Nuevo valor de espera en puntos de vaciado (segs.):"
                new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 10, 1, 500, 1)
                for LHDobject in LHD._registry:
                    LHDobject.PVwaitTime = new

            if item == items[6]:
                string = "Nuevo valor de capacidad de combustible (mts.):"
                new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 3500, 1, 10000, 1)
                for LHDobject in LHD._registry:
                    LHDobject.FuelCap = new

            if item == items[7]:
                string = "Nuevo valor de distancia para reabastecimiento de combustible (mts.):"
                new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 200, 1, 10000, 1)
                for LHDobject in LHD._registry:
                    LHDobject.refuelDistance = new

            if item == items[8]:
                string = "Nuevo valor de tiempo de espera para reabastecimiento de combustible (mts.):"
                new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 200, 1, 5000, 1)
                for LHDobject in LHD._registry:
                    LHDobject.refuelWaitTime = new

    def todosPE(self):
        items = ["Material", "Ley de cobre"]
        item, ok = QInputDialog.getItem (self, "Gopher Underground",
                                         "¿Que desea cambiar?:", items, 0, False)
        if ok:
            if item == items[0]:
                string = "Nuevo valor de material (tons.):"
                new, ok = QInputDialog.getInt (self, "Gopher Underground", string, 500, 1, 50000, 1)
                for PEobject in PuntoExtraccion._registry:
                    PEobject.setMaterial (new)

            if item == items[1]:
                string = "Nuevo valor de ley de cobre (%):"
                new, ok = QInputDialog.getDouble (self, "Gopher Underground", string, 0.5, 0, 100, 2)
                for PEobject in PuntoExtraccion._registry:
                    PEobject.cu_ore = new


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

class LHD(object):
    __metaclass__ = IterRegistry
    _registry = []
    name = ""
    routeList = []
    itinerary = []
    def __init__(self, name = "", routeList = []):
        self._registry.append(self)
        self.routeList = routeList
        self.name = name

        self.max_speed = 16 #m/s
        self.accel = 2 #m/s
        self.desaccel = 2 #m/s

        self.capacity = 20 #tons

        self.PEwaitTime = 20 #segundos
        self.PVwaitTime = 10 #segundos

        self.FuelCap = 3500 #mts
        self.refuelDistance = 200 #mts
        self.refuelWaitTime = 200 #segundos

    def cicleSpeed(self):
        routeList = self.routeList
        print ("Self Route List ", routeList)
        max_speed = self.max_speed
        accel = self.accel
        desaccel = self.desaccel

        itinerary = []
        #print (max_speed,accel,desaccel)

        for i in self.routeList:
            print ("i: ", i)
            dist = i[0].Distance
            print ("Distancia: ", dist)
            load = self.capacity
            #print (dist)
            aTime = np.sqrt (dist * (2 * desaccel) / ((accel + desaccel) * accel))
            velF = aTime*accel
            #print(aTime,velF)
            if velF > max_speed:
                distanceA = 0.5 * accel *(max_speed // accel)**2
                distanceD = 0.5 * desaccel *(max_speed // desaccel)**2
                TimeA = np.sqrt (2 * distanceA / accel)
                TimeD = np.sqrt (2 * distanceD / desaccel)
                TimeK = (dist - (distanceA + distanceD)) / max_speed
                cicleTime = TimeA + TimeD + TimeK
                print (cicleTime)
            else:
                cicleTime = np.sqrt(dist*(2*desaccel)/((accel+desaccel)*accel)) + np.sqrt(dist*(2*accel)/((desaccel+accel)*desaccel))
                print (cicleTime)

            itinerary.append([cicleTime,i[1],i[0], dist])

        self.itinerary = itinerary
        #print(self.itinerary)




class PuntoExtraccion(object):
    __metaclass__ = IterRegistry
    _registry = []
    name = ""
    coordX = 0
    coordY = 0
    def __init__(self, name = "", coordX = 0, coordY = 0, Material = 500, cu_ore = 0.5):
        self._registry.append(self)
        self.name = name
        self.__material = Material
        self.SimMaterial = Material
        self.cu_ore = cu_ore  # %
        self.coordX = coordX
        self.coordY = coordY

    def RefillMaterial(self):
        self.SimMaterial = self.__material

    def setMaterial(self, newMaterial):
        self.__material = newMaterial
        self.SimMaterial = self.__material

class PuntoVaciado(object):
    __metaclass__ = IterRegistry
    _registry = []
    name = ""
    coordX = 0
    coordY = 0
    def __init__(self, name, coordX = 0, coordY = 0):
        self._registry.append(self)
        self.name = name
        self.coordX = coordX
        self.coordY = coordY

class Ruta (object):
    __metaclass__ = IterRegistry
    _registry = []
    name = ""
    PExt = 0
    PVac = 0
    Distance = 0
    def __init__(self, PExt, PVac, name = "", Distance=0):
        self._registry.append(self)
        self.name = name
        self.Distance = Distance
        self.PExt = PExt
        self.PVac = PVac

def printRutas():
    for rutaObject in Ruta._registry:
        print(rutaObject.name," ", rutaObject.PExt.name, (rutaObject.PExt.coordX,rutaObject.PExt.coordY), " ",
              rutaObject.PVac.name, (rutaObject.PVac.coordX,rutaObject.PVac.coordY), "  Dist:", round(rutaObject.Distance, 2))
    print("")


def fullciclo(tiempo = 120):
    tsecs = tiempo * 60
    fullSim = []
    fPE_Sim = []

    for LHDobject in LHD._registry:
        LHDSim = []
        PE_Sim = []
        Time = 0
        fuel = LHDobject.FuelCap
        LHDcargo = 0
        while Time < tsecs:
            for j in LHDobject.itinerary:
                if j[1] == "v": # j[1] = VoE
                    if Time == 0:
                        LHDSim.append ([Time, LHDobject.name, j[1], 0, 0, j[2], fuel, 0]) # j[2] = Ruta
                        PE_Sim.append ([Time, j[2].PExt, j[2].PExt.SimMaterial, (j[2].PExt.SimMaterial*j[2].PExt.cu_ore)/100])
                        ExtraTime = LHDobject.PEwaitTime
                        matPExt = j[2].PExt.SimMaterial
                        LHDcargo = min (LHDobject.capacity, matPExt)
                        j[2].PExt.SimMaterial = matPExt - LHDcargo
                        Time = Time + ExtraTime
                        LHDSim.append ([Time, LHDobject.name, j[1], -LHDcargo, 0, j[2], fuel, 0])
                        PE_Sim.append ([Time, j[2].PExt, j[2].PExt.SimMaterial, (j[2].PExt.SimMaterial*j[2].PExt.cu_ore)/100])
                    ExtraTime = j[0]
                    if fuel < (LHDobject.refuelDistance+j[3]):
                        ExtraTime = ExtraTime + LHDobject.refuelWaitTime
                        fuel = LHDobject.FuelCap - LHDobject.refuelDistance
                    fuel = fuel - j[3]
                    Time = Time + ExtraTime
                    if Time > tsecs:
                        break
                    LHDSim.append ([Time, LHDobject.name, j[1], 0, 0, j[2], fuel, 0])
                    PE_Sim.append ([Time, j[2].PExt, j[2].PExt.SimMaterial, (j[2].PExt.SimMaterial*j[2].PExt.cu_ore)/100])
                    ExtraTime = LHDobject.PVwaitTime
                    Time = Time + ExtraTime
                    if Time > tsecs:
                        break
                    LHDSim.append ([Time, LHDobject.name, j[1], 0, LHDcargo, j[2], fuel, (LHDcargo*j[2].PExt.cu_ore)/100])
                    PE_Sim.append ([Time, j[2].PExt, j[2].PExt.SimMaterial, (j[2].PExt.SimMaterial*j[2].PExt.cu_ore)/100])
                    if j[2].PExt.SimMaterial == 0:
                        LHDSim.append ([Time, "break", "break", "break", "break", "break", "break"])
                        PE_Sim.append ([Time, "break", "break", "break", "break", "break", "break"])
                if j[1] == "e":
                    if Time == 0:
                        LHDSim.append ([Time, LHDobject.name, j[1], 0, 0, j[2],fuel, 0])
                        PE_Sim.append ([Time, j[2].PExt, j[2].PExt.SimMaterial, (j[2].PExt.SimMaterial*j[2].PExt.cu_ore)/100])
                    ExtraTime = j[0]
                    if fuel < (LHDobject.refuelDistance + j[3]):
                        ExtraTime = ExtraTime + LHDobject.refuelWaitTime
                        fuel = LHDobject.FuelCap - LHDobject.refuelDistance
                    fuel = fuel - j[3]
                    Time = Time + ExtraTime
                    if Time > tsecs:
                        break
                    LHDSim.append ([Time, LHDobject.name, j[1], 0, 0, j[2], fuel, 0])
                    PE_Sim.append ([Time, j[2].PExt, j[2].PExt.SimMaterial, (j[2].PExt.SimMaterial*j[2].PExt.cu_ore)/100])
                    ExtraTime = LHDobject.PEwaitTime
                    Time = Time + ExtraTime
                    if Time > tsecs:
                        break
                    matPExt = j[2].PExt.SimMaterial
                    LHDcargo = min (LHDobject.capacity, matPExt)
                    j[2].PExt.SimMaterial = matPExt - LHDcargo
                    LHDSim.append ([Time, LHDobject.name, j[1], -LHDcargo, 0, j[2], fuel, 0])
                    PE_Sim.append ([Time, j[2].PExt, j[2].PExt.SimMaterial, (j[2].PExt.SimMaterial*j[2].PExt.cu_ore)/100])
            if Time > tsecs:
                break
        fullSim.append(LHDSim)
        fPE_Sim.append(PE_Sim)

    print("Full Sim", fullSim)
    print("fPE Sim", fPE_Sim)
    return fullSim, fPE_Sim

def ProdTotal(tiempo = 120):
    for LHDobject in LHD._registry:
        LHDobject.cicleSpeed ()

    for PExtraccion in PuntoExtraccion._registry:
        PExtraccion.RefillMaterial()

    fullArray, PE_Sim = fullciclo(tiempo)
    funcfullArray = fullArray
    concatArray = []
    n = 0

    for ciclo in funcfullArray:
        # for item in ciclo:
        #     if i[4] > 0:
        concatArray = ciclo + concatArray

    concatArray.sort(key = lambda x: x[0])
    print(concatArray)

    producto = 0
    timeArr = []
    prodArr = []
    for i in concatArray:
        if i[1] == "break":
            break
        time = i[0] / 60
        producto = producto + i[4]

        timeArr.append(time)
        prodArr.append(producto)
    print (len(timeArr))
    fig = plt.figure ()
    ax = plt.axes ()

    ax.plot (timeArr, prodArr)
    plt.show()
    plt.savefig ('MxProdTotalChart.png')

def ProdLHDindividual(tiempo = 120):
    for LHDobject in LHD._registry:
        LHDobject.cicleSpeed ()

    for PExtraccion in PuntoExtraccion._registry:
        PExtraccion.RefillMaterial()

    fullArray, PE_Sim = fullciclo(tiempo)

    ProdLHDListas = []
    for lhd in range(len(LHD._registry)):
        lhdArray = fullArray[lhd]
        producto = 0
        timeArr = []
        prodArr = []
        for i in lhdArray:
            if i[1] == "break":
                break
            time = i[0] / 60
            producto = producto + i[4]

            timeArr.append(time)
            prodArr.append(producto)
        ProdLHDListas.append((timeArr,prodArr))
    fig = plt.figure ()
    ax = plt.axes ()

    for i,j in ProdLHDListas:
        ax.plot (i, j)

    names = []
    for item in LHD._registry:
        names.append(item.name)
    plt.legend(names)
    plt.show()
    plt.savefig ('MxLHDChart.png')

def ProdTotalCu(tiempo = 120):
    for LHDobject in LHD._registry:
        LHDobject.cicleSpeed ()

    for PExtraccion in PuntoExtraccion._registry:
        PExtraccion.RefillMaterial()

    fullArray, PE_Sim = fullciclo(tiempo)
    concatArray = []
    n = 0

    for ciclo in fullArray:
        # for item in ciclo:
        #     if i[4] > 0:
        concatArray = ciclo + concatArray

    concatArray.sort(key = lambda x: x[0])
    print(concatArray)

    producto = 0
    timeArr = []
    prodArr = []
    for i in concatArray:
        if i[1] == "break":
            break
        time = i[0] / 60
        producto = producto + i[7]

        timeArr.append(time)
        prodArr.append(producto)
    print (len(timeArr))
    fig = plt.figure ()
    ax = plt.axes ()

    ax.plot (timeArr, prodArr)
    plt.show()
    plt.savefig ('CuTotalChart.png')

def ProdLHDindividualCu(tiempo = 120):
    for LHDobject in LHD._registry:
        LHDobject.cicleSpeed ()

    for PExtraccion in PuntoExtraccion._registry:
        PExtraccion.RefillMaterial()

    fullArray, PE_Sim = fullciclo(tiempo)

    ProdLHDListas = []
    for lhd in range(len(LHD._registry)):
        lhdArray = fullArray[lhd]
        producto = 0
        timeArr = []
        prodArr = []
        for i in lhdArray:
            if i[1] == "break":
                break
            time = i[0] / 60
            producto = producto + i[7]

            timeArr.append(time)
            prodArr.append(producto)
        ProdLHDListas.append((timeArr,prodArr))
    fig = plt.figure ()
    ax = plt.axes ()

    for i,j in ProdLHDListas:
        ax.plot (i, j)

    names = []
    for item in LHD._registry:
        names.append(item.name)
    plt.legend(names)
    plt.show()
    plt.savefig ('CuLHDChart.png')

def SimPuntoExt(tiempo = 120):
    for LHDobject in LHD._registry:
        LHDobject.cicleSpeed ()

    for PExtraccion in PuntoExtraccion._registry:
        PExtraccion.RefillMaterial()

    fullArray, PE_Sim = fullciclo (tiempo)
    concatArray = []
    n = 0

    for ciclo in PE_Sim:
        #print (ciclo)
        concatArray = ciclo + concatArray

    concatArray.sort(key = lambda x: x[0])

    simPExt = []
    for PExt in PuntoExtraccion._registry:
        timeArray = []
        extArray = []
        for item in concatArray:
            if item[1] == "break":
                break
            if PExt == item[1]:
                time = item[0] / 60
                ext = item[2]
                timeArray.append(time)
                extArray.append(ext)
        simPExt.append([timeArray, extArray])

    fig1 = plt.figure (0)
    ax1 = plt.axes ()
    #print (simPExt)

    for i, j in simPExt:
        #print (i,j)
        ax1.plot (i, j)

    names = []
    for item in PuntoExtraccion._registry:
        names.append (item.name)
    plt.legend (names)

    plt.savefig ('PExtChart.png')
    plt.show ()

def fuelSim(tiempo = 120):
    for LHDobject in LHD._registry:
        LHDobject.cicleSpeed ()

    for PExtraccion in PuntoExtraccion._registry:
        PExtraccion.RefillMaterial()

    fullArray, PE_Sim = fullciclo(tiempo)

    ProdLHDListas = []
    for lhd in range(len(LHD._registry)):
        lhdArray = fullArray[lhd]
        timeArr = []
        fuelArr = []
        for i in lhdArray:
            if i[1] == "break":
                break
            time = i[0] / 60
            fuel = i[6]

            timeArr.append(time)
            fuelArr.append(fuel)
        ProdLHDListas.append((timeArr,fuelArr))
    fig = plt.figure ()
    ax = plt.axes ()

    for i,j in ProdLHDListas:
        ax.plot (i, j)

    names = []
    for item in LHD._registry:
        names.append(item.name)
    plt.legend(names)
    plt.show()
    plt.savefig ('FuelChart.png')


# class MouseCoordinates (QLabel):
#
#     def __init__(self, parent=None):
#         super (MouseCoordinates, self).__init__ (parent)
#         self.setMouseTracking (True)
#
#         self.update ()
#
#     def update(self):
#         currentPos = QCursor.pos ()
#
#         x = currentPos.x ()
#         y = currentPos.y ()
#
#         self.setText (" Mouse: %d / %d " % (x, y))
#
#
# class StatusBar (QStatusBar):
#
#     def __init__(self, parent=None):
#         super (StatusBar, self).__init__ (parent)
#         self.setMouseTracking (True)
#
#         self.mouseCoords = MouseCoordinates ()
#
#         self.addWidget (self.mouseCoords)
#
#         self.update ()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()

