# Identify faces based off photos 
import cv2, sys, numpy, os, mysql.connector, uuid, mediapipe as mp, time
from datetime import datetime

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "Oatmeal_007",
    database="techDetect"
)

handPreviouslyUp = False
mainUser = "NULL"
loggedIn = []
handsUp = []
loggedOutEarly = []
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_smile.xml')
size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'

def faceFound():
    
    time = 120
    counter = 0
    global mainUser
    faceName = (names[prediction[0]])
    if not faceName in loggedIn:
        print("New face found!")
        print("The face belongs to ",(names[prediction[0]]) , "!")
        loggedIn.append((names[prediction[0]]))
        print( (names[prediction[0]]) +" has clocked in at: ", datetime.now() )
        if len(loggedIn) == 1:
            mainUser = faceName
            print("Primary user " + mainUser + " added!")
        print("Currently logged in: ", loggedIn)
        print ("again main user is ", mainUser)

def exit():
    global mainUser
    print("\n" * 5)
    print("Logging out ", mainUser, " ...")
    print("Clocking out user", mainUser, "at", datetime.now())
    loggedIn.remove(mainUser)
    quitInfo = (mainUser, " - ",datetime.now())
    quitTime = datetime.now()
    quitName = mainUser
    loggedOutEarly.append(quitInfo)
    print("Uploading to database...")


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
        print(mainUser + "'s hand removed")
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


#REMEMBER TO TONE DOWN THE HAND COUNT CZU 4 PROB IS A LOT
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
            