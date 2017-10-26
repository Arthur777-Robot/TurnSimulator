## -*- coding: utf-8 -*

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import math

class Draw(QGraphicsItem):
    def __init__(self,width=180, height=180, size=90):
        super(Draw,self).__init__()
        self.offsetx = 10
        self.offsety = 10
        self.width = width*2
        self.height = height*2
        self.size = size

        # this is the initial parameters for turn
        self.startx = 90
        self.starty = 90
        self.sla_start_x = 90
        self.sla_start_y =180 - 50
        self.tread = 63
        self.entry_vel = 1.0
        self.ang_accel = 0.01758
        self.weight = 0.070
        self.angvel_list = []
        self.pos_x_theo = []
        self.pos_y_theo = []
        self.pos_x_real = []
        self.pos_y_real = []
        self.r_tire_pos_x = []
        self.r_tire_pos_y = []
        self.l_tire_pos_x = []
        self.l_tire_pos_y = []

    def paint(self, painter, option, widget):
        painter.setPen(QColor(0,0,0))
        for i in range(0,5):
            painter.drawLine(self.offsetx + i*self.size, self.offsety,self.offsetx + i*self.size, self.offsety + self.width)
            painter.drawLine(self.offsetx, self.offsety + i*self.size, self.offsetx + self.height, self.offsety + i*self.size)


        for i in range(1,4,2):
            painter.drawLine(self.offsetx + self.size*i,self.offsety + self.size *4,self.offsetx + self.size*4,self.offsety+self.size*i)
            painter.drawLine(self.offsetx, self.offsety + self.size*i,self.offsetx + self.size*i,self.offsety)

        painter.drawLine(self.offsetx,self.offsety+self.size*3,self.offsetx + self.size,self.offsety + self.size*4)
        painter.drawLine(self.offsetx,self.offsety+self.size*1,self.offsetx + self.size*3,self.offsety + self.size*4)
        painter.drawLine(self.offsetx+self.size*1,self.offsety,self.offsetx + self.size*4,self.offsety + self.size*3)
        painter.drawLine(self.offsetx+self.size*3,self.offsety,self.offsetx + self.size*4,self.offsety + self.size*1)


        painter.setBrush(Qt.red)
        painter.drawRect(0,0,self.offsetx*2,self.offsety + self.width)
        painter.drawRect(0,0,self.offsety + self.height,self.offsety*2)
        painter.drawRect(self.size*2,self.size*2,self.offsetx*2,self.size*2 + self.offsety)

        painter.setPen(QColor(255,0,0))
        for i in range(len(self.pos_x_theo)):
            painter.drawPoint(self.pos_x_theo[i],self.pos_y_theo[i])

        painter.setPen(QColor(255,0,255))
        for i in range(len(self.pos_x_real)):
            painter.drawPoint(self.pos_x_real[i],self.pos_y_real[i])

        painter.setPen(QColor(0,255,0))
        for i in range(len(self.l_tire_pos_x)):
            painter.drawPoint(self.l_tire_pos_x[i],self.l_tire_pos_y[i])

        painter.setPen(QColor(0,255,0))
        for i in range(len(self.r_tire_pos_x)):
            painter.drawPoint(self.r_tire_pos_x[i],self.r_tire_pos_y[i])

    def cacl(self,target_ang):

        precision = 1/1
        angvel = 0
        mypos_x_theo =0
        mypos_y_theo = 0
        mypos_x_real = 0
        mypos_y_real = 0
        r_tire_x = 0
        r_tire_y = 0
        l_tire_x = 0
        l_tire_y = 0
        theta_theo = 0
        theta_real = 0
        theta_right = 0
        theta_left = 0

        count = 0
        second_count = 0
        speed_r = 0
        speed_l = 0
        init_speed = 700
        const = 100
        beta = 0

        chro_end_ang = 10

        del self.pos_x_theo[:]
        del self.pos_y_theo[:]
        del self.pos_x_real[:]
        del self.pos_y_real[:]

        count2 = 0

        while(theta_theo < target_ang):
            if theta_theo < chro_end_ang:
                count2 += 1
                angvel += self.ang_accel * precision
            elif theta_theo < (target_ang - chro_end_ang):
                pass

            elif theta_theo <= target_ang:
                count2 -=1
                angvel += -self.ang_accel * precision

            theta_theo += angvel * precision
            beta += -beta*const/init_speed + angvel * precision
            try:
                radius = 1/math.radians(angvel)
            except:
                radius = 10000

            G = self.weight * math.radians(init_speed * angvel)*init_speed/1000

            mypos_x_theo += np.cos(math.radians(90.0-theta_theo))*precision
            mypos_y_theo += np.sin((90.0-theta_theo)*math.pi/180.0)*precision
            mypos_x_real += np.cos(math.radians(90.0-theta_theo+beta))*precision
            mypos_y_real += np.sin((90.0-theta_theo+beta)*math.pi/180.0)*precision
            r_tire_x = mypos_x_theo+self.tread*0.5*np.cos((theta_theo)*math.pi/180.0)
            r_tire_y = mypos_y_theo-self.tread*0.5*np.sin((theta_theo)*math.pi/180.0)
            l_tire_x = mypos_x_theo-self.tread*0.5*np.cos((theta_theo)*math.pi/180.0)
            l_tire_y = mypos_y_theo+self.tread*0.5*np.sin((theta_theo)*math.pi/180.0)

            if(count == 1/precision):
                self.angvel_list.append(angvel)
                print(radius,angvel*700,theta_theo,beta,G)
                # print(angvel * 700 * math.pi /180)
                count = 0
            count +=1

            self.pos_x_theo.append(self.sla_start_x + self.offsetx + mypos_x_theo)
            self.pos_y_theo.append(self.size*4 -(self.sla_start_y + self.offsety + mypos_y_theo))
            self.pos_x_real.append(self.sla_start_x + self.offsetx + mypos_x_real)
            self.pos_y_real.append(self.size*4 -(self.sla_start_y + self.offsety + mypos_y_real))
            self.l_tire_pos_x.append(self.sla_start_x + l_tire_x + self.offsetx)
            self.l_tire_pos_y.append(self.size*4 - (self.sla_start_y + self.offsety + l_tire_y))
            self.r_tire_pos_x.append(self.sla_start_x + r_tire_x + self.offsetx)
            self.r_tire_pos_y.append(self.size*4 - (self.sla_start_y + self.offsety + r_tire_y))


            if len(self.pos_x_theo) > 100000:break
            if count2 <= 0:break
        self.update()

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.graphicsView = QGraphicsView()
        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(0, 0, 400, 400)
        self.graphicsView.setScene(scene)
        self.draw = Draw()
        scene.addItem(self.draw)

        self.runButton = QPushButton("&Run")
        self.runButton.clicked.connect(self.run)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.runButton)

        self.t_45 = QRadioButton("45")
        self.short90 = QRadioButton("short90")
        self.long90 = QRadioButton("long90")
        self.t_135 = QRadioButton("135")
        self.t_180 = QRadioButton("180")
        self.t_v= QRadioButton("vturn")

        self.bg1 = QButtonGroup()
        self.bg1.addButton(self.t_45)
        self.bg1.addButton(self.short90)
        self.bg1.addButton(self.long90)
        self.bg1.addButton(self.t_135)
        self.bg1.addButton(self.t_180)
        self.bg1.addButton(self.t_v)

        vbox = QVBoxLayout()
        vbox.addWidget(self.t_45)
        vbox.addWidget(self.short90)
        vbox.addWidget(self.long90)
        vbox.addWidget(self.t_135)
        vbox.addWidget(self.t_180)
        vbox.addWidget(self.t_v)

        propertyLayout = QVBoxLayout()
        propertyLayout.setAlignment(Qt.AlignTop)
        propertyLayout.addLayout(vbox)
        propertyLayout.addLayout(buttonLayout)

        mainLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addWidget(self.graphicsView)
        mainLayout.addLayout(propertyLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Turn Simulator")
        self.updating_rule = False

    def run(self):
        if self.t_45.isChecked():
            QMessageBox.about(self,"Message","vturn")
            self.draw.cacl(45)
        elif self.short90.isChecked():
            QMessageBox.about(self,"Message","vturn")
            self.draw.cacl(90)
        elif self.long90.isChecked():
            QMessageBox.about(self,"Message","vturn")
            self.draw.cacl(90)
        elif self.t_135.isChecked():
            QMessageBox.about(self,"Message","vturn")
            self.draw.cacl(135)
        elif self.t_180.isChecked():
            QMessageBox.about(self,"Message","vturn")
            self.draw.cacl(180)
        elif self.t_v.isChecked():
            QMessageBox.about(self,"Message","vturn")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())
