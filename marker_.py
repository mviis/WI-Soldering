import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image

class Canvas(QWidget):

    def __init__(self, *args, **kwargs,):
       
        super().__init__(*args, **kwargs)
        self.image = QImage("temp.png")
        self.pressed = self.moving = False
        self.revisions = []
        self.colorS = Qt.red

    def load_image(self, photo,w:int=0,h:int=0,):
        im = Image.open(photo)
        im.thumbnail((w,h), Image.ANTIALIAS)
        self.setFixedSize(w, h)
        im.save("temp.png", "PNG",quality=100, optimize=True)
        self.image = QImage("temp.png")
        
        self.revisions = []
        self.colorS = Qt.green


    def setColors(self,value):
        self.colorS = value

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = True
            self.center = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.moving = True
            r = (event.pos().x() - self.center.x()) ** 2 + (event.pos().y() - self.center.y()) ** 2
            self.radius = r ** 0.5
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.revisions.append(self.image.copy())
            qp = QPainter(self.image)
            self.draw_circle(qp) if self.moving else self.draw_point(qp)
            self.pressed = self.moving = False
            self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        rect = event.rect()
        qp.drawImage(rect, self.image, rect)
        if self.moving:
            self.draw_circle(qp)
        elif self.pressed:
            self.draw_point(qp)

    def draw_point(self, qp):
        qp.setPen(QPen(self.colorS, 5))
        qp.drawPoint(self.center)

    def draw_circle(self, qp):
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(QPen(self.colorS, 3, Qt.SolidLine))
        qp.drawEllipse(self.center, self.radius, self.radius)

  

    def undo(self):
        if self.revisions:
            self.image = self.revisions.pop()
            self.update()

    def reset(self):
        if self.revisions:
            self.image = self.revisions[0]
            self.revisions.clear()
            self.update()

    def save_image(self,fn,type_,val,w=1152,h=630):
        self.image.smoothScaled(w, h)
        self.image.save(fn,type_,val)