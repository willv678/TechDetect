CREATE SCHEMA IF NOT EXISTS `techDetect` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `techDetect` ;

DROP TABLE IF EXISTS `techDetect`.`attendance` ;
CREATE TABLE IF NOT EXISTS `techDetect`.`attendance` (
  `studentID` INT NOT NULL,
  `studentName` VARCHAR(45) NOT NULL,
  `studentCheckInTime` VARCHAR(45) NULL DEFAULT NULL,
  `studentCheckOutTime` VARCHAR(45) NULL DEFAULT NULL,
  `handRaised` TINYINT NULL,
  PRIMARY KEY (`studentID`))

SELECT * FROM `tech detect`.attendance; 