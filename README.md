# TechDetect Attendance Manager 
TechDetect is a python open-cv powered facial detection program that connects to a mySQL database and flask site to allow teams, schools, or corporations to keep tract of attendance using facial detection. The system was developed during my 2022 STEM@GTRI Internship.

## Setup

### Dependencies
TechDetect requires few dependencies, with notable packages being OpenCV and Google's Mediapipe package
Ensure you have [Python installed](https://www.python.org/downloads/), and use ```pip install``` to download these packages:

```
Flask==1.1.2
Flask_MySQLdb==1.0.1
imutils==0.5.4
mediapipe==0.8.10
MySQL-python==1.2.5
mysql_connector_repackaged==0.3.1
numpy==1.21.5
opencv_python==4.6.0.66
requests==2.27.1
SQLAlchemy==1.4.32
```

### MySQL
TechDetect requires a running MySQL Database installed locally on the host machine. [Install Here](https://dev.mysql.com/downloads/mysql/).
Any credentials will work with the program, as it will prompt the user with login credentials upon starting the appliocation.

### Program Files
Download the program from above or by running
```git clone https://github.com/willv678/TechDetect ```


## Running the Program

### First Time Setup
- To begin, first open ```createData.py```. The application will prompt you for your MySql Server login. Upon entering the credentials, you will be prompted for a face name and a corresponding ID number.

- The program will open a openCV window, which captures 75 images of the users face, saving them into a folder in ```./Datasets/name```. Afterwards, the information will be uploaded to the SQL database under ```TechDetect/Users```

### Main Application
- Open ```TechDetect.py``` and enter your database credentials
- TechDetect will now open the main window, a camera window that constantly analyzes video input, detecting faces and comparing them to the currently existing database, returning values drawn over the user's face if a customizable confidence score is met, returning *unknown* in event of a low confidence score
 ### Hand Detection
 Additionally, TechDetect features Google's mediapipe ai library in order to track hand movements onscreen, allowing for further implementation of code to run commands based on hand input. This feature was built primarily with education in mind, as the program comes with pre-concieved functions that already detect a hand raised and lowered as well as who it belongs to.

## Web Panel
All data can be accessed under a locally hosted Flask site. To start the site, run ```app.py``` in the ```./website``` folder. The website will then be hosted locally, which can be accessed from any internet browser on your machine.
### Logins
The Flask site is held behind a login system, with user logins maintained in our SQL database. To add a user, either insert a new record in the login databse, or hit register on the localhost site and enter credentials.
### Viewing Data
Welcome to our site! You can view today's attendance records with login and logout times that can be organized by either of these factors of by name or id numbers. Additionally, another page holds information of all registered users for view on the website, eliminating the need of a complex database CRUD workbench app.


## Closing Thoughts
TechDetect was created with the goal to revolutionize the classroom, aiding teachers and students alike by changing the way we think of the classroom. MY implementation of many hand and face detection booleans and arrays will hopefully lead to a further developed version that is able to evolve past what I've created now, perhaps implementing these changes to help teachers give their zoom-ridden students the same attention they deserve, or helping that one student in the back get seen by the professor in a crowded college class. I'm super excited to see how far I can take this project, and I'm incredibly glad I was given the opportunity from the STEM@GTRI program. Thanks for making it all the way to the end!
