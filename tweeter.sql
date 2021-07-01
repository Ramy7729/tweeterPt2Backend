-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: 35.202.43.44    Database: tweeter
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.18-MariaDB-1:10.4.18+maria~stretch

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `content` varchar(377) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `user_id` int(10) unsigned NOT NULL,
  `tweet_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `comment_FK` (`tweet_id`),
  KEY `comment_FK_1` (`user_id`),
  CONSTRAINT `comment_FK` FOREIGN KEY (`tweet_id`) REFERENCES `tweet` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_FK_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES ('testing comment like','2021-06-29 16:38:43',76,44,58),('Comment test','2021-06-30 04:24:06',77,46,62);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment_like`
--

DROP TABLE IF EXISTS `comment_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment_like` (
  `created_at` datetime DEFAULT current_timestamp(),
  `user_id` int(10) unsigned NOT NULL,
  `comment_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment_like_UN` (`user_id`,`comment_id`),
  KEY `comment_like_FK` (`comment_id`),
  CONSTRAINT `comment_like_FK` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_like_FK_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_like`
--

LOCK TABLES `comment_like` WRITE;
/*!40000 ALTER TABLE `comment_like` DISABLE KEYS */;
INSERT INTO `comment_like` VALUES ('2021-06-29 16:38:53',76,58,113),('2021-06-30 18:54:48',77,58,147);
/*!40000 ALTER TABLE `comment_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follow`
--

DROP TABLE IF EXISTS `follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follow` (
  `created_at` datetime DEFAULT current_timestamp(),
  `user_id` int(10) unsigned NOT NULL,
  `follow_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `follow_UN` (`user_id`,`follow_id`),
  KEY `follow_FK_1` (`follow_id`),
  CONSTRAINT `follow_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `follow_FK_1` FOREIGN KEY (`follow_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `follow_CHECK` CHECK (`user_id` <> `follow_id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follow`
--

LOCK TABLES `follow` WRITE;
/*!40000 ALTER TABLE `follow` DISABLE KEYS */;
INSERT INTO `follow` VALUES ('2021-06-29 19:36:50',77,76,42),('2021-06-30 04:24:43',77,75,44);
/*!40000 ALTER TABLE `follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet`
--

DROP TABLE IF EXISTS `tweet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet` (
  `content` varchar(377) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `image_url` varchar(500) DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tweet_FK` (`user_id`),
  CONSTRAINT `tweet_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet`
--

LOCK TABLES `tweet` WRITE;
/*!40000 ALTER TABLE `tweet` DISABLE KEYS */;
INSERT INTO `tweet` VALUES ('@PrinceAdam You\'re so weak, you have the body type of an elf on a shelf. Thin ankles with your blond hair!','2021-06-29 15:31:49',NULL,44,76),('hallo','2021-06-29 19:36:16',NULL,45,77),('magic','2021-06-30 04:23:35',NULL,46,77);
/*!40000 ALTER TABLE `tweet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet_like`
--

DROP TABLE IF EXISTS `tweet_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet_like` (
  `created_at` datetime DEFAULT current_timestamp(),
  `tweet_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tweet_like_UN` (`tweet_id`,`user_id`),
  KEY `tweet_like_FK_1` (`user_id`),
  CONSTRAINT `tweet_like_FK` FOREIGN KEY (`tweet_id`) REFERENCES `tweet` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tweet_like_FK_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet_like`
--

LOCK TABLES `tweet_like` WRITE;
/*!40000 ALTER TABLE `tweet_like` DISABLE KEYS */;
INSERT INTO `tweet_like` VALUES ('2021-06-29 15:31:52',44,76,34),('2021-06-30 18:54:33',46,77,47),('2021-06-30 18:54:35',44,77,48),('2021-06-30 18:54:36',45,77,49);
/*!40000 ALTER TABLE `tweet_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `username` varchar(50) NOT NULL,
  `email` varchar(255) NOT NULL,
  `bio` varchar(377) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `image_url` varchar(500) DEFAULT NULL,
  `banner_url` varchar(500) DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `password` varchar(150) NOT NULL,
  `salt` varchar(10) DEFAULT NULL,
  `birthdate` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_UN` (`username`),
  UNIQUE KEY `users_UN2` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('David Blaine','davidblaine@hogwarts.com','I am a master magician and my magic is definitely real.','2021-06-29 15:27:34','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFEJ_GnoWkuhwFHYLGj3AzU782Nscj3JdnhQ&usqp=CAU','https://i1.wp.com/decider.com/wp-content/uploads/2016/11/david-blaine-1284e28086c397e28086856.jpg?quality=80&strip=all&ssl=1',75,'33b0ff446692865da3f02889f27153b2cba371107887d4410d206b67617e60d77a518b4bcfd56d5d07f0900810054d20c86ad775a06d6cad964860692b0d83ec','YJE2dRA2Jj','2021-06-29'),('Skeletor','skeletor@hogwarts.com','Just chillin in my crib. Wearing mah purple hood. Lord of Destruction. Overlord of Evil.','2021-06-29 15:29:04','https://i.kym-cdn.com/entries/icons/original/000/017/507/1-13-Skeletor-Orgasm.png','https://www.writeups.org/wp-content/uploads/Castle-Grayskull-Masters-Universe-He-Man-entrance.jpg',76,'abe43aca0a1ff2f34577c36da876b9412938eff42a1cb8c4360cc551d05e17097ee83cc505f4862d2c40f4963012c3b34257e8fd9fd49becfbe0a6816f431d6a','oWyX5fjMxf','2021-06-29'),('Harry Potter','harrypotter@hogwarts.com','I dare say his name!!! Voldemort!','2021-06-29 15:30:13','https://i.ytimg.com/vi/gY_i1LcDObU/maxresdefault.jpg','https://images.dailyhive.com/20200414144211/shutterstock_550323016.jpg',77,'97e00e682c604f0aef8b1e65155f8cdf08f5b614eb1f0676b2f1ab2d285eed4be2a1708e6acae2306dc003461036536e4e6d93021b9cac7df40a61768e128d8a','pStC6Cmd3i','2021-06-29'),('Prince Adam','padam@hogwarts.com','I am Adam. Prince of Eternia and defender of the secrets of Castle Grayskull.','2021-06-29 15:33:55','https://i.kym-cdn.com/entries/icons/facebook/000/002/691/sings.jpg','https://lh3.googleusercontent.com/proxy/tfhV64p3kQAWExOrCqTqxoXyNzBJOApW6UkjbhUmHYa3UOy8StktVnjCaCqEsz7LZGEvdrQ5nRdMTXWh-WVb3D2FORCoiWp-Is7raSsWY9onMJeGSTv18L_iFxzVRdSGu_ubmQcendhvgyw',78,'92d92dc5fffb54db89904bca264f269ce905fc7eba98dfe25a15971c9032cf1252c805da04ab6f1ba376aec48b568fc29038d7a3364177d32b3755f2e6430155','Phz8ki64NN','2021-06-29'),('Se7n','se7n@hogwarts.com','What\'s in the box?','2021-06-29 19:52:14','https://i.pinimg.com/originals/eb/1b/4e/eb1b4eb9f308d86107c362e7bbe535b4.jpg','https://i.pinimg.com/originals/9a/c4/76/9ac476de26acc1acee1ec4be52aadb7d.jpg',79,'ce3da496220422af0dc3461302b4e1911b6b8a091914a99af7577b0fdacf2e88c7968d79390eb86f270c68f0c5051a781192a7ea53d8f3082ddb08303954fb80','F2vSCzFwif','2021-06-29');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_session`
--

DROP TABLE IF EXISTS `user_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_session` (
  `user_id` int(10) unsigned NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `token` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_session_UN` (`token`),
  KEY `user_session_FK` (`user_id`),
  CONSTRAINT `user_session_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_session`
--

LOCK TABLES `user_session` WRITE;
/*!40000 ALTER TABLE `user_session` DISABLE KEYS */;
INSERT INTO `user_session` VALUES (75,105,'zy-eNOZNMYsN0-82s69AbWr7cLMnYbmCc-NKGBwIjRU1Pv5ack53QV_0FBg7yr0LJXFK08GSzhIAcd_KcS0ctwmTLIRnAA'),(76,106,'MRUCFdqF3mLnAVgHDj0vRQYgJqkEdnrs2pGe3yQ_BzKaz283yU-xubd2kE5y1VTxa8QA-Q8ZvwrWfdMHYpu1bFKIKoTCUA'),(77,107,'F6nASdvL2J3c4fXgX2kKil7PkEJWKNL93YT10H86-gXsk8jGT1h0hPYQlRoKRAizf_8VeXOs1R4kBvTmNuf1WX7ay-bO6w'),(76,108,'GqfQUgnUYrahHfFGF5lyJ3S3i2xznnBu6Nj3ZX6IEOQBS6aZlSqxttoJfxGD7dB42-1fGLHXV5cS6UNoJocTg2GAzSV8XA'),(78,109,'NXTnI3d2SX44xCC28yhMJh2BAlZihmd_jRoSwOXGtpfQetTqyGpBro_WP52ABE8Hum_fCOLSUUpdbjt2vWbPepmgvJCBTA'),(76,110,'UB-iPF0mzevsIXvzikLkIPvzGJpy7vlcYSn1QiyD_Eg3KdArKDjeDtb_xDxzzzsuLxIiFgI1sY6IN8B7fZn3MFg2QESeoA'),(76,111,'ze02_Vhlfr8UEFNaY4Tq86Tm4BMMQHIGLEdRWk7SCsPmThdmmKPEQ_3gFFvC09Gm6T13tLxtMk29S9HffC7H1eg_zMlqiw'),(76,112,'1ZrF53zGzlm65fg5-Jr9cjYqAWTcpwvhYLho-TJoMnQ4DPsbFhWg4kmdUKJh-o_lDqFJYfhjyeZGdKLhCDYAzuFvlZ3UhA'),(76,113,'j5WfVZLnX7xfuR6amhPoAywFHPbL8YnsXLIALr0biTetbJzWUi9irZyLQKgATLa5ABqMMzeDxuuA-Z7VgLRvx4qCoH6JDQ'),(77,114,'LdMyX6S1P1umw3SZ2o7v2y_Zj_4q3GsXHaO8A3ZqDBFOqNWBQIiX-wA5-rHrHkywk0oJ2l8CFYuZzpyfHqXB2cRTd1Hleg'),(77,115,'e4IsX0wFYPCBatQgHEgal9w5DRFOdtlcdLJZQE3m170Qa6u0v_NYf81RghS8_Hj6JwsTVirnt5qf2AFQTRSghN4FzVjnIA'),(77,116,'WuOPseHLwuUJFKqBrx0CXLl_Qq-hufOntdTqazoLCghjyowfEY5M128wnbKKI1OMG6OLpiL9nsMOfcSiREE3ShhKOqwdEA'),(77,117,'n2SY7Uf-J9tWfWHulveYdYNIM3wTTKItxlgYDANEVP1_4zv4JRjOppxoDrOxQRKENzU4YQEyd7ytY4WxyjK60Au9T1TcnQ'),(77,118,'wcEEjupRYBRidIlxxxsttz7xP-p_WJamt6KNdVhyh5Xx18_XLNEDPydot4bdShqGjdTZ8EyKWuDUloPEeqL0skIlTG-8pg'),(79,123,'jEFB-t0CpAo5IxHQoqAd8NzIvCClsDOjyR4j6YQf7XofnioMqmleuEzDXeNFQmMrxGN-338-RILlKxda3plzMX44eRBLzg');
/*!40000 ALTER TABLE `user_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'tweeter'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-01 13:48:07
