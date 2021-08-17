# CREATE DATABASE adoption_agency;

CREATE TABLE `pets` (
	`id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(40) NOT NULL,
    `speciesID` INT NOT NULL, # This will link to the species table 
    `sex` VARCHAR(1), # F/M
    `age` FLOAT NOT NULL, # This will be in years, 6 months will be 0.5 years
    `sizeID` INT, # This will link to the size table to prevent dirty data
    `weight` FLOAT, # This will be in pounds
    `fixed` BOOLEAN,
    `houseTrained` BOOLEAN, # Can be null for not aplicable situations
    `description` TEXT,
    `admittedOn` DATETIME,
    `adopted` BOOLEAN,
    `isActive` BOOLEAN # Used for soft deletes
);

CREATE TABLE `species` (
	`id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `isActive` BOOLEAN # Used for soft deletes
);

CREATE TABLE `breeds` (
	`id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `speciesID` INT NOT NULL, # Associates breeds with species
    `isActive` BOOLEAN # Used for soft deletes
);

CREATE TABLE `sizes` (
	`id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(40) NOT NULL,
    `isActive` BOOLEAN # Used for soft deletes
);

CREATE TABLE `colors` (
	`id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    `isActive` BOOLEAN # Used for soft deletes
);

# Links pets to colors to allow multiples
CREATE TABLE `petColorTags` (
	`id` INT PRIMARY KEY AUTO_INCREMENT,
    `petID` INT NOT NULL, # This will link to the pets table
    `colorID` INT NOT NULL, # This will link to the colors table
    `isActive` BOOLEAN # Used for soft deletes
);

# Links pets to breeds to allow for multiples
CREATE TABLE `petBreedTags` (
	`id` INT PRIMARY KEY AUTO_INCREMENT,
    `petID` INT NOT NULL, # This will link to the pets table
    `breedID` INT NOT NULL, # This will link to the breeds table,
    `isActive` BOOLEAN # Used for soft deletes
);

ALTER TABLE `pets` ADD FOREIGN KEY (`speciesID`) REFERENCES `species`(`id`);
ALTER TABLE `pets` ADD FOREIGN KEY (`sizeID`) REFERENCES `sizes`(`id`);
ALTER TABLE `breeds` ADD FOREIGN KEY (`speciesID`) REFERENCES `species`(`id`);
ALTER TABLE `petColorTags` ADD FOREIGN KEY (`petID`) REFERENCES `pets`(`id`);
ALTER TABLE `petColorTags` ADD FOREIGN KEY (`colorID`) REFERENCES `colors`(`id`);
ALTER TABLE `petBreedTags` ADD FOREIGN KEY (`petID`) REFERENCES `pets`(`id`);
ALTER TABLE `petBreedTags` ADD FOREIGN KEY (`breedID`) REFERENCES `breeds`(`id`);

