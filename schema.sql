-- MySQL 8.0.16+. Safe to run again, but does not migrate older schemas.
CREATE DATABASE IF NOT EXISTS job_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE job_tracker;
CREATE TABLE IF NOT EXISTS companies (
 company_id INT PRIMARY KEY AUTO_INCREMENT,
 company_name VARCHAR(100) NOT NULL,
 industry VARCHAR(50), website VARCHAR(200), city VARCHAR(50), state VARCHAR(50), notes TEXT
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS jobs (
 job_id INT PRIMARY KEY AUTO_INCREMENT, company_id INT NOT NULL,
 job_title VARCHAR(100) NOT NULL,
 job_type ENUM('Full-time','Part-time','Contract','Internship'),
 salary_min INT, salary_max INT, job_url VARCHAR(300), date_posted DATE, requirements JSON,
 CONSTRAINT fk_jobs_company FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE RESTRICT,
 CONSTRAINT ck_salary_min CHECK (salary_min IS NULL OR salary_min >= 0),
 CONSTRAINT ck_salary_max CHECK (salary_max IS NULL OR salary_max >= 0),
 CONSTRAINT ck_salary_range CHECK (salary_min IS NULL OR salary_max IS NULL OR salary_max >= salary_min),
 INDEX idx_jobs_title (job_title)
) ENGINE=InnoDB;
