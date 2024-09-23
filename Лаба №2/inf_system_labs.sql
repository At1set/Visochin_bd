-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Сен 23 2024 г., 14:01
-- Версия сервера: 8.0.30
-- Версия PHP: 8.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `inf_system_labs`
--

DELIMITER $$
--
-- Процедуры
--
CREATE DEFINER=`root`@`%` PROCEDURE `insertNewJournal` (IN `id` INT, IN `_action` VARCHAR(10), IN `oldValue` VARCHAR(50), IN `newValue` VARCHAR(50))   INSERT INTO `journal` (`id`, `datetime`, `action`, `oldValue`, `newValue`)
VALUES (id, NOW(), _action, oldValue, newValue)$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `employees`
--

CREATE TABLE `employees` (
  `id` int UNSIGNED NOT NULL,
  `name` varchar(10) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Триггеры `employees`
--
DELIMITER $$
CREATE TRIGGER `After_insert` AFTER INSERT ON `employees` FOR EACH ROW CALL insertNewJournal(NEW.id, 'insert', null, NEW.name)
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `Before_delete` BEFORE DELETE ON `employees` FOR EACH ROW CALL insertNewJournal(OLD.id, 'delete', OLD.name, null)
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `Before_update` BEFORE UPDATE ON `employees` FOR EACH ROW CALL insertNewJournal(NEW.id, 'update', OLD.name, NEW.name)
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `journal`
--

CREATE TABLE `journal` (
  `id` int UNSIGNED NOT NULL,
  `datetime` datetime NOT NULL,
  `action` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `oldValue` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `newValue` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Индексы таблицы `journal`
--
ALTER TABLE `journal`
  ADD PRIMARY KEY (`id`,`datetime`),
  ADD UNIQUE KEY `datetime` (`datetime`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `employees`
--
ALTER TABLE `employees`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
