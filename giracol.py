#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Giracol

(C) Olivier Friard 2012

rewriting in python/pyqt of an old game created in Pascal/Delphi.


Giracol is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or any later version.

Giracol is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Giracol; see the file COPYING.TXT.  If not, write to
the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.

"""

__version__ = '2'

import sys, random
from PyQt4 import QtGui, QtCore

class Giracol(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(Giracol, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Giracol')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        newGameAction = QtGui.QAction(QtGui.QIcon('new.png'), '&New game', self)
        newGameAction.setShortcut('Ctrl+N')
        newGameAction.setStatusTip('Create a new game')
        newGameAction.triggered.connect(self.newGame)
        fileMenu.addAction(newGameAction)

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        fileMenu.addAction(exitAction)

        helpMenu = menubar.addMenu('Help')
        
        helpAction = QtGui.QAction(QtGui.QIcon('help.png'), '&How to play', self)
        helpAction.setShortcut('F1')
        helpAction.setStatusTip('How to play')
        helpAction.triggered.connect(self.help)
        helpMenu.addAction(helpAction)


        aboutAction = QtGui.QAction(QtGui.QIcon('about.png'), '&About', self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.setStatusTip('About Giracol')
        aboutAction.triggered.connect(self.about)
        helpMenu.addAction(aboutAction)


        self.show()

        self.nx = 5
        self.ny = 5
        #self.col = [ QtCore.Qt.red, QtCore.Qt.blue, QtCore.Qt.green, QtCore.Qt.magenta, QtCore.Qt.yellow, QtGui.QColor(64,255,255) ]
        #[ QtGui.QColor(38,30,35),QtGui.QColor(46,54,61),QtGui.QColor(52,115,59),QtGui.QColor(99,176,0),QtGui.QColor(206,227,25),QtGui.QColor(38,30,35) ]
        shire = [(60,18,19),(43,71,13),(248,167,62),(34,36,49),(133,47,0)]
        
        self.col = []
        for c in shire:
            self.col.append(QtGui.QColor(c[0],c[1],c[2]))
        
        self.margin = 40
        
        self.vlist = [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]

        self.newGame()
       
    def help(self):
        QtGui.QMessageBox.information(self, 'Giracol', 'The goal is to align horizontally the tiles of the same color.<br>You can move the tiles by rotation around a single tile by clicking it.<br><b>Left click</b> rotates the tiles in the <b>anticlockwise</b> direction while <b>right click</b> rotates in the <b>clockwise</b> direction.<br><br>Have fun!')
        
    def about(self):

        QtGui.QMessageBox.about(self, 'Giracol', 'Olivier Friard 2012.<br>version %s' % __version__)

    def newGame(self):
        
        self.count = 0

        self.t = [ [ 0 for i in range(self.nx + 2) ] for j in range(self.ny + 2) ]

        for x in range(self.nx + 2):
            for y in range(self.ny + 2):
                self.t[x][y] = -1   ### no color

        for r in range(1, self.nx + 1):
            for c in range(1, self.ny + 1):
                x = random.randint(1, self.nx)
                y = random.randint(1, self.ny)

                while self.t[x][y] <> -1:
                    x = random.randint(1, self.nx)
                    y = random.randint(1, self.ny)
                self.t[x][y] = self.col[r - 1]
        self.update()
        self.statusBar().showMessage('Ready')
        

    def getGridParam(self):
        xmax = self.size().width() - self.margin 
        xmin = self.margin
        
        ymax = self.size().height() - self.margin 
        ymin = self.margin
        
        dx = (xmax - xmin) / self.nx *1.0
        dy = (ymax - ymin) / self.ny *1.0
        return xmin, xmax, ymin, ymax, dx, dy

    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawGrid(qp)
        qp.end()

    def verif(self):
        """
        test if position wins
        returns number of aligned tiles
        """
        # horizontally
        ch = 0
        for y in range(1, self.nx + 1):
            for x in range(1, self.ny + 1):
                #print x,y ,self.t[x][y] , self.t[x][1]
                if self.t[x][y] == self.t[1][y]:
                    ch += 1

        # vertically
        cv = 0
        for y in range(1, self.nx + 1):
            for x in range(1, self.ny + 1):
                #print x,y ,self.t[x][y] , self.t[x][1]
                if self.t[y][x] == self.t[y][1]:
                    cv += 1


        print 'Score:',max(ch, cv)
        return max(ch, cv)

    def mousePressEvent(self, ev):

        xm, ym = QtCore.QPoint(ev.pos()).x(),QtCore.QPoint(ev.pos()).y()

        xmin, xmax, ymin, ymax, dx, dy = self.getGridParam()

        if xm < xmin or xm > xmax or ym < ymin or ym > ymax:
            return

        self.count += 1
        self.statusBar().showMessage('%d moves' % self.count)

        xg = int((xm - self.margin)/dx) + 1
        yg = int((ym - self.margin)/dy) + 1
        
        neighbors = []
        for i in range(len(self.vlist)):
            v = self.vlist[i]

            if self.t[xg + v[0]][yg + v[1]] == -1:
                continue

            neighbors.append((xg + v[0],yg + v[1], self.t[xg + v[0]][yg + v[1]]) )

        if ev.button() == 1: ### left click
            for n in range(len(neighbors)):
                print n, neighbors[n]
                if n < len(neighbors) - 1:
                    self.t[neighbors[n][0]][neighbors[n][1]] = neighbors[n+1][2]
                else:
                    self.t[neighbors[n][0]][neighbors[n][1]] = neighbors[0][2]

        if ev.button() == 2: ### right click
            for n in range(len(neighbors)):
                if n > 0:
                    self.t[neighbors[n][0]][neighbors[n][1]] = neighbors[n - 1][2]
                else:
                    self.t[neighbors[n][0]][neighbors[n][1]] = neighbors[len(neighbors) - 1][2]

        self.update()  ### force paint event

        if self.verif() == self.nx * self.ny:
            QtGui.QMessageBox.information(self, 'Giracol', 'You solved it in %d moves!' % self.count)
            self.newGame()


    def drawGrid(self, qp):

        xmax = self.size().width() - self.margin 
        xmin = self.margin
        
        ymax = self.size().height() - self.margin 
        ymin = self.margin
        
        dx = (xmax - xmin) / self.nx *1.0
        dy = (ymax - ymin) / self.ny *1.0

        xmin, xmax, ymin, ymax, dx, dy = self.getGridParam()

        for x in range(1,self.nx+1):
            for y in range(1,self.ny+1):
                qp.fillRect(xmin + round(dx * (x-1)), ymin + round(dy *(y-1)), dx-3, dy-3, self.t[x][y]) 


app = QtGui.QApplication(sys.argv)
giracol = Giracol()
sys.exit(app.exec_())


