CREATE SCHEMA `shoppingapp` ;

CREATE TABLE `shoppingapp`.`products` (
  `id` INT NOT NULL,
  `product_name` VARCHAR(45) NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  `image_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `shoppingapp`.`cart_items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `product_id` INT NULL,
  `size` VARCHAR(45) NULL,
  `quantity` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `product_id_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `product_id`
    FOREIGN KEY (`product_id`)
    REFERENCES `shoppingapp`.`products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

INSERT INTO products (id, category, product_name, price, image_name)
VALUES 
  (1, 'Dress', 'Celestial Charm Dress', 80.00, 'dress1.png'),
  (2, 'Dress', 'Midnight Bloom Gown', 70.00, 'dress2.png'),
  (3, 'Dress', 'Enchanting Ember Dress', 90.00, 'dress3.png'),
  (4, 'Dress', 'Serene Serendipity Frock', 135.00, 'dress4.png'),
  (5, 'Dress', 'Velvet Vortex Ensemble', 95.00, 'dress5.png'),
  (6, 'Dress', 'Radiant Rainforest Robe', 140.00, 'dress6.png'),
  (7, 'Pants', 'Stealthy Shadow Trousers', 180.00, 'pants1.png'),
  (8, 'Pants', 'Electric Ember Denim', 190.00, 'pants2.png'),
  (9, 'Pants', 'Cosmic Cascade Pants', 165.00, 'pants3.png'),
  (10, 'Pants', 'Urban Utopia Pants', 155.00, 'pants4.png'),
  (11, 'Pants', 'Crimson Comet Pants', 170.00, 'pants5.png'),
  (12, 'Pants', 'Sapphire Skyline', 165.00, 'pants6.png'),
  (13, 'Skirts', 'Mystic Meadow Skirt', 110.00, 'skirt1.png'),
  (14, 'Skirts', 'Electric Elegance Midi', 115.00, 'skirt2.png'),
  (15, 'Skirts', 'Whimsical Waterfall Wrap', 105.00, 'skirt3.png'),
  (16, 'Skirts', 'Enigmatic Envy', 125.00, 'skirt4.png'),
  (17, 'Skirts', 'Crystal Cascade Skirt', 135.00, 'skirt5.png'),
  (18, 'Skirts', 'Sunlit Serenade Pleated', 130.00, 'skirt6.png'),
  (19, 'Tops', 'Stellar Symphony', 50.00, 'top1.png'),
  (20, 'Tops', 'Mirage Melody', 40.00, 'top2.png'),
  (21, 'Tops', 'Enchanted Echo Peplum', 60.00, 'top3.png'),
  (22, 'Tops', 'Midnight Muse', 55.00, 'top4.png'),
  (23, 'Tops', 'Voyage Camisole', 65.00, 'top5.png'),
  (24, 'Tops', 'Celestial Serenity', 70.00, 'top6.png'),
  (25, 'Jackets', 'Celestial Cascade', 200.00, 'jacket1.png'),
  (26, 'Jackets', 'Arctic Aurora', 250.00, 'jacket2.png'),
  (27, 'Jackets', 'Velvet Vortex', 230.00, 'jacket3.png'),
  (28, 'Jackets', 'Ember Parka', 240.00, 'jacket4.png'),
  (29, 'Jackets', 'Urban Utopia', 280.00, 'jacket5.png'),
  (30, 'Jackets', 'Brooklyn New York', 300.00, 'jacket6.png');

DELIMITER $$
CREATE PROCEDURE create_order(
  IN p_product_name varchar(200),
  IN p_price decimal(10,2),
  IN p_category varchar(200),
  IN p_image_name varchar(200),
  IN p_size varchar(45),
  IN p_quantity int
)
BEGIN
  DECLARE v_product_id INT;

  INSERT INTO products(product_name, price, category, image_name) 
  VALUES(p_product_name, p_price, p_category, p_image_name);
  
  SET v_product_id = LAST_INSERT_ID();
  
  INSERT INTO cart_items(product_id, size, quantity) 
  VALUES(v_product_id, p_size, p_quantity);
  
  SELECT LAST_INSERT_ID() AS id;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE update_order(
  IN order_id int,
  IN p_product_name varchar(200),
  IN p_price decimal(10,2),
  IN p_category varchar(200),
  IN p_image_name varchar(200),
  IN p_size varchar(45),
  IN p_quantity int
)
BEGIN
  UPDATE products
  SET product_name = p_product_name, 
      price = p_price, 
      category = p_category, 
      image_name = p_image_name
  WHERE id = (SELECT product_id FROM cart_items WHERE id = order_id);

  UPDATE cart_items
  SET size = p_size, quantity = p_quantity
  WHERE id = order_id;

  SELECT order_id AS id;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE delete_order(IN order_id int)
BEGIN
  DECLARE v_product_id INT;

  SELECT product_id INTO v_product_id FROM cart_items WHERE id = order_id;

  DELETE FROM products WHERE id = v_product_id;
  DELETE FROM cart_items WHERE id = order_id;
  
  SELECT order_id AS id;
END$$
DELIMITER ;
