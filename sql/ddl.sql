-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema contratos_menores_test
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema contratos_menores_test
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `contratos_menores_test` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `contratos_menores_test` ;

-- -----------------------------------------------------
-- Table `contratos_menores_test`.`empresa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `contratos_menores_test`.`empresa` (
  `empresa_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nif_empresa` VARCHAR(150) NULL DEFAULT NULL,
  `empresa_nombre` VARCHAR(580) NULL DEFAULT NULL,
  `empresa_es_pyme` VARCHAR(20) NULL DEFAULT NULL,
  `empresa_pais` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`empresa_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `contratos_menores_test`.`tipo_actividad_organo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `contratos_menores_test`.`tipo_actividad_organo` (
  `codigo_actividad_organo` VARCHAR(10) NOT NULL,
  `nombre_actividad_organo` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`codigo_actividad_organo`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `contratos_menores_test`.`tipo_organo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `contratos_menores_test`.`tipo_organo` (
  `codigo_tipo_organo` VARCHAR(10) NOT NULL,
  `nombre_tipo_organo` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`codigo_tipo_organo`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `contratos_menores_test`.`organo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `contratos_menores_test`.`organo` (
  `organo_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `organo_dir3` VARCHAR(20) NULL DEFAULT NULL,
  `organo_nombre` VARCHAR(300) NULL DEFAULT NULL,
  `tipo_organo_codigo` VARCHAR(10) NULL DEFAULT NULL,
  `actividad_organo_codigo` VARCHAR(10) NULL DEFAULT NULL,
  `organo_postalcode` VARCHAR(20) NULL DEFAULT NULL,
  `organo_localidad` VARCHAR(255) NULL DEFAULT NULL,
  `organo_email` VARCHAR(255) NULL DEFAULT NULL,
  `organo_telefono` VARCHAR(30) NULL DEFAULT NULL,
  `organo_nif` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`organo_id`),
  INDEX `FK_org_tipoorg_idx` (`tipo_organo_codigo` ASC) VISIBLE,
  INDEX `FK_org_actividad_organo_idx` (`actividad_organo_codigo` ASC) VISIBLE,
  CONSTRAINT `FK_org_actividad_organo`
    FOREIGN KEY (`actividad_organo_codigo`)
    REFERENCES `contratos_menores_test`.`tipo_actividad_organo` (`codigo_actividad_organo`),
  CONSTRAINT `FK_org_tipo_organo`
    FOREIGN KEY (`tipo_organo_codigo`)
    REFERENCES `contratos_menores_test`.`tipo_organo` (`codigo_tipo_organo`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
ROW_FORMAT = COMPRESSED;


-- -----------------------------------------------------
-- Table `contratos_menores_test`.`tipo_contrato`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `contratos_menores_test`.`tipo_contrato` (
  `codigo_tipo_contrato` VARCHAR(10) NOT NULL,
  `nombre_contrato` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`codigo_tipo_contrato`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `contratos_menores_test`.`contrato`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `contratos_menores_test`.`contrato` (
  `id_entry_num` VARCHAR(45) NOT NULL,
  `id_entry` VARCHAR(255) NULL DEFAULT NULL,
  `titulo` VARCHAR(4500) NULL DEFAULT NULL,
  `id_licitacion` VARCHAR(120) NULL DEFAULT NULL,
  `fecha_actualizacion` DATETIME NULL DEFAULT NULL,
  `fecha_adjudicacion` DATETIME NULL DEFAULT NULL,
  `estado` VARCHAR(30) NULL DEFAULT NULL,
  `codigo_tipo_contrato` VARCHAR(10) NULL DEFAULT NULL,
  `codigo_subtipo_contrato` VARCHAR(10) NULL DEFAULT NULL,
  `importe_estimado` DECIMAL(15,2) NULL DEFAULT NULL,
  `importe_total` DECIMAL(15,2) NULL DEFAULT NULL,
  `importe_sin_impuestos` DECIMAL(15,2) NULL DEFAULT NULL,
  `codigo_cpv_principal` VARCHAR(20) NULL DEFAULT NULL,
  `codigo_region_nuts` VARCHAR(10) NULL DEFAULT NULL,
  `ofertas_recibidas` VARCHAR(10) NULL DEFAULT NULL,
  `id_plataforma` VARCHAR(50) NULL DEFAULT NULL,
  `contr_organo_id` INT UNSIGNED NULL,
  `contr_empresa_id` INT UNSIGNED NULL,
  PRIMARY KEY (`id_entry_num`),
  INDEX `FK_tipo_contrato_idx` (`codigo_tipo_contrato` ASC) VISIBLE,
  INDEX `FK_contr_empresa_idx` (`contr_empresa_id` ASC) VISIBLE,
  INDEX `FK_contr_organo_idx` (`contr_organo_id` ASC) VISIBLE,
  CONSTRAINT `FK_contr_empresa`
    FOREIGN KEY (`contr_empresa_id`)
    REFERENCES `contratos_menores_test`.`empresa` (`empresa_id`),
  CONSTRAINT `FK_contr_organo`
    FOREIGN KEY (`contr_organo_id`)
    REFERENCES `contratos_menores_test`.`organo` (`organo_id`),
  CONSTRAINT `FK_contr_tipo_contrato`
    FOREIGN KEY (`codigo_tipo_contrato`)
    REFERENCES `contratos_menores_test`.`tipo_contrato` (`codigo_tipo_contrato`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
