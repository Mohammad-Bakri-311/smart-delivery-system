-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 25, 2026 at 05:25 PM
-- Server version: 8.4.7
-- PHP Version: 8.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_delivery`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart_items`
--

DROP TABLE IF EXISTS `cart_items`;
CREATE TABLE IF NOT EXISTS `cart_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_cart_customer` (`customer_id`),
  KEY `fk_cart_product` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `cart_items`
--

INSERT INTO `cart_items` (`id`, `customer_id`, `product_id`, `quantity`, `created_at`) VALUES
(17, 4, 444, 1, '2026-04-25 16:26:41'),
(18, 4, 443, 1, '2026-04-25 16:26:43');

-- --------------------------------------------------------

--
-- Table structure for table `drivers`
--

DROP TABLE IF EXISTS `drivers`;
CREATE TABLE IF NOT EXISTS `drivers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `vehicle_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `current_x` double DEFAULT NULL,
  `current_y` double DEFAULT NULL,
  `status` enum('available','busy') COLLATE utf8mb4_unicode_ci DEFAULT 'available',
  PRIMARY KEY (`id`),
  KEY `fk_drivers_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `drivers`
--

INSERT INTO `drivers` (`id`, `user_id`, `phone`, `vehicle_type`, `current_x`, `current_y`, `status`) VALUES
(1, 2, '0500000000', 'Motorcycle', 32.928, 35.305, 'available');

-- --------------------------------------------------------

--
-- Table structure for table `markets`
--

DROP TABLE IF EXISTS `markets`;
CREATE TABLE IF NOT EXISTS `markets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `owner_id` int DEFAULT NULL,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `open_time` time DEFAULT NULL,
  `close_time` time DEFAULT NULL,
  `is_active` tinyint DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `image_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `owner_id` (`owner_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `markets`
--

INSERT INTO `markets` (`id`, `owner_id`, `name`, `address`, `latitude`, `longitude`, `open_time`, `close_time`, `is_active`, `created_at`, `image_url`) VALUES
(1, NULL, 'Burger House', 'Tel Aviv', 32.0853, 34.7818, '08:00:00', '23:00:00', 1, '2026-04-24 19:37:55', NULL),
(3, NULL, 'Pharmacy Plus', 'Netanya', 32.3215, 34.8532, '08:00:00', '23:00:00', 1, '2026-04-24 19:37:55', NULL),
(4, NULL, 'Fresh Market', 'Nazareth', 32.6996, 35.3035, '08:00:00', '23:00:00', 1, '2026-04-24 19:37:55', NULL),
(5, NULL, 'Sushi Express', 'Karmiel', 32.9172, 35.305, '08:00:00', '23:00:00', 1, '2026-04-24 19:37:55', NULL),
(6, NULL, 'Bakery Fresh', 'Sakhnin', 32.8642, 35.2971, '08:00:00', '23:00:00', 1, '2026-04-24 19:37:55', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
CREATE TABLE IF NOT EXISTS `notifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `message` text COLLATE utf8mb4_unicode_ci,
  `is_read` tinyint DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_notifications_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `title`, `message`, `is_read`, `created_at`) VALUES
(1, 4, 'Market Order Created', 'Order #1 was created.', 1, '2026-04-24 14:27:32'),
(2, 4, 'Payment Successful', 'Payment for order #1 completed.', 1, '2026-04-24 14:33:19'),
(3, 4, 'Market Order Created', 'Order #2 was created.', 1, '2026-04-24 16:46:14'),
(4, 4, 'Payment Successful', 'Payment for order #2 completed successfully.', 1, '2026-04-24 16:46:50'),
(5, 4, 'Order Created', 'Custom delivery order #3 was created.', 1, '2026-04-24 16:50:23'),
(6, 4, 'Market Order Created', 'Order #4 was created.', 1, '2026-04-24 21:12:14'),
(7, 6, 'Market Order Created', 'Order #5 was created.', 0, '2026-04-24 23:28:52'),
(8, 6, 'Market Order Created', 'Order #6 was created.', 0, '2026-04-24 23:32:05'),
(9, 6, 'Market Order Created', 'Order #7 was created.', 0, '2026-04-24 23:34:44'),
(10, 4, 'Market Order Created', 'Order #8 was created.', 1, '2026-04-25 11:47:32');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `driver_id` int DEFAULT NULL,
  `pickup_address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `delivery_address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pickup_x` double DEFAULT NULL,
  `pickup_y` double DEFAULT NULL,
  `delivery_x` double DEFAULT NULL,
  `delivery_y` double DEFAULT NULL,
  `package_description` text COLLATE utf8mb4_unicode_ci,
  `status` enum('pending','assigned','picked_up','delivered','cancelled') COLLATE utf8mb4_unicode_ci DEFAULT 'pending',
  `distance_to_driver` double DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `market_id` int DEFAULT NULL,
  `total_price` double DEFAULT '0',
  `payment_status` enum('unpaid','paid','failed') COLLATE utf8mb4_unicode_ci DEFAULT 'unpaid',
  `stripe_session_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estimated_minutes` int DEFAULT '30',
  `picked_up_at` datetime DEFAULT NULL,
  `delivered_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_orders_customer` (`customer_id`),
  KEY `fk_orders_driver` (`driver_id`),
  KEY `fk_orders_market` (`market_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `customer_id`, `driver_id`, `pickup_address`, `delivery_address`, `pickup_x`, `pickup_y`, `delivery_x`, `delivery_y`, `package_description`, `status`, `distance_to_driver`, `created_at`, `market_id`, `total_price`, `payment_status`, `stripe_session_id`, `estimated_minutes`, `picked_up_at`, `delivered_at`) VALUES
(1, 4, 1, 'Netanya', 'Bi\'ina, Israel', 32.3215, 34.8532, 32.929538, 35.27191699999999, 'Burger x1, Milk x1', 'delivered', 0.7562840008885519, '2026-04-24 14:27:32', NULL, 62, 'paid', NULL, 0, '2026-04-25 01:43:58', '2026-04-25 01:43:58'),
(2, 4, NULL, 'Netanya', 'Lod, Israel', 32.3215, 34.8532, 31.951014, 34.888075, 'Chocolate Cake x1', 'delivered', NULL, '2026-04-24 16:46:14', 6, 22, 'paid', NULL, 0, '2026-04-25 01:34:49', '2026-04-25 01:34:51'),
(3, 4, NULL, 'Arad, Israel', 'Eilat, Israel', 31.26125469999999, 35.2152179, 29.557669, 34.951925, 'keys', 'delivered', NULL, '2026-04-24 16:50:23', NULL, 20, 'paid', NULL, 0, '2026-04-25 01:34:38', '2026-04-25 01:34:40'),
(4, 4, 1, 'Karmiel', 'Bi\'ina, Israel', 32.9172, 35.305, 32.929538, 35.27191699999999, 'Spring Rolls x1, Sunscreen x1, First Aid Kit x1', 'delivered', 0.010799999999996146, '2026-04-24 21:12:13', 5, 83, 'paid', NULL, 0, '2026-04-25 01:34:33', '2026-04-25 01:34:36'),
(5, 6, 1, 'Netanya', 'Haifa, Israel', 32.3215, 34.8532, 32.7940463, 34.989571, 'Baby Wipes x1, Milkshake x1', 'delivered', 0.7562840008885519, '2026-04-24 23:28:52', 3, 28, 'paid', NULL, 0, NULL, '2026-04-25 14:48:11'),
(6, 6, NULL, 'Netanya', 'Haifa, Israel', 32.3215, 34.8532, 32.7940463, 34.989571, 'First Aid Kit x2', 'pending', NULL, '2026-04-24 23:32:05', 3, 70, 'paid', NULL, 30, NULL, NULL),
(7, 6, NULL, 'Netanya', 'Haifa, Israel', 32.3215, 34.8532, 32.7940463, 34.989571, 'Face Masks x1', 'pending', NULL, '2026-04-24 23:34:44', 3, 15, 'paid', NULL, 30, NULL, NULL),
(8, 4, NULL, 'Sakhnin', 'Kiryat Shmona, Israel', 32.8642, 35.2971, 33.20809, 35.5699622, 'Milkshake x1, Spring Rolls x1, Fried Rice x1, Ice Coffee x1', 'pending', NULL, '2026-04-25 11:47:32', 6, 69, 'paid', NULL, 30, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
CREATE TABLE IF NOT EXISTS `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_name` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `price` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_order_items_order` (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_name`, `quantity`, `price`) VALUES
(4, 4, 'Spring Rolls', 1, 18),
(5, 4, 'Sunscreen', 1, 30),
(6, 4, 'First Aid Kit', 1, 35),
(7, 5, 'Baby Wipes', 1, 12),
(8, 5, 'Milkshake', 1, 16),
(9, 6, 'First Aid Kit', 2, 35),
(10, 7, 'Face Masks', 1, 15),
(11, 8, 'Milkshake', 1, 16),
(12, 8, 'Spring Rolls', 1, 18),
(13, 8, 'Fried Rice', 1, 22),
(14, 8, 'Ice Coffee', 1, 13);

-- --------------------------------------------------------

--
-- Table structure for table `order_tracking`
--

DROP TABLE IF EXISTS `order_tracking`;
CREATE TABLE IF NOT EXISTS `order_tracking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `note` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_tracking_order` (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `order_tracking`
--

INSERT INTO `order_tracking` (`id`, `order_id`, `status`, `note`, `created_at`) VALUES
(1, 1, 'created', 'Market order created', '2026-04-24 14:27:32'),
(2, 1, 'paid', 'Demo payment completed', '2026-04-24 14:33:19'),
(3, 2, 'created', 'Market order created', '2026-04-24 16:46:14'),
(4, 2, 'paid', 'Demo card payment completed', '2026-04-24 16:46:50'),
(5, 4, 'created', 'Market order created', '2026-04-24 21:12:13'),
(6, 4, 'paid', 'Demo payment completed', '2026-04-24 21:34:30'),
(7, 4, 'paid', 'Demo payment completed', '2026-04-24 21:38:28'),
(8, 4, 'paid', 'Demo payment completed', '2026-04-24 21:45:25'),
(9, 4, 'paid', 'Demo payment completed', '2026-04-24 21:45:28'),
(10, 3, 'paid', 'Demo payment completed', '2026-04-24 21:45:46'),
(11, 3, 'paid', 'Demo payment completed', '2026-04-24 21:50:51'),
(12, 3, 'paid', 'Demo payment completed', '2026-04-24 21:51:44'),
(13, 3, 'paid', 'Demo payment completed', '2026-04-24 21:53:26'),
(14, 3, 'paid', 'Demo payment completed', '2026-04-24 21:53:28'),
(15, 3, 'paid', 'Demo payment completed', '2026-04-24 21:54:10'),
(16, 3, 'paid', 'Demo payment completed', '2026-04-24 21:54:13'),
(17, 3, 'paid', 'Demo payment completed', '2026-04-24 21:57:34'),
(18, 4, 'picked_up', 'Status updated by admin', '2026-04-24 22:01:40'),
(19, 3, 'picked_up', 'Status updated by admin', '2026-04-24 22:01:43'),
(20, 2, 'picked_up', 'Status updated by admin', '2026-04-24 22:01:45'),
(21, 1, 'picked_up', 'Status updated by admin', '2026-04-24 22:01:48'),
(22, 2, 'delivered', 'Status updated by admin', '2026-04-24 22:01:51'),
(23, 4, 'delivered', 'Status updated by admin', '2026-04-24 22:01:54'),
(24, 3, 'delivered', 'Status updated by admin', '2026-04-24 22:01:55'),
(25, 4, 'picked_up', 'Status updated by admin', '2026-04-24 22:05:55'),
(26, 4, 'delivered', 'Status updated by admin', '2026-04-24 22:05:57'),
(27, 4, 'cancelled', 'Status updated by admin', '2026-04-24 22:06:11'),
(28, 4, 'picked_up', 'Status updated by admin', '2026-04-24 22:34:33'),
(29, 4, 'delivered', 'Status updated by admin', '2026-04-24 22:34:36'),
(30, 3, 'picked_up', 'Status updated by admin', '2026-04-24 22:34:38'),
(31, 3, 'delivered', 'Status updated by admin', '2026-04-24 22:34:40'),
(32, 2, 'picked_up', 'Status updated by admin', '2026-04-24 22:34:41'),
(33, 2, 'delivered', 'Status updated by admin', '2026-04-24 22:34:42'),
(34, 1, 'cancelled', 'Status updated by admin', '2026-04-24 22:34:43'),
(35, 1, 'cancelled', 'Status updated by admin', '2026-04-24 22:34:45'),
(36, 2, 'cancelled', 'Status updated by admin', '2026-04-24 22:34:48'),
(37, 2, 'picked_up', 'Status updated by admin', '2026-04-24 22:34:49'),
(38, 2, 'delivered', 'Status updated by admin', '2026-04-24 22:34:51'),
(39, 1, 'picked_up', 'Status updated by admin', '2026-04-24 22:43:58'),
(40, 5, 'created', 'Market order created', '2026-04-24 23:28:52'),
(41, 5, 'paid', 'Demo payment completed', '2026-04-24 23:29:04'),
(42, 6, 'created', 'Market order created', '2026-04-24 23:32:05'),
(43, 6, 'paid', 'Demo payment completed', '2026-04-24 23:32:20'),
(44, 7, 'created', 'Market order created', '2026-04-24 23:34:44'),
(45, 7, 'paid', 'Demo payment completed', '2026-04-24 23:34:55'),
(46, 8, 'created', 'Market order created', '2026-04-25 11:47:32'),
(47, 8, 'paid', 'Demo payment completed', '2026-04-25 11:48:08');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `market_id` int NOT NULL,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `price` double NOT NULL,
  `image_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_available` tinyint DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_products_market` (`market_id`)
) ENGINE=InnoDB AUTO_INCREMENT=469 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `market_id`, `name`, `description`, `price`, `image_url`, `is_available`, `created_at`) VALUES
(418, 1, 'Chicken Burger', 'Juicy chicken burger', 35, '/static/images/products/Chicken-Burger.jpg', 1, '2026-04-24 19:38:06'),
(419, 1, 'Beef Burger', 'Classic beef burger', 40, '/static/images/products/Beef-Burger.jpg', 1, '2026-04-24 19:38:06'),
(420, 1, 'Cheese Burger', 'With cheese', 42, '/static/images/products/Cheese-Burger.jpg', 1, '2026-04-24 19:38:06'),
(421, 1, 'Double Burger', 'Double meat', 50, '/static/images/products/Double-Burger.jpg', 1, '2026-04-24 19:38:06'),
(422, 1, 'BBQ Burger', 'BBQ flavor', 45, '/static/images/products/BBQ-Burger.jpg', 1, '2026-04-24 19:38:06'),
(423, 1, 'Vegan Burger', 'Plant-based', 38, '/static/images/products/Vegan-Burger.jpg', 1, '2026-04-24 19:38:06'),
(424, 1, 'Fries', 'Crispy fries', 15, '/static/images/products/Fries.jpg', 1, '2026-04-24 19:38:06'),
(425, 1, 'French Fries', 'Large fries', 18, '/static/images/products/French-Fries.jpg', 1, '2026-04-24 19:38:06'),
(426, 1, 'Onion Rings', 'Crunchy', 20, '/static/images/products/Onion-Rings.jpg', 1, '2026-04-24 19:38:06'),
(427, 1, 'Cola Drink', 'Cold drink', 10, '/static/images/products/Cola-Drink.jpg', 1, '2026-04-24 19:38:06'),
(435, 3, 'Toothbrush', 'Soft brush', 10, '/static/images/products/Toothbrush.jpg', 1, '2026-04-24 19:39:43'),
(436, 3, 'Toothpaste', 'Clean teeth', 12, '/static/images/products/Toothpaste.jpg', 1, '2026-04-24 19:39:43'),
(437, 3, 'Shampoo', 'Hair care', 18, '/static/images/products/Shampoo.jpg', 1, '2026-04-24 19:39:43'),
(438, 3, 'Body Lotion', 'Skin care', 22, '/static/images/products/Body-Lotion.jpg', 1, '2026-04-24 19:39:43'),
(439, 3, 'Face Masks', 'Protection', 15, '/static/images/products/Face-Masks.jpg', 1, '2026-04-24 19:39:43'),
(440, 3, 'Cough Syrup', 'Cold medicine', 20, '/static/images/products/Cough-Syrup.jpg', 1, '2026-04-24 19:39:43'),
(441, 3, 'Pain Relief Tablets', 'Pain relief', 14, '/static/images/products/Pain-Relief-Tablets.jpg', 1, '2026-04-24 19:39:43'),
(442, 3, 'First Aid Kit', 'Emergency kit', 35, '/static/images/products/First-Aid-Kit.jpg', 1, '2026-04-24 19:39:43'),
(443, 3, 'Baby Wipes', 'For babies', 12, '/static/images/products/Baby-Wipes.jpg', 1, '2026-04-24 19:39:43'),
(444, 3, 'Sunscreen', 'UV protection', 30, '/static/images/products/Sunscreen.jpg', 1, '2026-04-24 19:39:43'),
(445, 4, 'Fruit Salad', 'Mixed fruits', 18, '/static/images/products/Fruit-Salad.jpg', 1, '2026-04-24 19:40:41'),
(446, 4, 'Cucumber 1KG', 'Fresh', 8, '/static/images/products/Cucumber-1KG.jpg', 1, '2026-04-24 19:40:41'),
(447, 4, 'Tomatoes 1KG', 'Red tomatoes', 10, '/static/images/products/Tomatoes-1KG.jpg', 1, '2026-04-24 19:40:41'),
(448, 4, 'Salmon Bowl', 'Healthy meal', 45, '/static/images/products/Salmon-Bowl.jpg', 1, '2026-04-24 19:40:41'),
(449, 4, 'Chicken Teriyaki', 'Japanese chicken', 40, '/static/images/products/ChickenTeriyaki.jpg', 1, '2026-04-24 19:40:41'),
(450, 5, 'Sushi Combo', 'Mixed sushi', 60, '/static/images/products/Sushi-Combo.jpg', 1, '2026-04-24 19:41:20'),
(451, 5, 'Tuna Roll', 'Fresh tuna', 30, '/static/images/products/Tuna-Roll.jpg', 1, '2026-04-24 19:41:20'),
(452, 5, 'Vegetarian Sushi', 'Veg sushi', 28, '/static/images/products/Vegetarian-Sushi.jpg', 1, '2026-04-24 19:41:20'),
(453, 5, 'Fried Rice', 'Asian rice', 22, '/static/images/products/Fried-Rice.jpg', 1, '2026-04-24 19:41:20'),
(454, 5, 'Spring Rolls', 'Crispy', 18, '/static/images/products/Spring-Rolls.jpg', 1, '2026-04-24 19:41:20'),
(455, 6, 'Croissant', 'French pastry', 12, '/static/images/products/Croissant.jpg', 1, '2026-04-24 19:42:04'),
(456, 6, 'Baguette', 'French bread', 10, '/static/images/products/Baguette.jpg', 1, '2026-04-24 19:42:04'),
(457, 6, 'Cookies', 'Sweet', 8, '/static/images/products/Cookies.jpg', 1, '2026-04-24 19:42:04'),
(458, 6, 'Donut', 'Sugar donut', 9, '/static/images/products/Donut.jpg', 1, '2026-04-24 19:42:04'),
(459, 6, 'Cheesecake', 'Cheese cake', 20, '/static/images/products/Cheesecake.jpg', 1, '2026-04-24 19:42:04'),
(460, 6, 'Waffle Chocolate', 'Sweet waffle', 18, '/static/images/products/Waffle-Chocolate.jpg', 1, '2026-04-24 19:42:04'),
(462, 6, 'Fruit Cake', 'Mixed fruit cake', 22, '/static/images/products/Fruit-Cake.jpg', 1, '2026-04-24 19:42:04'),
(463, 6, 'Pancake', 'Soft pancake', 15, '/static/images/products/Pancake.jpg', 1, '2026-04-24 19:42:04'),
(464, 6, 'Hot Chocolate', 'Warm drink', 14, '/static/images/products/Hot-Chocolate.jpg', 1, '2026-04-24 19:42:04'),
(465, 6, 'Ice Coffee', 'Cold coffee', 13, '/static/images/products/Ice-Coffee.jpg', 1, '2026-04-24 19:42:04'),
(466, 6, 'Milkshake', 'Sweet drink', 16, '/static/images/products/Milkshake.jpg', 1, '2026-04-24 19:42:04');

-- --------------------------------------------------------

--
-- Table structure for table `support_tickets`
--

DROP TABLE IF EXISTS `support_tickets`;
CREATE TABLE IF NOT EXISTS `support_tickets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `order_id` int DEFAULT NULL,
  `subject` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `message` text COLLATE utf8mb4_unicode_ci,
  `status` enum('open','closed') COLLATE utf8mb4_unicode_ci DEFAULT 'open',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `admin_reply` text COLLATE utf8mb4_unicode_ci,
  `reply_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_support_customer` (`customer_id`),
  KEY `fk_support_order` (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `support_tickets`
--

INSERT INTO `support_tickets` (`id`, `customer_id`, `order_id`, `subject`, `message`, `status`, `created_at`, `admin_reply`, `reply_at`) VALUES
(4, 4, 4, 'Order problem', 'i have waited alot and nothing happen for now what the problem ?', 'closed', '2026-04-24 23:24:05', 'we are sorry for that,  will check this and found a fast solve thanks for support us.', '2026-04-25 02:24:53'),
(5, 6, 5, 'thanks', 'thank you this site is very good and all is easy to use', 'closed', '2026-04-24 23:29:51', NULL, NULL),
(6, 6, 6, 'thank you', 'iukgigiugl', 'closed', '2026-04-24 23:32:45', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('customer','driver','admin') COLLATE utf8mb4_unicode_ci DEFAULT 'customer',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `full_name`, `email`, `password`, `role`, `created_at`) VALUES
(1, 'Admin', 'admin@gmail.com', '1234', 'admin', '2026-04-24 14:19:50'),
(2, 'Driver One', 'driver@gmail.com', '1234', 'driver', '2026-04-24 14:19:50'),
(4, 'Mohammad Bakri', 'hajaj.bakri@gmail.com', '1234', 'customer', '2026-04-24 14:20:28'),
(6, 'john', 'john@gmail.com', '1234', 'customer', '2026-04-24 23:25:16');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD CONSTRAINT `fk_cart_customer` FOREIGN KEY (`customer_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_cart_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `drivers`
--
ALTER TABLE `drivers`
  ADD CONSTRAINT `fk_drivers_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `fk_notifications_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `fk_orders_customer` FOREIGN KEY (`customer_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_orders_driver` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_orders_market` FOREIGN KEY (`market_id`) REFERENCES `markets` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `fk_order_items_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `order_tracking`
--
ALTER TABLE `order_tracking`
  ADD CONSTRAINT `fk_tracking_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `fk_products_market` FOREIGN KEY (`market_id`) REFERENCES `markets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `support_tickets`
--
ALTER TABLE `support_tickets`
  ADD CONSTRAINT `fk_support_customer` FOREIGN KEY (`customer_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_support_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
