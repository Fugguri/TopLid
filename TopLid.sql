-- MariaDB dump 10.19  Distrib 10.9.4-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: TopLid
-- ------------------------------------------------------
-- Server version	10.9.4-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(512) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES
(8,'/admin'),
(1,'fugguri'),
(2,'Son2421'),
(4,'Назад');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chats`
--

DROP TABLE IF EXISTS `chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chat` varchar(512) NOT NULL,
  `chat_num` int(11) DEFAULT NULL,
  `chat_title` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chat` (`chat`)
) ENGINE=InnoDB AUTO_INCREMENT=941 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chats`
--

LOCK TABLES `chats` WRITE;
/*!40000 ALTER TABLE `chats` DISABLE KEYS */;
INSERT INTO `chats` VALUES
(1,'AboutBusinessnews',1726215181,'ПроБизнесНовости'),
(90,'kommercheskay',1712116640,'Коммерческая Недвижимость | Москва бизнес'),
(119,'kvartiryvmoskve',1607483225,'Продажа недвижимости — Москва'),
(166,'travlmechat',1588466758,'TravelMe | Недвижимость Москва и Санкт-Петербург'),
(179,'novosib_ndv',1685018906,'Недвижимость Новосибирска'),
(195,'Posredniki_Rus',1208767045,'БИЗНЕС ЧАТ | Предприниматели'),
(224,'freelead',1428955589,'БИЗНЕС ЧАТ | ПРЕДПРИНИМАТЕЛИ🤝'),
(291,'biznes_chat',1371121321,'БИЗНЕС-ЧАТ № 1 | Предприниматели'),
(359,'bk_kit',1235644054,'Бизнес-сообщество \"КИТ\"'),
(389,'seniorsql',1468396285,'Senior SQL Developer'),
(588,'forumdubai',1690810154,'ДубайЧё Чат • Жизнь в Дубае • Общение • Переезд'),
(787,'rent_in_dubai',1144748083,'Аренда Дубай: сдам/сниму'),
(844,'Fugguri_test',1845240182,'Tecтовая группа'),
(880,'frilancru',1289147868,'ФРИЛАНС ЧАТ | ФРИЛАНС БИРЖА'),
(917,'pybotg',1565231422,'Python Telegram Bot'),
(929,'UAE_chat',1480867611,'РУССКОЯЗЫЧНЫЕ В ОАЭ | ДУБАЙ ЧАТ'),
(930,'biznesuae',1282199221,'№1 Бизнес чат Дубай / Мероприятия, нетворкинг, общение и реклама в ОАЭ.'),
(935,'moscoworkk',1712857891,'РАБОТА и УСЛУГИ'),
(937,'exchange_reklama',1341594690,'Реклама | Биржа'),
(938,'adm_telegram',1403878209,'Реклама | Админы Телеграм'),
(939,'tgm_adm',1444874452,'Админы Телеграм | Реклама'),
(940,'tgm_trade',1434229785,'Реклама в Телеграм');
/*!40000 ALTER TABLE `chats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keywords`
--

DROP TABLE IF EXISTS `keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(512) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `word` (`word`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keywords`
--

LOCK TABLES `keywords` WRITE;
/*!40000 ALTER TABLE `keywords` DISABLE KEYS */;
INSERT INTO `keywords` VALUES
(15,'/start'),
(2,'Btdhb'),
(16,'python'),
(17,'бот'),
(22,'Инвестировать в недвижимость'),
(41,'Инвестирую в недвижимость'),
(12,'Ищу'),
(5,'Ищу квартиру'),
(10,'Ищу клиентов'),
(21,'Ищу недвижимость'),
(43,'Ищу продюсера'),
(34,'Квартира'),
(30,'Квартира в Дубае'),
(35,'Квартиру'),
(46,'Кто занимается продвижением телеграмм каналов'),
(8,'Кулю дом'),
(13,'Купить'),
(26,'Купить новостройку'),
(14,'Купить рекламу'),
(3,'куплю'),
(24,'Куплю апартаменты'),
(25,'Куплю виллу'),
(6,'Куплю квартиру'),
(39,'Куплю квартиру в Москве'),
(40,'Куплю новостройку'),
(4,'Куплю рекламу'),
(20,'Недвижемость'),
(27,'Недвижимость в Дубае'),
(29,'Недвижимость в Таиланде'),
(28,'Недвижимость в Тайланде'),
(45,'Нужен продюсер'),
(36,'Нужна квартира'),
(11,'Нужны клиенты'),
(7,'Сниму квартиру'),
(1,'Текст');
/*!40000 ALTER TABLE `keywords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unex_words`
--

DROP TABLE IF EXISTS `unex_words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unex_words` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(512) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `word` (`word`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unex_words`
--

LOCK TABLES `unex_words` WRITE;
/*!40000 ALTER TABLE `unex_words` DISABLE KEYS */;
INSERT INTO `unex_words` VALUES
(1,'ntrcn'),
(4,'OAdmin'),
(13,'Доход'),
(12,'Маркетинг'),
(8,'Помогу купить квартиру'),
(9,'Помогу продать квартиру'),
(18,'Предлагаю'),
(14,'Продается'),
(2,'Продам'),
(16,'Ремонт'),
(15,'Сдается'),
(11,'Сетевым'),
(3,'Список чатов'),
(10,'Топ инвестиций');
/*!40000 ALTER TABLE `unex_words` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `telegram_id` bigint(20) NOT NULL,
  `full_name` text DEFAULT NULL,
  `username` text DEFAULT NULL,
  `pay_end` text DEFAULT NULL,
  `is_all_chats` int(11) DEFAULT 1,
  `click_left` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `telegram_id` (`telegram_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,248184623,'Никита Радзюк','fugguri','2023-01-26',1,74),
(2,5909883622,'Ппппп','popidal','2023-01-24',1,2),
(3,1358110465,'Ilya','son2421','2023-01-24',1,0),
(6,439480420,'𒆜𝔸𝕝𝕖𝕩𝕖𝕪𒆜','al8891','2023-01-25',1,2),
(11,565331673,'Мастер По всем вопросам','masternavseruki1','2022-12-25',1,2),
(12,5775778456,'I N','izzat_nasri','2023-01-26',1,2),
(13,309276932,'Илья Бабайцев | Инвестиции в недвижимость','ilia_babaycev','2023-01-27',1,200),
(14,1026968356,'S','esofcos7','2022-12-27',1,0),
(15,1806092395,'Рабочий аккаунт','jobaccount21','2023-01-28',1,0),
(16,270027852,'Кирилл Игнатьев','Ignatiev_Kirill','2022-12-28',1,0),
(17,557307227,'Александр','kontextologiya','2022-12-29',1,0),
(19,730881710,'Стас','Stasyan1703','2023-01-30',1,10);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_chats`
--

DROP TABLE IF EXISTS `users_chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_chats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `chat_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chat_id` (`chat_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `users_chats_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `users_chats_ibfk_2` FOREIGN KEY (`chat_id`) REFERENCES `chats` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=941 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_chats`
--

LOCK TABLES `users_chats` WRITE;
/*!40000 ALTER TABLE `users_chats` DISABLE KEYS */;
INSERT INTO `users_chats` VALUES
(90,3,90),
(119,3,119),
(166,3,166),
(179,3,179),
(224,3,224),
(291,3,291),
(359,3,359),
(588,15,588),
(929,3,929),
(930,3,930),
(935,1,935),
(936,1,844),
(937,1,937),
(938,1,938),
(939,1,939),
(940,1,940);
/*!40000 ALTER TABLE `users_chats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_keywords`
--

DROP TABLE IF EXISTS `users_keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `keyword_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `keyword_id` (`keyword_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `users_keywords_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `users_keywords_ibfk_2` FOREIGN KEY (`keyword_id`) REFERENCES `keywords` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_keywords`
--

LOCK TABLES `users_keywords` WRITE;
/*!40000 ALTER TABLE `users_keywords` DISABLE KEYS */;
INSERT INTO `users_keywords` VALUES
(1,1,1),
(4,3,4),
(5,3,5),
(6,3,6),
(7,3,7),
(8,3,8),
(10,3,10),
(11,3,11),
(16,1,16),
(20,3,20),
(21,13,21),
(22,13,22),
(24,13,24),
(25,13,25),
(26,13,26),
(27,13,27),
(28,13,28),
(29,13,29),
(31,13,30),
(32,1,17),
(34,3,34),
(35,3,35),
(36,3,36),
(38,1,12),
(39,13,39),
(40,13,40),
(41,13,41),
(43,3,43),
(45,3,45),
(46,3,46);
/*!40000 ALTER TABLE `users_keywords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_unex_words`
--

DROP TABLE IF EXISTS `users_unex_words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_unex_words` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `unex_word_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unex_word_id` (`unex_word_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `users_unex_words_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `users_unex_words_ibfk_2` FOREIGN KEY (`unex_word_id`) REFERENCES `unex_words` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_unex_words`
--

LOCK TABLES `users_unex_words` WRITE;
/*!40000 ALTER TABLE `users_unex_words` DISABLE KEYS */;
INSERT INTO `users_unex_words` VALUES
(1,1,1),
(5,3,4),
(6,3,3),
(7,3,2),
(8,13,8),
(9,13,9),
(10,13,10),
(11,1,11),
(12,1,12),
(13,1,13),
(14,3,14),
(15,3,15),
(16,3,16),
(18,3,18);
/*!40000 ALTER TABLE `users_unex_words` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-01  5:28:47
