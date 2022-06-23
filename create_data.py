#take many photos of connor ford's face
import cv2, sys, numpy, os
import mysql.connector

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "Oatmeal_007",
    database="python"
)

haar_file = 'haarcascade_frontalface_default.xml'


datasets = 'datasets'

sub_data = 'Will Varner'	

path = os.path.join(datasets, sub_data)
if not os.path.isdir(path):
	os.mkdir(path)


(width, height) = (130, 100)

#usb use 1
face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(0)


count = 1
while count < 50:
	(_, im) = webcam.read()
	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 4)
	for (x, y, w, h) in faces:
		cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
		face = gray[y:y + h, x:x + w]
		face_resize = cv2.resize(face, (width, height))
		cv2.imwrite('% s/% s.png' % (path, count), face_resize)
	count += 1
	
	cv2.imshow('OpenCV', im)
	key = cv2.waitKey(10)
	if key == 27:
		break

mycursor = mydb.cursor()

sql = "INSERT INTO attendance (name) VALUES (%s)"
val = (sub_data)
mycursor.execute(sql, val)

mydb.commit()
print(mycursor.rowcount, "record of", sub_data, "inserted.")