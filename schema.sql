-- ============================================================================
-- DROP EXISTING TABLES (if needed)
-- ============================================================================
DROP TABLE IF EXISTS `Naman_project`.`Student_Marks`;
DROP TABLE IF EXISTS `Naman_project`.`Students`;

-- ============================================================================
-- CREATE STUDENT INFORMATION TABLE
-- ============================================================================
CREATE TABLE `Naman_project`.`Students` (
  `UID` INT NOT NULL AUTO_INCREMENT,
  `Student_Name` VARCHAR(100) NOT NULL,
  `Father_Name` VARCHAR(100) NOT NULL,
  `Mother_Name` VARCHAR(100) NOT NULL,
  `Parent_Number` VARCHAR(15) NOT NULL,
  `Address` VARCHAR(255) NOT NULL,
  `Created_At` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`UID`),
  UNIQUE INDEX `UID_UNIQUE` (`UID` ASC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- CREATE STUDENT MARKS TABLE
-- ============================================================================
CREATE TABLE `Naman_project`.`Student_Marks` (
  `Mark_ID` INT NOT NULL AUTO_INCREMENT,
  `UID` INT NOT NULL,
  `Physics_Marks` INT NOT NULL,
  `Chemistry_Marks` INT NOT NULL,
  `Mathematics_Marks` INT NOT NULL,
  `English_Marks` INT NOT NULL,
  `Computer_Marks` INT NOT NULL,
  `PHE_Marks` INT NOT NULL,
  `Total` INT NOT NULL,
  `Percentage` DECIMAL(5, 2) NOT NULL,
  `Grade` VARCHAR(2) NOT NULL,
  `Updated_At` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`Mark_ID`),
  FOREIGN KEY (`UID`) REFERENCES `Students`(`UID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- INSERT SAMPLE STUDENT DATA
-- ============================================================================
INSERT INTO `Naman_project`.`Students` (`Student_Name`, `Father_Name`, `Mother_Name`, `Parent_Number`, `Address`) VALUES
('Rajesh Kumar', 'Amit Kumar', 'Priya Kumar', '9876543210', '123 Main Street, Delhi'),
('Aisha Khan', 'Mohammad Khan', 'Fatima Khan', '9876543211', '456 Park Avenue, Mumbai'),
('Rohan Sharma', 'Vikram Sharma', 'Neha Sharma', '9876543212', '789 Maple Lane, Bangalore'),
('Zara Patel', 'Arjun Patel', 'Divya Patel', '9876543213', '321 Elm Street, Ahmedabad'),
('Aaryan Singh', 'Rajesh Singh', 'Anjali Singh', '9876543214', '654 Oak Road, Pune');

-- ============================================================================
-- INSERT SAMPLE MARKS DATA
-- ============================================================================
INSERT INTO `Naman_project`.`Student_Marks` (`UID`, `Physics_Marks`, `Chemistry_Marks`, `Mathematics_Marks`, `English_Marks`, `Computer_Marks`, `PHE_Marks`, `Total`, `Percentage`, `Grade`) VALUES
(1, 85, 92, 88, 90, 95, 80, 530, 88.33, 'A'),
(2, 78, 85, 82, 88, 90, 75, 498, 83.00, 'A'),
(3, 92, 89, 95, 86, 88, 85, 535, 89.17, 'A'),
(4, 73, 78, 80, 75, 82, 70, 458, 76.33, 'B'),
(5, 88, 91, 90, 87, 93, 86, 535, 89.17, 'A');

-- ============================================================================
-- DISPLAY TABLE STRUCTURE
-- ============================================================================
SHOW TABLES IN `Naman_project`;
SELECT * FROM `Naman_project`.`Students`;
SELECT * FROM `Naman_project`.`Student_Marks`;