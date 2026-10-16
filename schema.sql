-- MySQL 8.0.16+. Safe to run again, but does not migrate older schemas.
CREATE DATABASE IF NOT EXISTS job_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE job_tracker;
CREATE TABLE IF NOT EXISTS companies (
 company_id INT PRIMARY KEY AUTO_INCREMENT,
 company_name VARCHAR(100) NOT NULL,
 industry VARCHAR(50), website VARCHAR(200), city VARCHAR(50), state VARCHAR(50), notes TEXT
) ENGINE=InnoDB;
