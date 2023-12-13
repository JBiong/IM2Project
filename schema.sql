CREATE TABLE `persons` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `age` int NOT NULL,
  `email` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE VIEW get_users AS 
SELECT
p.name,
p.age,
p.email,
u.id,
u.username,
u.password
FROM persons p
INNER JOIN users u ON u.person_id = p.id;

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `person_id` int NOT NULL,
  `username` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

DELIMITER $$
CREATE PROCEDURE create_user(
    IN p_name VARCHAR(200),
    IN p_age INT,
    IN p_email VARCHAR(200),
    IN p_username VARCHAR(200),
    IN p_password VARCHAR(200)
)
BEGIN
DECLARE v_person_id int;
INSERT INTO persons(name,age,email) VALUES (p_name,p_age, p_email);
SET v_person_id = LAST_INSERT_ID();
INSERT INTO users(person_id,username,password) VALUES (v_person_id,p_username,p_password);
SELECT LAST_INSERT_ID() AS id;
END$$
DELIMITER;

DELIMITER $$
CREATE PROCEDURE update_user(
  IN user_id int,
  IN p_name varchar(200),
  IN p_age int,
  IN p_email varchar(200),
  IN p_username varchar(200),
  IN p_password varchar(200)
)
BEGIN
  UPDATE persons
  INNER JOIN users ON users.person_id = persons.id
  SET name = p_name, age = p_age, email = p_email
  WHERE users.id = user_id;
  UPDATE users SET username = p_username, password = p_password
  WHERE id = user_id;
  SELECT user_id AS id;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE delete_user(IN user_id int)
BEGIN
  DELETE FROM persons WHERE id = (SELECT person_id FROM users WHERE id = user_id);
  DELETE FROM users WHERE id = user_id;
  SELECT user_id AS id;
END$$
DELIMITER ;


CREATE TABLE `products` (
   `product_id` INT PRIMARY KEY AUTO_INCREMENT,
   `product_name` VARCHAR(255) NOT NULL,
   `qty` INT,
   `size` VARCHAR(50),
   `price` DECIMAL(10, 2)
)ENGINE=InnoDB;


DELIMITER $$

CREATE PROCEDURE create_product(
    IN p_product_name VARCHAR(255),
    IN p_qty INT,
    IN p_size VARCHAR(50),
    IN p_price DECIMAL(10, 2)
)
BEGIN
    INSERT INTO Product (product_name, qty, size, price)
    VALUES (p_product_name, p_qty, p_size, p_price);
END $$

DELIMITER ;