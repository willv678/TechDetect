# Identify faces based off photos 
import cv2, sys, numpy, os, mysql.connector, uuid, mediapipe as mp, time
from datetime import datetime
import textwrap

from sqlalchemy import true


date = datetime.now()
dateString = str(date)
todayDate = (textwrap.shorten(dateString, 11, placeholder = ''))
todayDate = todayDate.replace("-","_")

studentID = "19151"
todayTime = (dateString)
todayTime = dateString[10:]

todayTime = todayTime[:6]


mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "Oatmeal_007",
    database="techDetect"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE SCHEMA IF NOT EXISTS `techDetect` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;")
mycursor.execute("USE `techDetect` ;")
print(todayDate)
mycursor.execute("DROP TABLE IF EXISTS `techDetect`.`attendance_"+todayDate+"` ;")
mycursor.execute("""CREATE TABLE IF NOT EXISTS `techDetect`.`attendance_"""+todayDate+ """` (
  `studentID` INT NOT NULL,
  `studentName` VARCHAR(45) NOT NULL,
  `studentCheckInTime` VARCHAR(45) NULL DEFAULT NULL,
  `studentCheckOutTime` VARCHAR(45) NULL DEFAULT NULL,
  `handRaised` TINYINT NULL,
  PRIMARY KEY (`studentID`))
""")

#mycursor.execute("""
#INSERT INTO attendance_2022_07_12 (studentID, studentName, studentCheckInTime)
#VALUES (19151, "Will_Varner", "8:10");
#""")

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
def getTime():
    global todayDate
    global currentTime
    date = datetime.now()
    dateString = str(date)
    todayDate = (textwrap.shorten(dateString, 11, placeholder = ''))

    todayTime = (dateString)
    todayTime = dateString[10:]

    todayTime = todayTime[:6]
    currentTime = todayTime

def faceFound():
    global mainUser
    global todayDate
    global mainStudentID
    global todayTime
    global currentTime
    faceName = (names[prediction[0]])
    if not faceName in loggedIn:
        print("New face found!")
        print("The face belongs to ",(names[prediction[0]]) , "!")
        loggedIn.append((names[prediction[0]]))
        print( (names[prediction[0]]) +" has clocked in at: ", datetime.now() )
        if len(loggedIn) == 1:
            mainUser = faceName
            print("Primary user " + mainUser + " added!")
            
            #adds user to DB
            mycursor.execute("SELECT studentID FROM students WHERE studentName = '"+mainUser+"'")
            ID = mycursor.fetchall()
            mainStudentID = str(ID)
            mainStudentID = mainStudentID[2:7]
            print(mainUser + "'s student id is: " + mainStudentID)
            sql = "INSERT INTO attendance_"+todayDate+" (studentID, studentName, studentCheckInTime) VALUES (%s, %s, %s)"
            getTime()
            print("Current time is " + currentTime)
            val = (mainStudentID, mainUser, currentTime)
            #val = (19999, "Will", "2:00")
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted!")


        print("Currently logged in: ", loggedIn)
        print ("again main user is ", mainUser)





def exit():
    global mainUser
    global quitTime
    global quitName
    global currentTime
    global todayDate

    print("\n" * 5)
    print("Logging out ", mainUser, " ...")
    print("Clocking out user", mainUser, "at", datetime.now())
    print(todayDate)
    loggedIn.remove(mainUser)
    quitInfo = (mainUser, " - ",datetime.now())
    quitTime = datetime.now()
    quitName = mainUser
    loggedOutEarly.append(quitInfo)
    print("Uploading to database...")
    


    date = datetime.now()
    dateString = str(date)
    todayDate = (textwrap.shorten(dateString, 11, placeholder = ''))
    todayDate = todayDate.replace("-","_")
    print(todayDate)
    getTime()
    #checkout
    mycursor.execute("UPDATE `techdetect`.`attendance_"+todayDate+"` SET `studentCheckOutTime` = '"+ currentTime+"' WHERE (`studentID` = '"+ mainStudentID+"')")
    mydb.commit()
    print("Successfully checked out user!")


def handDetected():
    global mainUser
    global handPreviouslyUp
    if handPreviouslyUp == False:
        print("Hand found!")
        print("Hand belongs to", mainUser)
        handPreviouslyUp = True
    
    handsUp.append(mainUser)
def handLowered():
    global mainUser
    global handPreviouslyUp
    if handPreviouslyUp == True:
        handsUp.remove(mainUser)
        print(mainUser, "'s hand removed")
        handPreviouslyUp = False

def handLower():
    if handPreviouslyUp == True:
        print("among us")

print('Starting up...')
print("SQL Connected!", mydb)

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
outputFolderName = "Detection webcamtures"
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
webcam = cv2.VideoCapture(0)


#HAND DETECTING
with mp_hands.Hands(min_detection_confidence=.8, min_tracking_confidence=.8, max_num_hands=2) as hands:
    while True:
        (ret, im) = webcam.read()



                                                                                                                            #HAND CODE BEGINS


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
            handDetected()
        else: 
            handLowered()


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
                faceFound()
            else:
                cv2.putText(image, 'not recognized', (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                print("Foreign Face Found")

        cv2.imshow('Tech Detect', image)



        key = cv2.waitKey(10)
        if key == 27:
            exit()
            break

#All above code made by Will Varner