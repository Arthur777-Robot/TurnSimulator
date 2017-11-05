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
        self.weight = 0.080
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

    def cacl(self,target_ang,init_speed = 700,max_G = 0.5):

        precision = 1/10
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
        const = 100
        beta = 0
        G = 0
        ang_vel_beta = 0
        flag = 0


        del self.pos_x_theo[:]
        del self.pos_y_theo[:]
        del self.pos_x_real[:]
        del self.pos_y_real[:]
        del self.r_tire_pos_x[:]
        del self.r_tire_pos_y[:]
        del self.l_tire_pos_x[:]
        del self.l_tire_pos_y[:]
        del self.angvel_list[:]

        # while(theta_theo - beta < target_ang):
        # while((angvel + ang_vel_beta) >= 0):
        while(angvel >= 0):
        # while((angvel ) >= 0):
            if (G < max_G and flag == 0):
                angvel += self.ang_accel * precision
                chro_end_ang = theta_theo
            elif theta_theo < (target_ang - chro_end_ang):
            # elif theta_theo-beta < (target_ang - chro_end_ang):
                flag = 1
                pass

            # elif theta_theo <= target_ang:
            # elif (angvel + ang_vel_beta) >= 0:
            elif (angvel) >= 0:
                angvel += -self.ang_accel * precision

            theta_theo += angvel * precision
            ang_vel_beta = (-beta*const/init_speed + angvel) * precision
            beta += (-beta*const/init_speed + angvel) * precision
            try:
                radius = 1/math.radians(angvel)         #radius in mm
            except:
                radius = 10000

            G = radius/1000 * (math.radians(angvel * init_speed + ang_vel_beta)) **2 / 9.8

            mypos_x_theo += np.cos(math.radians(90.0-theta_theo))*precision
            mypos_y_theo += np.sin((90.0-theta_theo)*math.pi/180.0)*precision
            mypos_x_real += np.cos(math.radians(90.0-theta_theo+beta))*precision
            mypos_y_real += np.sin((90.0-theta_theo+beta)*math.pi/180.0)*precision
            r_tire_x = mypos_x_real+self.tread*0.5*np.cos((theta_theo-beta)*math.pi/180.0)
            r_tire_y = mypos_y_real-self.tread*0.5*np.sin((theta_theo-beta)*math.pi/180.0)
            l_tire_x = mypos_x_real-self.tread*0.5*np.cos((theta_theo-beta)*math.pi/180.0)
            l_tire_y = mypos_y_real+self.tread*0.5*np.sin((theta_theo-beta)*math.pi/180.0)

            if(count == 1/precision):
                self.angvel_list.append(angvel)
                print(angvel,theta_theo,theta_theo-beta,beta,G)
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


            if len(self.pos_x_theo) > 5000:break

        # if(target_ang < 120 or target_ang > 85):
        #     for i in range(len(self.pos_x_theo)):
        #         self.pos_y_real[i] += (self.sla_start_y + self.offsety*2 + mypos_y_real) - self.size*3
        #         self.pos_y_theo[i] += (self.sla_start_y + self.offsety*2 + mypos_y_real) - self.size*3
        #         self.l_tire_pos_y[i] += (self.sla_start_y + self.offsety*2 + mypos_y_real) - self.size*3
        #         self.r_tire_pos_y[i] += (self.sla_start_y + self.offsety*2 + mypos_y_real) - self.size*3
        self.update()
        return beta

    def save(self):
        # f = open('test.c','w')
        # f.writelines(self.angvel_list)
        # f.close()
        csv_file = u"test"
        csv_filename = csv_file + ".c"
        np.savetxt(csv_filename, (self.angvel_list), delimiter=",",header=" ",fmt='%f')

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.graphicsView = QGraphicsView()
        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(0, 0, 400, 400)
        self.graphicsView.setScene(scene)
        self.draw = Draw()
        scene.addItem(self.draw)

        self.init_vel = QLineEdit()
        self.init_vel.setText(str("1000"))
        self.maxG = QLineEdit()
        self.maxG.setText(str("1.0"))

        lineLayout = QVBoxLayout()
        lineLayout.addWidget(QLabel("Entering Velocity[mm/s]"))
        lineLayout.addWidget(self.init_vel)
        lineLayout.addWidget(QLabel("Max_G"))
        lineLayout.addWidget(self.maxG)

        self.runButton = QPushButton("&Run")
        self.runButton.clicked.connect(self.run)
        self.saveButton = QPushButton("&Save")
        self.saveButton.clicked.connect(self.save)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.runButton)
        buttonLayout.addWidget(self.saveButton)

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
        propertyLayout.addLayout(lineLayout)
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
        self.graphicsView.update()
        if self.t_45.isChecked():
            QMessageBox.about(self,"Message","45 turn")
            beta = self.draw.cacl(45,int(self.init_vel.text()),float(self.maxG.text()))
            self.graphicsView.update()
            self.draw.cacl(45+beta,int(self.init_vel.text()),float(self.maxG.text()))
        elif self.short90.isChecked():
            QMessageBox.about(self,"Message","short 90 turn")
            beta = self.draw.cacl(90,int(self.init_vel.text()),float(self.maxG.text()))
            self.graphicsView.update()
            self.draw.cacl(90+beta,int(self.init_vel.text()),float(self.maxG.text()))
        elif self.long90.isChecked():
            QMessageBox.about(self,"Message","long 90 turn")
            beta = self.draw.cacl(90,int(self.init_vel.text()),float(self.maxG.text()))
            self.graphicsView.update()
            self.draw.cacl(90+beta,int(self.init_vel.text()),float(self.maxG.text()))
        elif self.t_135.isChecked():
            QMessageBox.about(self,"Message","135 turn")
            beta = self.draw.cacl(135,int(self.init_vel.text()),float(self.maxG.text()))
            self.graphicsView.update()
            self.draw.cacl(135+beta,int(self.init_vel.text()),float(self.maxG.text()))
        elif self.t_180.isChecked():
            QMessageBox.about(self,"Message","vturn")
            beta = self.draw.cacl(180,int(self.init_vel.text()),float(self.maxG.text()))
            # beta1 = self.draw.cacl(180)
            # beta2 = self.draw.cacl(180+beta1)
            # print(beta1,beta2)
        elif self.t_v.isChecked():
            QMessageBox.about(self,"Message","vturn")

    def save(self):
        self.draw.save()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())
