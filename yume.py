# !/usr/bin/python3.10
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime

app=QApplication(sys.argv)

class Yume(QWidget):
    # Attribut
    assistant_name="Yume"

    update_delay=1000 # Mise à jour chaque milliseconde
    reset_delay=datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day+1, 0, 0, 0)-datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second) # Temps restant avant le lendemain
    f_already_show=[False, False, False, False]

    good_morning_img=QMovie("img/good_morning_img.gif")
    good_afternoon_img=QMovie("img/good_afternoon_img.gif")
    good_evening_img=QMovie("img/good_evening_img.gif")
    good_night_img=QMovie("img/good_night_img.gif")
    
    layout=None
    actual_time=None
    actual_img=None
    label=None
    update_timer=QTimer()
    reset_timer=QTimer()

    def __init__(self, parent=None):
        super(Yume, self).__init__(parent)        
        self.layout=QVBoxLayout(self)
        self.actual_img=QLabel(self)
        self.label=QLabel(self)
        self.button=QPushButton("Okay compris, merci")

        self.layout.addWidget(self.actual_img)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.actual_img.setAlignment(Qt.AlignCenter)
        self.label.setAlignment(Qt.AlignCenter)            
        self.hide()
        self.resetTime()
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self.size(), qApp.desktop().availableGeometry())) 
        self.setWindowTitle("{0}, mon assistante personnelle ^^".format(self.assistant_name))
        self.setWindowIcon(QIcon("img/app_icon.jpg"))   
        self.updateYume()        
        self.button.clicked.connect(self.hide)
        self.update_timer.start(self.update_delay)
        self.reset_timer.start(int(self.reset_delay.total_seconds()*1000))
        self.update_timer.timeout.connect(self.updateYume)
        self.reset_timer.timeout.connect(self.resetFlag)

    def resetTime(self):
        self.morning_beginning_time=datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 6, 0, 0)
        self.morning_ending_time=datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 12, 0, 0)

        self.afternoon_beginning_time=self.morning_ending_time
        self.afternoon_ending_time=datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 18, 0, 0)

        self.night_beginning_time=self.afternoon_ending_time
        self.midnight_time_next_day=datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day+1, 0, 0, 0)
        self.midnight_time_today=datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 0, 0, 0)
        self.night_ending_time=datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 6, 0, 0)

    def resetFlag(self):        
        for i in range(len(self.f_already_show)):
            self.f_already_show[i]=False

        self.reset_delay=datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day+1, 0, 0, 0)-datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second) 
        self.reset_timer.start(int(self.reset_delay.total_seconds()*1000))

    def updateYume(self):
        self.resetTime()
        self.actual_time=datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second)
        
        if self.morning_beginning_time<=self.actual_time and self.actual_time<self.morning_ending_time:            
            self.actual_img.setMovie(self.good_morning_img)            
            self.good_morning_img.start()
            self.label.setText("<body style=\"font-size: large; font-weight: bold;\"><p>Bonjour Chris, il est {0}h{1}min.</p><p>Je vous souhaite une excellente journée.</p><p>Bon courage ^^.</p></body>".format(str(self.actual_time.hour).zfill(2), str(self.actual_time.minute).zfill(2)))
            if not self.isVisible() and not self.f_already_show[0]:
                self.show()
            self.f_already_show[0]=True            
            self.update_timer.start(self.update_delay)

        
        elif self.afternoon_beginning_time<=self.actual_time and self.actual_time<self.afternoon_ending_time:
            self.actual_img.setMovie(self.good_afternoon_img)
            self.good_afternoon_img.start()
            self.label.setText("<body style=\"font-size: large; font-weight: bold;\"><p>Yo Chris, il est {0}h{1}min.</p><p>Je vous souhaite une excellente après-midi.</p><p>Mangez bien et reposez-vous bien ^^.</p></body>".format(str(self.actual_time.hour).zfill(2), str(self.actual_time.minute).zfill(2)))
            if not self.isVisible() and not self.f_already_show[1]:
                self.show()
            self.f_already_show[1]=True            
            self.update_timer.start(self.update_delay)
        
        elif self.night_beginning_time<=self.actual_time and self.actual_time<self.midnight_time_next_day:            
            self.actual_img.setMovie(self.good_evening_img)
            self.good_evening_img.start()
            self.label.setText("<body style=\"font-size: large; font-weight: bold;\"><p>Bonsoir Chris, il est {0}h{1}min.</p><p>Je vous souhaite une excellente soirée.</p><p>Mangez bien et reposez-vous bien ^^.</p></body>".format(str(self.actual_time.hour).zfill(2), str(self.actual_time.minute).zfill(2)))
            if not self.isVisible() and not self.f_already_show[2]:
                self.show()
            self.f_already_show[2]=True            
            self.update_timer.start(self.update_delay)

        elif self.midnight_time_today<=self.actual_time and self.actual_time<self.morning_beginning_time:
            self.actual_img.setMovie(self.good_night_img)
            self.good_night_img.start()
            self.label.setText("<body style=\"font-size: large; font-weight: bold;\"><p>Bonne nuit Chris, il est {0}h{1}min.</p><p>Je vous souhaite une excellente nuit.</p><p>Vous devriez aller vous coucher maintenant ^^.</p></body>".format(str(self.actual_time.hour).zfill(2), str(self.actual_time.minute).zfill(2)))
            if not self.isVisible() and not self.f_already_show[3]:
                self.show()
            self.f_already_show[3]=True            
            self.update_timer.start(self.update_delay)


yume=Yume()
sys.exit(app.exec())