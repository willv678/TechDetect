CREATE TABLE IF NOT EXISTS `techdetect`.`accounts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `organization` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`))
