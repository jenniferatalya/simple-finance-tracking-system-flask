-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 21, 2022 at 07:54 AM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tiny_jar`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `cust_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_name` varchar(50) DEFAULT NULL,
  `cust_addr` text,
  `cust_tlp` varchar(20) DEFAULT NULL,
  `cust_state` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`cust_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`cust_id`, `cust_name`, `cust_addr`, `cust_tlp`, `cust_state`) VALUES
(1, 'hAII', 'Kos Deltu', '081326116108', 'Active'),
(2, 'Jabez Pengen Punya Pacar', 'Dorm - 1908', '081362625819', 'Active'),
(3, 'Chef Renata', 'Belakang Mall Kelapa Gading', '081226706010', 'Active'),
(4, 'Timothy bukan Wijaya', 'Kosan deket Jennifer', '081542335768', 'Active'),
(5, 'Jennifer Oke', 'Kosan', '10010101001', 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
CREATE TABLE IF NOT EXISTS `role` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(15) DEFAULT NULL,
  `authority` text,
  PRIMARY KEY (`role_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`role_id`, `role_name`, `authority`) VALUES
(2, 'finance', 'nanti dulu.'),
(3, 'manager', 'nanti'),
(1, 'sales admin', 'ntar');

-- --------------------------------------------------------

--
-- Table structure for table `sales_invoice`
--

DROP TABLE IF EXISTS `sales_invoice`;
CREATE TABLE IF NOT EXISTS `sales_invoice` (
  `id_trans` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime DEFAULT NULL,
  `cust_id` int(11) DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  `remark` text,
  `state` varchar(10) DEFAULT NULL,
  `paid_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id_trans`),
  KEY `cust_id` (`cust_id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sales_invoice`
--

INSERT INTO `sales_invoice` (`id_trans`, `date`, `cust_id`, `total`, `remark`, `state`, `paid_date`) VALUES
(9, '2022-10-21 00:00:00', 2, 16000, 'Beli takoyaki', 'Void', '2022-10-21 14:22:52'),
(8, '2022-10-21 00:00:00', 1, 15000, 'Buat makan di zaki', 'Paid', '2022-10-21 14:22:52'),
(4, '2022-10-21 00:00:00', 1, 20000, 'Ngutang', 'Paid', '2022-10-21 14:22:52'),
(5, '2022-10-21 00:00:00', 2, 80000, 'Belum gajian', 'Unpaid', NULL),
(6, '2022-10-21 00:00:00', 3, 13000, 'Pinjem', 'Unpaid', NULL),
(7, '2022-10-21 00:00:00', 4, 150000, 'Buat jalan sama pacar', 'Unpaid', NULL),
(10, '2022-10-21 00:00:00', 3, 75000, 'Beli album BTS', 'Unpaid', NULL),
(11, '2022-10-21 00:00:00', 4, 600000, 'Buat bayar member GYM', 'Unpaid', NULL),
(12, '2022-10-21 00:00:00', 2, 25000, 'lalala', 'Unpaid', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) DEFAULT NULL,
  `user_pswd` varchar(64) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `role_id` (`role_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1023 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `user_name`, `user_pswd`, `role_id`) VALUES
(1021, 'renatavalencia', 'renatacantik', 1),
(208, 'jenniferatalya', 'jennifercantik', 2),
(123, 'timothylovejennie', 'forever', 3),
(1022, 'Jabez Joeniko', 'matcha', 3);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
