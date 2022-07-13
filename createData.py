#take many photos of connor ford's face
import getpass
import cv2, sys, numpy, os, mysql.connector

dbUser = input("Enter SQL username: \n")
dbPass = getpass.getpass("Enter SQL password: \n") 


mydb = mysql.connector.connect(
	host = "localhost",
	user = dbUser,
	password = dbPass,
)

mycursor = mydb.cursor()


mycursor.execute("CREATE DATABASE IF NOT EXISTS techDetect")
mydb.commit()
mycursor.execute("USE techDetect")

haar_file = 'haarcascade_frontalface_default.xml'


datasets = 'datasets'

sub_data = input("Please enter your full name: \n")
print(sub_data)
ID = input("Enter face ID: \n")

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

print ("Face captured, uploading face ID to database...")

sub_data
ID

mycursor.execute("INSERT INTO `techdetect`.`students` (`studentID`, `studentName`) VALUES ('"+ID+"', '"+sub_data+"');")
mydb.commit()
print(mycursor.rowcount, "record inserted!")
print("Process completed...")