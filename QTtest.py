from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import logging
import cv2, sys, numpy, os, mysql.connector, uuid, mediapipe as mp, time, imutils, getpass
from datetime import datetime
import textwrap

from sqlalchemy import true

###### pyuic5 -x gui.ui -o gui.py


handPreviouslyUp = False
mainUser = "NULL"
loggedIn = []
handsUp = []
loggedOutEarly = []
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_smile.xml')
size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'
currentTime = ""

(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
	for subdir in dirs:
		names[id] = subdir
		subjectpath = os.path.join(datasets, subdir)
		for filename in os.listdir(subjectpath):
			path = subjectpath + '/' + filename
			label = id
			images.append(cv2.imread(path, 0))
			labels.append(int(label))
		id += 1
(width, height) = (130, 100)

(images, labels) = [numpy.array(lis) for lis in [images, labels]]

model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, labels)

face_cascade = cv2.CascadeClassifier(haar_file)
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)


    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        with mp_hands.Hands(min_detection_confidence=.8, min_tracking_confidence=.8, max_num_hands=2) as hands:
            while True:
                ret, im = cap.read()

                image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                #flip im hopefully :)
                image - cv2.flip(image, 1)
                image.flags.writeable = False
                results = hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                #print(results)
                #testing media pipe ^

                if results.multi_hand_landmarks:
                    for num, hand in enumerate(results.multi_hand_landmarks):
                        mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                                mp_drawing.DrawingSpec(color=(250, 44, 250), thickness = 2, circle_radius = 2)
                                                )
                    print("Hand detected lol")
                else: 
                    print("Hand lowered lol")


                                                                                                                                        #HAND CODE ENDS


                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    face = gray[y:y + h, x:x + w]
                    face_resize = cv2.resize(face, (width, height))

                    roi_gray = gray[y:y + h, x:x + w]
                    roi_color = image[y:y + h, x:x + w]
                    
                    smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)

                    for (sx, sy, sw, sh) in smiles:
                        cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)

                    prediction = model.predict(face_resize)
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)

                    if prediction[1]<500:
                        cv2.putText(image, '% s - %.0f' % (names[prediction[0]], prediction[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                        #faceFound()
                    else:
                        cv2.putText(image, 'not recognized', (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                        print("Foreign Face Found")

                if ret:
                    self.change_pixmap_signal.emit(image)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()



    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())