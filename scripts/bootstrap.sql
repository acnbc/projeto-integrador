-- Execute com: mysql -u root < scripts/bootstrap.sql
CREATE DATABASE IF NOT EXISTS ufrj CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin';
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON ufrj.* TO 'admin'@'localhost';
GRANT ALL PRIVILEGES ON ufrj.* TO 'admin'@'%';
FLUSH PRIVILEGES;
