-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 01, 2022 at 07:18 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `circket`
--

-- --------------------------------------------------------

--
-- Table structure for table `captian`
--

CREATE TABLE `captian` (
  `Team_id` int(10) NOT NULL,
  `Player_id` varchar(10) NOT NULL,
  `Team_Name` varchar(30) NOT NULL,
  `Captian_name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `captian`
--

INSERT INTO `captian` (`Team_id`, `Player_id`, `Team_Name`, `Captian_name`) VALUES
(222, 'aus1', 'Australia', 'Aron finch'),
(333, 'pak1', 'Pakistan', 'Babar azam'),
(444, 'eng1', 'England', 'Buttler'),
(555, 'nez1', 'Newzeland', 'Kane williomson'),
(666, 'wi1', 'westindies', 'Nicholas pooran'),
(111, 'ind1', 'India', 'Rohit sharma');

-- --------------------------------------------------------

--
-- Table structure for table `coach`
--

CREATE TABLE `coach` (
  `Coach_id` int(10) NOT NULL,
  `C_Name` varchar(30) NOT NULL,
  `Team_Name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `coach`
--

INSERT INTO `coach` (`Coach_id`, `C_Name`, `Team_Name`) VALUES
(11, 'Rahul dravid', 'India'),
(22, 'Mcdonald', 'Australia'),
(33, 'Mathew hyden', 'Pakistan'),
(44, 'McCullum', 'England'),
(55, 'Stead', 'Newzland'),
(66, 'Simmons', 'Westindies');

-- --------------------------------------------------------

--
-- Table structure for table `matches`
--

CREATE TABLE `matches` (
  `Match_ID` varchar(11) NOT NULL,
  `T1_Name` varchar(30) NOT NULL,
  `T2_Name` varchar(30) NOT NULL,
  `Stadium` varchar(100) NOT NULL,
  `Match_Date_Time` datetime NOT NULL,
  `Winner` varchar(30) NOT NULL,
  `Losser` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `matches`
--

INSERT INTO `matches` (`Match_ID`, `T1_Name`, `T2_Name`, `Stadium`, `Match_Date_Time`, `Winner`, `Losser`) VALUES
('m1', 'India', 'England', 'Chinnaswamy Bengaluru', '2022-11-01 10:00:00', 'India', 'England'),
('m2', 'India', 'Pakistan', 'Eden gardens', '2022-12-02 10:00:00', '', ''),
('m3', 'Pakistan', 'Newzeland', 'Wankhede Mumbai', '2022-11-05 10:00:01', 'Newzeland', 'Pakistan'),
('m5', 'England', 'Newzeland', 'Ferosha kotla stadium, New delhi', '2022-11-19 10:00:00', 'Newzeland', 'England');

-- --------------------------------------------------------

--
-- Table structure for table `players`
--

CREATE TABLE `players` (
  `Player_id` varchar(10) NOT NULL,
  `Team_name` varchar(20) NOT NULL,
  `Player_name` varchar(30) NOT NULL,
  `Age` int(10) NOT NULL,
  `No_of_t20` int(10) NOT NULL,
  `Playing_role` varchar(30) NOT NULL,
  `batting_style` varchar(30) NOT NULL,
  `avg` float NOT NULL,
  `Total_runs` int(10) NOT NULL,
  `S R` float NOT NULL,
  `50/100` varchar(30) NOT NULL,
  `bowling_type` varchar(30) DEFAULT NULL,
  `No_of_wicket` int(10) NOT NULL,
  `economy` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `players`
--

INSERT INTO `players` (`Player_id`, `Team_name`, `Player_name`, `Age`, `No_of_t20`, `Playing_role`, `batting_style`, `avg`, `Total_runs`, `S R`, `50/100`, `bowling_type`, `No_of_wicket`, `economy`) VALUES
('aus1', 'Australia', 'Aron finch', 36, 103, 'batting', 'right handed', 34.29, 3120, 142.35, '19/2', '', 0, 0),
('aus7', 'Australia', 'Zampa', 30, 72, 'bowling', 'right handed', 6, 48, 82.76, '0/0', 'right arm leg break', 82, 6.93),
('eng1', 'England', 'Buttler', 32, 103, 'batting', 'right handed', 34.69, 2602, 144.32, '19/1', '', 0, 0),
('eng6', 'England', 'Sam curran', 24, 35, 'All rounder', 'left handed ', 12, 158, 130.58, '0/0', 'left arm medium fast', 41, 7.71),
('ind1', 'India', 'Rohit sharma', 36, 148, 'batting', 'right hand', 31.33, 2768, 139, '29/4', '', 0, 0),
('ind2', 'India', 'Rishabh pant', 25, 66, 'batting', 'left handed', 22.43, 987, 126.38, '3/0', '', 0, 0),
('nez1', 'Newzland', 'Kane williomson', 32, 87, 'batting', 'right handed', 33.3, 2464, 123.02, '17/0', 'right arm off break', 6, 8.34),
('nez2', 'Newzland', 'Conway', 31, 35, 'batting', 'left handed', 48.75, 1170, 130.58, '8/0', '', 0, 0),
('pak1', 'Pakistan', 'Babar azam', 28, 99, 'batting', 'right handed', 41.42, 3355, 127.81, '30/2', '', 0, 0),
('pak2', 'Pakistan', 'Rizwan', 30, 80, 'batting', 'right handed', 48.8, 2635, 126.62, '23/1', '', 0, 0),
('wi1', 'West indies', 'nicholas pooran', 27, 72, 'batting', 'left handed', 25.48, 1427, 129.03, '9/0', '', 0, 0),
('wi5', 'West indies', 'Hitmyer', 26, 50, 'batting', 'left handed', 20.97, 797, 118.42, '4/0', '', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `team`
--

CREATE TABLE `team` (
  `Team_id` int(10) NOT NULL,
  `Team_Name` varchar(30) NOT NULL,
  `Team_Rank` int(10) NOT NULL,
  `Captain_Name` varchar(30) NOT NULL,
  `Number_of_wins` int(10) NOT NULL,
  `Number_of_losses` int(10) NOT NULL,
  `Wicket_Keeper` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `team`
--

INSERT INTO `team` (`Team_id`, `Team_Name`, `Team_Rank`, `Captain_Name`, `Number_of_wins`, `Number_of_losses`, `Wicket_Keeper`) VALUES
(111, 'India', 1, 'Rohit sharma', 6, 0, 'Rishabh pant'),
(222, 'Australia', 2, 'Aron finch', 3, 3, 'Mathew wade'),
(333, 'Pakistan', 3, 'Babar azam', 0, 6, 'Rizwan'),
(444, 'England', 4, 'Buttler', 2, 4, 'Buttler'),
(555, 'Newzeland', 5, 'Kane williomson', 5, 1, 'Conway'),
(666, 'Westindies', 6, 'Nikolus pooran', 1, 5, 'Nikolous pooran');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(10) NOT NULL,
  `username` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`) VALUES
(1, 'satwick', 'satwick@gmail.com', 'satwick'),
(2, 'ameet', 'ameet@gmail.com', 'ameet');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `captian`
--
ALTER TABLE `captian`
  ADD KEY `fk_c` (`Player_id`),
  ADD KEY `fk_c1` (`Team_id`);

--
-- Indexes for table `coach`
--
ALTER TABLE `coach`
  ADD PRIMARY KEY (`Coach_id`);

--
-- Indexes for table `matches`
--
ALTER TABLE `matches`
  ADD PRIMARY KEY (`Match_ID`);

--
-- Indexes for table `players`
--
ALTER TABLE `players`
  ADD PRIMARY KEY (`Player_id`);

--
-- Indexes for table `team`
--
ALTER TABLE `team`
  ADD PRIMARY KEY (`Team_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `captian`
--
ALTER TABLE `captian`
  ADD CONSTRAINT `fk_c` FOREIGN KEY (`Player_id`) REFERENCES `players` (`Player_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_c1` FOREIGN KEY (`Team_id`) REFERENCES `team` (`Team_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
