CREATE DATABASE IF NOT EXISTS shoppingdb;
CREATE USER IF NOT EXISTS 'mahasan'@'%' IDENTIFIED BY 'mahasandatabase';
GRANT ALL PRIVILEGES ON shoppingdb.* TO 'mahasan'@'%';
FLUSH PRIVILEGES;

USE shoppingdb;

CREATE TABLE IF NOT EXISTS shopping_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    plan_id INT,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (plan_id) REFERENCES shopping_plans(id)
);
