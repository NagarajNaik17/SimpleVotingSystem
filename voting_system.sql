-- set up user Mysql server and 
-- set up username and password in app.py
-- command for setup mysql

CREATE DATABASE IF NOT EXISTS voting_system;
USE voting_system;

CREATE TABLE IF NOT EXISTS voters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    voter_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    place VARCHAR(100) NOT NULL,
    voted BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    place VARCHAR(100) NOT NULL,
    party_symbol VARCHAR(255),
    votes INT DEFAULT 0
);