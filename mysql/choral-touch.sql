SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `choral_touch` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `choral_touch` ;

-- -----------------------------------------------------
-- Table `choral_touch`.`event`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `choral_touch`.`event` ;

CREATE  TABLE IF NOT EXISTS `choral_touch`.`event` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `month` INT NOT NULL ,
  `day` INT NOT NULL ,
  `year` INT NOT NULL ,
  `note` VARCHAR(45) NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;

USE `choral_touch` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;