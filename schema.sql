CREATE TABLE `persons` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `age` int NOT NULL,
  `email` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `person_id` int NOT NULL,
  `username` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
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

CREATE VIEW get_orders AS 
SELECT
p.product_name,
p.product_stock,
p.price,
p.category,
p.image_name
o.id,
o.order_name,
o.quantity,
o.size,
u.id,
u.username,
u.password
FROM products p
INNER JOIN orders o ON o.product_id = p.id INNER JOIN
users u ON o.user_id = u.id;


CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `order_name` varchar(200) NOT NULL,
  `quantity` varchar(200) NOT NULL,
  `size` varchar(200) NOT NULL,
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
CREATE PROCEDURE create_order(
  IN p_product_name VARCHAR(200),
  IN p_product_stock INT,
  IN p_price DECIMAL(10,2),
  IN p_category VARCHAR(200),
  IN p_image_name VARCHAR(200),
  IN p_order_name VARCHAR(200),
  IN p_quantity INT,
  IN p_size VARCHAR(200),
  IN p_username VARCHAR(200),
  IN p_password VARCHAR(200)
)
BEGIN
  DECLARE v_product_id INT;
  DECLARE v_user_id INT;


  INSERT INTO products(product_name, product_stock, price, category, image_name) 
  VALUES(p_product_name, p_product_stock, p_price, p_category, p_image_name);
  SET v_product_id = LAST_INSERT_ID();
  
  SELECT id INTO v_user_id FROM users WHERE username = p_username AND password = p_password;

  INSERT INTO orders(product_id, user_id, order_name, quantity, size) 
  VALUES(v_product_id, v_user_id, p_order_name, p_quantity, p_size);

  SELECT LAST_INSERT_ID() AS id;
END$$
DELIMITER ;


CREATE TABLE `products` (
  `id` INT NOT NULL,
  `product_name` VARCHAR(45) NOT NULL,
  `product_stock` INT NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  `image_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));

INSERT INTO products (id, category, product_name,product_stock, price, image_name)
VALUES 
  (1, 'Dress', 'Celestial Charm Dress', 30, 80.00, 'dress1.png'),
  (2, 'Dress', 'Midnight Bloom Gown', 30, 70.00, 'dress2.png'),
  (3, 'Dress', 'Enchanting Ember Dress', 30, 90.00, 'dress3.png'),
  (4, 'Dress', 'Serene Serendipity Frock', 30, 135.00, 'dress4.png'),
  (5, 'Dress', 'Velvet Vortex Ensemble', 30, 95.00, 'dress5.png'),
  (6, 'Dress', 'Radiant Rainforest Robe', 30, 140.00, 'dress6.png'),
  (7, 'Pants', 'Stealthy Shadow Trousers', 30, 180.00, 'pants1.png'),
  (8, 'Pants', 'Electric Ember Denim', 30, 190.00, 'pants2.png'),
  (9, 'Pants', 'Cosmic Cascade Pants', 30, 165.00, 'pants3.png'),
  (10, 'Pants', 'Urban Utopia Pants', 30, 155.00, 'pants4.png'),
  (11, 'Pants', 'Crimson Comet Pants', 30, 170.00, 'pants5.png'),
  (12, 'Pants', 'Sapphire Skyline', 30, 165.00, 'pants6.png'),
  (13, 'Skirts', 'Mystic Meadow Skirt', 30, 110.00, 'skirt1.png'),
  (14, 'Skirts', 'Electric Elegance Midi', 30, 115.00, 'skirt2.png'),
  (15, 'Skirts', 'Whimsical Waterfall Wrap', 30, 105.00, 'skirt3.png'),
  (16, 'Skirts', 'Enigmatic Envy', 30, 125.00, 'skirt4.png'),
  (17, 'Skirts', 'Crystal Cascade Skirt', 30, 135.00, 'skirt5.png'),
  (18, 'Skirts', 'Sunlit Serenade Pleated', 30, 130.00, 'skirt6.png'),
  (19, 'Tops', 'Stellar Symphony', 30, 50.00 'top1.png'),
  (20, 'Tops', 'Mirage Melody', 30, 40.00, 'top2.png'),
  (21, 'Tops', 'Enchanted Echo Peplum', 30, 60.00, 'top3.png'),
  (22, 'Tops', 'Midnight Muse', 30, 55.00, 'top4.png'),
  (23, 'Tops', 'Voyage Camisole', 30, 65.00, 'top5.png'),
  (24, 'Tops', 'Celestial Serenity', 30, 70.00, 'top6.png'),
  (25, 'Jackets', 'Celestial Cascade', 30, 200.00, 'jacket1.png'),
  (26, 'Jackets', 'Arctic Aurora', 30, 250.00, 'jacket2.png'),
  (27, 'Jackets', 'Velvet Vortex', 30, 230.00, 'jacket3.png'),
  (28, 'Jackets', 'Ember Parka', 30, 240.00, 'jacket4.png'),
  (29, 'Jackets', 'Urban Utopia', 30, 280.00, 'jacket5.png'),
  (30, 'Jackets', 'Brooklyn New York', 30, 300.00, 'jacket6.png');



-- DELIMITER $$
-- CREATE PROCEDURE update_order(
--   IN order_id int,
--   IN p_product_name varchar(200),
--   IN p_price decimal(10,2),
--   IN p_category varchar(200),
--   IN p_image_name varchar(200),
--   IN p_size varchar(45),
--   IN p_quantity int
-- )
-- BEGIN
--   UPDATE products
--   SET product_name = p_product_name, 
--       price = p_price, 
--       category = p_category, 
--       image_name = p_image_name
--   WHERE id = (SELECT product_id FROM cart_items WHERE id = order_id);

--   UPDATE cart_items
--   SET size = p_size, quantity = p_quantity
--   WHERE id = order_id;

--   SELECT order_id AS id;
-- END$$
-- DELIMITER ;

-- DELIMITER $$
-- CREATE PROCEDURE delete_order(IN order_id int)
-- BEGIN
--   DECLARE v_product_id INT;

--   SELECT product_id INTO v_product_id FROM cart_items WHERE id = order_id;

--   DELETE FROM products WHERE id = v_product_id;
--   DELETE FROM cart_items WHERE id = order_id;
  
--   SELECT order_id AS id;
-- END$$
-- DELIMITER ;