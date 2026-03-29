-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: tet_mart_db
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add category',7,'add_category'),(26,'Can change category',7,'change_category'),(27,'Can delete category',7,'delete_category'),(28,'Can view category',7,'view_category'),(29,'Can add product',8,'add_product'),(30,'Can change product',8,'change_product'),(31,'Can delete product',8,'delete_product'),(32,'Can view product',8,'view_product'),(33,'Can add order item',10,'add_orderitem'),(34,'Can change order item',10,'change_orderitem'),(35,'Can delete order item',10,'delete_orderitem'),(36,'Can view order item',10,'view_orderitem'),(37,'Can add order',9,'add_order'),(38,'Can change order',9,'change_order'),(39,'Can delete order',9,'delete_order'),(40,'Can view order',9,'view_order');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-01-22 17:57:16.481929','2','lehongson',1,'[{\"added\": {}}]',6,1),(2,'2026-01-22 17:58:34.640968','2','lehongson',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"S\\u1ed1 \\u0111i\\u1ec7n tho\\u1ea1i\", \"\\u0110\\u1ecba ch\\u1ec9 giao h\\u00e0ng\", \"\\u1ea2nh \\u0111\\u1ea1i di\\u1ec7n\"]}}]',6,1),(3,'2026-01-22 17:59:56.643972','2','lehongson',2,'[]',6,1),(4,'2026-01-22 18:18:27.135241','1','Bánh Kẹo Tết',1,'[{\"added\": {}}]',7,1),(5,'2026-01-22 18:19:55.071683','1','Hộp Bánh Chocopie',1,'[{\"added\": {}}]',8,1),(6,'2026-01-22 19:21:59.211542','2','Kẹo dẻo hương trái cây Chupa Chups Sour Belt gieo quẻ hũ 112g',1,'[{\"added\": {}}]',8,1),(7,'2026-01-23 06:07:36.909101','3','Bánh bông lan tròn vị bơ sữa và dâu Solite Cupcake Selection hộp 288g',1,'[{\"added\": {}}]',8,1),(8,'2026-01-25 19:21:30.028424','3','user',1,'[{\"added\": {}}]',6,1),(9,'2026-01-25 19:26:16.680246','3','user',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"S\\u1ed1 \\u0111i\\u1ec7n tho\\u1ea1i\", \"\\u0110\\u1ecba ch\\u1ec9 giao h\\u00e0ng\", \"\\u1ea2nh \\u0111\\u1ea1i di\\u1ec7n\"]}}]',6,1),(10,'2026-01-26 10:14:51.386880','2','Đèn lồng',1,'[{\"added\": {}}]',7,1),(11,'2026-01-26 10:15:07.084356','1','Bánh Kẹo Tết',3,'',7,1),(12,'2026-01-26 10:15:20.676874','3','Bao lì xì',1,'[{\"added\": {}}]',7,1),(13,'2026-01-26 10:15:46.682084','4','Hoa mai/đào giả',1,'[{\"added\": {}}]',7,1),(14,'2026-01-26 10:19:27.841530','4','Đèn lồng đỏ 30cm',1,'[{\"added\": {}}]',8,1),(15,'2026-01-26 10:21:08.028248','5','Cành đào giả 1m2',1,'[{\"added\": {}}]',8,1),(16,'2026-01-26 10:23:46.939988','6','Set bao lì xì 2026 (20 cái)',1,'[{\"added\": {}}]',8,1),(17,'2026-01-26 10:24:45.084182','6','Set bao lì xì 2026 (20 cái)',2,'[{\"changed\": {\"fields\": [\"M\\u00f4 t\\u1ea3\"]}}]',8,1),(18,'2026-01-26 10:25:00.698392','5','Cành đào giả 1m2',2,'[{\"changed\": {\"fields\": [\"M\\u00f4 t\\u1ea3\"]}}]',8,1),(19,'2026-01-26 10:25:09.104220','4','Đèn lồng đỏ 30cm',2,'[{\"changed\": {\"fields\": [\"M\\u00f4 t\\u1ea3\"]}}]',8,1),(20,'2026-01-27 21:18:51.089711','7','cuckcckc',1,'[{\"added\": {}}]',8,1),(21,'2026-01-27 21:19:33.398296','7','cuckcckc',3,'',8,1),(22,'2026-01-27 21:40:56.827520','8','Set bao lì xì 2026 (20 cái)',1,'[{\"added\": {}}]',8,1),(23,'2026-01-28 08:26:12.038238','9','10 gốc hoa hồng',1,'[{\"added\": {}}]',8,1),(24,'2026-01-28 09:12:13.173871','7','TestĐăngKí',3,'',6,1),(25,'2026-01-28 20:01:33.591301','10','Hoa Hồng',1,'[{\"added\": {}}]',8,1),(26,'2026-03-18 17:35:17.465335','10','Hoa Hồng',2,'[{\"changed\": {\"fields\": [\"\\u1ea2nh s\\u1ea3n ph\\u1ea9m\"]}}]',8,1),(27,'2026-03-18 17:35:25.749836','8','Set bao lì xì 2026 (20 cái)',2,'[{\"changed\": {\"fields\": [\"\\u1ea2nh s\\u1ea3n ph\\u1ea9m\"]}}]',8,1),(28,'2026-03-18 17:35:33.665502','5','Cành đào giả 1m2',2,'[{\"changed\": {\"fields\": [\"\\u1ea2nh s\\u1ea3n ph\\u1ea9m\"]}}]',8,1),(29,'2026-03-18 17:35:42.395729','4','Đèn lồng đỏ 30cm',2,'[{\"changed\": {\"fields\": [\"\\u1ea2nh s\\u1ea3n ph\\u1ea9m\"]}}]',8,1),(30,'2026-03-22 11:07:24.436982','10','Hoa Hồng',2,'[{\"changed\": {\"fields\": [\"\\u1ea2nh s\\u1ea3n ph\\u1ea9m\"]}}]',8,1),(31,'2026-03-22 11:07:34.743810','8','Set bao lì xì 2026 (20 cái)',2,'[{\"changed\": {\"fields\": [\"\\u1ea2nh s\\u1ea3n ph\\u1ea9m\"]}}]',8,1),(32,'2026-03-22 11:07:41.738370','5','Cành đào giả 1m2',2,'[{\"changed\": {\"fields\": [\"\\u1ea2nh s\\u1ea3n ph\\u1ea9m\"]}}]',8,1),(33,'2026-03-22 11:09:27.038892','4','Đèn lồng đỏ 30cm',2,'[{\"changed\": {\"fields\": [\"\\u1ea2nh s\\u1ea3n ph\\u1ea9m\"]}}]',8,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'contenttypes','contenttype'),(9,'orders','order'),(10,'orders','orderitem'),(7,'products','category'),(8,'products','product'),(5,'sessions','session'),(6,'users','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-01-22 17:49:49.750479'),(2,'contenttypes','0002_remove_content_type_name','2026-01-22 17:49:49.830411'),(3,'auth','0001_initial','2026-01-22 17:49:50.021214'),(4,'auth','0002_alter_permission_name_max_length','2026-01-22 17:49:50.072500'),(5,'auth','0003_alter_user_email_max_length','2026-01-22 17:49:50.075850'),(6,'auth','0004_alter_user_username_opts','2026-01-22 17:49:50.080256'),(7,'auth','0005_alter_user_last_login_null','2026-01-22 17:49:50.084368'),(8,'auth','0006_require_contenttypes_0002','2026-01-22 17:49:50.085884'),(9,'auth','0007_alter_validators_add_error_messages','2026-01-22 17:49:50.091616'),(10,'auth','0008_alter_user_username_max_length','2026-01-22 17:49:50.095683'),(11,'auth','0009_alter_user_last_name_max_length','2026-01-22 17:49:50.100114'),(12,'auth','0010_alter_group_name_max_length','2026-01-22 17:49:50.111624'),(13,'auth','0011_update_proxy_permissions','2026-01-22 17:49:50.116395'),(14,'auth','0012_alter_user_first_name_max_length','2026-01-22 17:49:50.119800'),(15,'users','0001_initial','2026-01-22 17:49:50.371527'),(16,'admin','0001_initial','2026-01-22 17:49:50.519806'),(17,'admin','0002_logentry_remove_auto_add','2026-01-22 17:49:50.526566'),(18,'admin','0003_logentry_add_action_flag_choices','2026-01-22 17:49:50.532744'),(19,'products','0001_initial','2026-01-22 17:49:50.640754'),(20,'sessions','0001_initial','2026-01-22 17:49:50.671001'),(22,'orders','0001_initial','2026-01-26 00:32:49.871736');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('69j959wbkp3skvs88kqltdfja4wkjfxb','.eJyNj8tugzAURH8FedVKmPgBscky-666jRT5cQE3YBIwbaIo_14TIbVRVKmba3k8dzzniowaAtpcUT4PrzpAG7SbCKUkTgLSJ-1uomC5r5O7TuerqRJOTIdSdByciTt5QQjJSIpOk_LBhQvaiBS5TtVz4KoD69TqOPR2MmFcfXocg3jOiMBiUKPEHSfnQ-0bQ09M2OwL9DGGj-1Ux3ULHre9r7Ht8fKtUQHqfrj83RbdUiR_Qb1DSLTqZ0N0muS8nIywdfLCSGLuAnWvP1TsmYr-j0oy0ua4q8XgxYVF0cSgR6oRAo6FcOvw2eG5RhzYKPeIt33ujG6Rba-m0OynEYa9s9FHc_QgamUO4OcX-6F83Wem92FwOpst2fI6Zm-9hXa7eB8CGjU2cVsKU9mKQsUNk5WiGjSooiq5VYaXZK11rkEUrBRlDkJTS0ghdE4l57pYg0S3bzUyvW4:1w4jfr:Jez63ahY2RHgABhKeLXLXwjv7Vs1gI5-huqrWR6zKPw','2026-04-06 18:06:47.777088'),('8el789wro6zsf0jk10bsbj1zbw98n4i8','.eJxVjEEOwiAQRe_C2hAKEwZcuvcMhBlAqgaS0q6Md9cmXej2v_f-S4S4rTVsIy9hTuIsjDj9bhT5kdsO0j22W5fc27rMJHdFHnTIa0_5eTncv4MaR_3WsZCavLcGAS0ToAcAnpCZyBSbsvYGXEkOckFN6El5h2BU1OycsuL9Adr_N2E:1vk67f:HD0J2KZFGBcvjFirIVpn2c6Q5dqdJ9wHTk12Y_8tpFA','2026-02-08 19:50:11.399825'),('pmdwmzp2ydekgwad7oixldow1iqo62o4','.eJxVjEEOwiAQRe_C2pBRmKG4dO8ZmoEBqRpISrsy3l2bdKHb_977LzXyupRx7WkeJ1FndVSH3y1wfKS6AblzvTUdW13mKehN0Tvt-tokPS-7-3dQuJdvbZwRCOzZegZAy2DEZiKOJM6B5BMgQMiYMBFmb3wc_JDJBE9i0ar3B9jPN3w:1vlBi5:nqCy_ybWEOAO9I9FR8OyTEsynBXU5geFllP_2Vt57Ao','2026-02-11 20:00:17.818209'),('tt33saal63pa7m8vu6mlxd13f412ckg6','.eJxVjEEOwiAQRe_C2pBRmKG4dO8ZmoEBqRpISrsy3l2bdKHb_977LzXyupRx7WkeJ1FndVSH3y1wfKS6AblzvTUdW13mKehN0Tvt-tokPS-7-3dQuJdvbZwRCOzZegZAy2DEZiKOJM6B5BMgQMiYMBFmb3wc_JDJBE9i0ar3B9jPN3w:1viyxQ:afMzex-mBsuE5M6MII2aS7RniF8Jtz-_KtZuwvgaBn4','2026-02-05 17:59:00.862196'),('vljx7biaqtzuqwdo5waemperybtxhua0','.eJxVjEEOwiAQRe_C2pBRmKG4dO8ZmoEBqRpISrsy3l2bdKHb_977LzXyupRx7WkeJ1FndVSH3y1wfKS6AblzvTUdW13mKehN0Tvt-tokPS-7-3dQuJdvbZwRCOzZegZAy2DEZiKOJM6B5BMgQMiYMBFmb3wc_JDJBE9i0ar3B9jPN3w:1w0zdj:KgD9mwFbFVPpypEJwTXEtxWTNu7O11yWU2H8wWEkVTs','2026-03-27 10:21:07.520966'),('zawrksautfflf41ef6uc0xhagy98qcii','.eJyVkk1v2zAMhv-KodMGRA4l-TPH7tLLTr0WCGhJtrXYUuKPLUGR_z4pzTqnWYHuIsEk9fJ5Sb-QLc5Tu51HPWyNIhvCyGoZq1DutA0J9QNt42Lp7DSYKg4l8TU7xt-d0t3DtfZGoMWx9a9FLhRUWGJSIkCaIAiV1FmGMlN5DqrmkAJUdapTnaV1KUpZlEWdiarMVJImXlTiMJHNC0nCYbHXXvZ5BsbAn6ALG3XPM9NK2Ca6xFn4lHUkQPb-_X4w0r9JfB-IYUUOM9rJTCeyYcmKmB6boLjutTK43g9OzXIa1z8t9Uoi4ZDTfMCxoL2A466xrWQHnqv4l672Xn3s5iZMSVvaOdtQ5ei1r8RJN244fYxLzivCYGHr0WH0-JZ9Q2dwh84_Jn-Sg9Z2bN205cAzCoxysQXgLE3i_UX3Ct06pK27RBawAaJHs_4zSw8NLmpM4EIRmIsF8pOeogpdMOULZXS83qF19IVDJC8BZr7-9cPvV5F-bhMFhy6hfZMPNj9xH5Re6HYTo56oB6KdoUdDLxPgQCWaW5cP98zBWrqw9u3Vu22jf48iYj1fLKm431L22f-rLDzwIZeNhZ1mbC7wnSuJtqXK22oM0te-_7Gy8_k3iCI0WQ:1w6Gyv:U2SfgKIteJun1QH3B7Ar8vrTvOZrP_GBRnpBYsgxLhI','2026-04-10 23:52:49.220616');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_order`
--

DROP TABLE IF EXISTS `orders_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `address` varchar(255) NOT NULL,
  `note` longtext,
  `total_price` decimal(12,0) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_order_user_id_e9b59eb1_fk_users_user_id` (`user_id`),
  CONSTRAINT `orders_order_user_id_e9b59eb1_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_order`
--

LOCK TABLES `orders_order` WRITE;
/*!40000 ALTER TABLE `orders_order` DISABLE KEYS */;
INSERT INTO `orders_order` VALUES (1,'','','',NULL,42000,'completed','2026-01-25 23:28:11.947474',1),(2,'','','',NULL,70000,'completed','2026-01-25 23:28:16.909035',1),(3,'','','',NULL,70000,'completed','2026-01-25 23:28:28.913500',1),(4,'','','',NULL,50000,'completed','2026-01-25 23:35:40.038671',1),(5,'','','',NULL,50000,'completed','2026-01-25 23:35:42.639366',1),(6,'','','',NULL,50000,'completed','2026-01-25 23:36:57.434041',1),(7,'','','',NULL,50000,'completed','2026-01-25 23:37:28.161053',1),(8,'','','',NULL,42000,'completed','2026-01-25 23:37:50.142371',1),(9,'','','',NULL,42000,'cancelled','2026-01-25 23:37:55.347003',1),(10,'','','',NULL,50000,'cancelled','2026-01-26 00:36:39.744911',1),(11,'','','',NULL,50000,'cancelled','2026-01-26 00:36:44.742503',1),(12,'','','',NULL,70000,'cancelled','2026-01-26 00:36:57.795766',1),(13,'','','',NULL,70000,'cancelled','2026-01-26 00:36:59.371597',1),(14,'','','',NULL,42000,'cancelled','2026-01-26 00:42:03.706430',1),(15,'','','',NULL,42000,'cancelled','2026-01-26 07:35:52.186081',4),(16,'','','',NULL,42000,'cancelled','2026-01-26 07:36:22.478928',4),(17,'','','',NULL,70000,'cancelled','2026-01-26 07:36:53.497478',4),(18,'','','',NULL,42000,'cancelled','2026-01-26 07:58:03.726667',4),(19,'','','',NULL,42000,'completed','2026-01-26 08:19:38.718707',4),(20,'','','',NULL,180000,'completed','2026-01-26 18:58:50.527771',1),(21,'','','',NULL,25000,'cancelled','2026-01-26 19:00:21.389910',1),(22,'','','',NULL,25000,'completed','2026-01-26 19:00:31.240834',1),(23,'','','',NULL,45000,'cancelled','2026-01-26 19:05:52.775759',1),(24,'','','',NULL,45000,'completed','2026-01-26 19:06:34.292805',1),(25,'','','',NULL,45000,'cancelled','2026-01-26 19:11:03.377107',1),(26,'','','',NULL,180000,'cancelled','2026-01-26 19:14:27.826904',1),(27,'','','',NULL,45000,'cancelled','2026-01-26 19:16:12.366060',1),(28,'','','',NULL,125000,'cancelled','2026-01-26 19:20:08.836104',1),(29,'','','',NULL,180000,'completed','2026-01-26 19:20:35.563484',1),(30,'','','',NULL,900000,'shipping','2026-01-26 19:24:06.011810',1),(31,'','','',NULL,180000,'shipping','2026-01-26 19:24:11.041669',1),(32,'','','',NULL,45000,'cancelled','2026-01-26 20:21:32.543641',1),(33,'','','',NULL,315000,'pending','2026-01-27 21:17:08.236560',1),(34,'','','',NULL,315000,'completed','2026-01-28 15:46:15.805438',10),(35,'','','',NULL,180000,'pending','2026-03-13 22:42:01.262780',1),(36,'','','',NULL,180000,'pending','2026-03-13 22:42:03.213188',1),(37,'','','',NULL,720000,'shipping','2026-03-15 07:49:19.466167',1),(38,'','','',NULL,180000,'new','2026-03-15 08:28:19.015071',1),(39,'','','',NULL,180000,'completed','2026-03-15 08:35:17.430123',1),(40,'testadmin','Chưa cập nhật','Chưa cập nhật','Đơn mua ngay',45000,'pending','2026-03-23 18:00:56.062233',14),(41,'admin','Chưa cập nhật','Chưa cập nhật',NULL,10000,'pending','2026-03-24 18:41:45.077478',1),(42,'admin','Chưa cập nhật','Chưa cập nhật',NULL,25000,'pending','2026-03-24 18:42:40.584184',1),(43,'admin','Chưa cập nhật','Chưa cập nhật',NULL,25000,'pending','2026-03-24 18:45:26.762449',1),(44,'admin','Chưa cập nhật','Chưa cập nhật',NULL,25000,'pending','2026-03-24 18:52:03.737731',1),(45,'admin','Chưa cập nhật','Chưa cập nhật',NULL,180000,'completed','2026-03-24 18:52:27.267277',1),(46,'admin','Chưa cập nhật','Chưa cập nhật',NULL,10000,'completed','2026-03-24 18:53:56.604779',1),(47,'admin','Chưa cập nhật','Chưa cập nhật',NULL,180000,'new','2026-03-27 17:08:26.821238',1),(48,'admin','Chưa cập nhật','Chưa cập nhật',NULL,45000,'completed','2026-03-27 22:43:47.525984',1);
/*!40000 ALTER TABLE `orders_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_orderitem`
--

DROP TABLE IF EXISTS `orders_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `price` decimal(12,0) NOT NULL,
  `quantity` int unsigned NOT NULL,
  `order_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` (`order_id`),
  KEY `orders_orderitem_product_id_afe4254a_fk_products_product_id` (`product_id`),
  CONSTRAINT `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`),
  CONSTRAINT `orders_orderitem_product_id_afe4254a_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  CONSTRAINT `orders_orderitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_orderitem`
--

LOCK TABLES `orders_orderitem` WRITE;
/*!40000 ALTER TABLE `orders_orderitem` DISABLE KEYS */;
INSERT INTO `orders_orderitem` VALUES (7,180000,1,20,5),(10,45000,1,23,4),(11,45000,1,24,4),(12,45000,1,25,4),(13,180000,1,26,5),(14,45000,1,27,4),(16,45000,4,29,4),(17,180000,5,30,5),(18,180000,1,31,5),(19,45000,1,32,4),(20,45000,7,33,4),(21,45000,7,34,4),(22,180000,1,35,5),(23,180000,1,36,5),(24,180000,4,37,5),(25,180000,1,38,5),(26,180000,1,39,5),(27,45000,1,40,4),(28,10000,1,41,10),(29,25000,1,42,8),(30,25000,1,43,8),(31,25000,1,44,8),(32,180000,1,45,5),(33,10000,1,46,10),(34,180000,1,47,5),(35,45000,1,48,4);
/*!40000 ALTER TABLE `orders_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_category`
--

DROP TABLE IF EXISTS `products_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `slug` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_category`
--

LOCK TABLES `products_category` WRITE;
/*!40000 ALTER TABLE `products_category` DISABLE KEYS */;
INSERT INTO `products_category` VALUES (2,'Đèn lồng','den-long'),(3,'Bao lì xì','bao-li-xi'),(4,'Hoa mai/đào giả','hoa-mai-dao-gia');
/*!40000 ALTER TABLE `products_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_product`
--

DROP TABLE IF EXISTS `products_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `description` longtext NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `stock` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `products_product_category_id_9b594869_fk_products_category_id` (`category_id`),
  CONSTRAINT `products_product_category_id_9b594869_fk_products_category_id` FOREIGN KEY (`category_id`) REFERENCES `products_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_product`
--

LOCK TABLES `products_product` WRITE;
/*!40000 ALTER TABLE `products_product` DISABLE KEYS */;
INSERT INTO `products_product` VALUES (4,'Đèn lồng đỏ 30cm','den-long-do-30cm','products/vn-11134207-7ras8-m30xkgnhc1q27d.webp','Điểm nổi bật không thể bỏ qua! ?\r\n\r\nCombo lồng đèn giấy trang trí Tết mang đến vẻ đẹp truyền thống, họa tiết sinh động và chất liệu giấy bền đẹp. Sản phẩm phù hợp cho mọi không gian: từ cửa hàng, quán cà phê đến nhà ở, giúp không gian thêm rực rỡ và tràn ngập không khí Tết.\r\n\r\n\r\n\r\nNhiều lựa chọn đa dạng ?\r\n\r\n- Kích thước: 11cm, 15cm, 20cm, 25cm, 30cm, 35cm\r\n\r\n- Số lượng: 30, 50, 100 cái\r\n\r\n- Họa tiết: Phúc, Lộc, Thọ, Tài, Phát\r\n\r\n- Có thể kết hợp nhiều mẫu trong một combo\r\n\r\n\r\n\r\nThông tin hữu ích khác ?\r\n\r\n- Lồng đèn dễ dàng tự lắp ráp, sử dụng đèn LED hoặc nến an toàn\r\n\r\n- Phù hợp để trang trí, làm quà tặng hoặc chụp ảnh dịp Tết\r\n\r\n- Sản phẩm có sẵn nhiều lựa chọn về số lượng và kích thước, đáp ứng nhu cầu sử dụng khác nhau\r\n\r\n\r\n\r\nHãy lựa chọn combo lồng đèn giấy trang trí Tết để không gian của bạn thêm phần ấm cúng và tràn đầy sức sống trong dịp đầu năm mới!',45000,119,1,'2026-01-26 10:19:27.841530',2),(5,'Cành đào giả 1m2','canh-dao-gia-1m2','products/vn-11134207-7r98o-lq7cgn0ke11u8a.webp','cành Hoa Đào cổ trang trí nhà cửa, sự kiện, studio, mang không gian tết cổ truyền, \r\n\r\nCành loại thân gỗ to sần đẹp cắm bình siêu sang\r\n\r\nloại dài cành cao 1m2 , hàng loại 1 nhiều hoa thân sần siêu đẹp\r\n\r\ngiá trên là giá 1 cành',180000,33,1,'2026-01-26 10:21:08.026799',4),(8,'Set bao lì xì 2026 (20 cái)','set-bao-li-xi-2026-20-cai','products/vn-11134207-820l4-mg7rn7y2134c00.webp','Bao Lì Xì Combo 20 Cái',25000,197,1,'2026-01-27 21:40:56.823373',3),(10,'Hoa Hồng','hoa-hong','products/Screenshot_2026-01-23_002154.png','Hoa hồng rất đẹp',10000,248,1,'2026-01-28 20:01:33.589254',4);
/*!40000 ALTER TABLE `products_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user`
--

DROP TABLE IF EXISTS `users_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `address` longtext,
  `avatar` varchar(100) DEFAULT NULL,
  `is_customer` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
INSERT INTO `users_user` VALUES (1,'pbkdf2_sha256$1200000$2GRY4ggClHSAfhYKyNhLPE$oBzhnuYm4D/esG02RxdTNN7SzAs+Q72x4cQmV8FXd88=','2026-03-18 08:28:41.717440',1,'admin','','','',1,1,'2026-01-22 17:50:15.028649',NULL,NULL,'',1),(2,'pbkdf2_sha256$1200000$yakmJyxdvTxVSaLTkNU3IC$KKZMsGmR4clBuLaNro4Gp6CofKwRMdRywhVS6Dxcx44=',NULL,0,'lehongson','Sơn','Lê','lehongson270920050@gmail.com',0,1,'2026-01-22 17:57:15.000000','0348063722','Thai Nguyen City','avatars/Screenshot_2026-01-19_150740.png',1),(3,'pbkdf2_sha256$1200000$egFUp558B4ttT8iLjE5S6F$WQkp/q9VSWRB8yrf64887F0IBzeyOB3oa6D2mydKndQ=','2026-01-25 19:50:12.336544',0,'user','Son','Le','lehongson270920050@gmail.com',0,1,'2026-01-25 19:21:29.000000','0348063722','Thai Nguyen','avatars/Screenshot_2026-01-23_002154.png',1),(4,'pbkdf2_sha256$1200000$NEmcEEhPRWHchyraNvUhDx$kmvpPopl8EJ558gJIjk2Cfyei5So7E2gLowXVjRLbtA=','2026-03-03 03:07:48.677622',0,'user1','','','lehongson270920050@gmail.com',0,1,'2026-01-25 20:33:09.810537',NULL,NULL,'',1),(5,'pbkdf2_sha256$1200000$3bCNyzooZEwBYLBKirLXnc$noW8PrRZ1bhccJcPqaxGJRIcp2pU/iyVS/1V4JikvHY=','2026-01-26 19:24:29.245535',0,'user3','','','lehongson270920050@gmail.com',0,1,'2026-01-26 08:17:57.877075',NULL,NULL,'',1),(6,'pbkdf2_sha256$1200000$CdFjon1HCIYYs2O5QAiH0K$kwfqConItrEcKNycg7LC1NZ7oLF3K63HxlDosSogkyI=','2026-01-28 08:57:06.408471',0,'sinhngothi','','','sinh79579@gmail.com',0,1,'2026-01-28 08:57:05.496663',NULL,NULL,'',1),(8,'pbkdf2_sha256$1200000$uXbz9kAWYSfQVk0uYEy8Zs$GI1jxJOXdqTm6kTa9/ek1GKHpteFvd2KtuGw5nf3OlU=','2026-01-28 09:06:10.996750',0,'TestĐăngKíTesi','','','TestDangKi@gmail.com',0,1,'2026-01-28 09:06:10.032354',NULL,NULL,'',1),(9,'pbkdf2_sha256$1200000$W5Dv9hZSszbfXRv1dbKLqX$k85G5S5jXUD7iJk7zqe+hsA0I8k3mAqTPJsmmBJtR78=','2026-01-28 09:22:12.789033',0,'songhgoj','','','djhdhj@gmail.com',0,1,'2026-01-28 09:22:11.836930',NULL,NULL,'',1),(10,'pbkdf2_sha256$1200000$ikTlHpvd9qjMk3arQJ2YCa$H6io+xjudjbNAPKbl3Co1LDQiUjiK81BfDucsT5ZKj8=','2026-01-28 15:45:38.198573',0,'TestDemo','','','TestDemo@gmail.com',0,1,'2026-01-28 15:45:37.163292',NULL,NULL,'',1),(11,'pbkdf2_sha256$1200000$YPWQTgV3wP0JdWm96BDiSs$PRShEzb2isvcCNfr/LZOnROSRewp5of2W88obXmOha4=','2026-01-28 18:51:02.654358',0,'TestBaoCao','','','TestBaoCao@gmai.com',0,1,'2026-01-28 18:15:29.336000',NULL,NULL,'',1),(12,'pbkdf2_sha256$1200000$S0zfaprQK7lwELDdBYdnl2$qRJ27xA7u5ExaJUQHNKC68hevT561lDi3GSHTDgflz4=','2026-01-28 18:54:45.683458',0,'TestThuNghiem','','','TestThuNghiem@gmail.com',0,1,'2026-01-28 18:54:44.723888',NULL,NULL,'',1),(13,'pbkdf2_sha256$1200000$GkGCeEhGNQNEj49OzHIYKy$prknn3qEfIovcxFCAcuMzN772hGQd3n3FCuf8vCmbTw=','2026-01-28 18:58:06.951994',0,'TestChinhThuc','','','TestChinhThuc@gmail.com',0,1,'2026-01-28 18:55:37.782629',NULL,NULL,'',1),(14,'pbkdf2_sha256$1200000$ADtapmLYaYJC6R7x9AyZ2a$DrGQThoI+aEy4hVgHQjXtI+5e3E0EjR8OycYhF4TZg0=','2026-03-23 17:59:27.291697',1,'testadmin','','','test@test.com',1,1,'2026-03-23 17:58:24.070728',NULL,NULL,'',1);
/*!40000 ALTER TABLE `users_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_groups`
--

DROP TABLE IF EXISTS `users_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_groups_user_id_group_id_b88eab82_uniq` (`user_id`,`group_id`),
  KEY `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_user_groups_user_id_5f6f5a90_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_groups`
--

LOCK TABLES `users_user_groups` WRITE;
/*!40000 ALTER TABLE `users_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_user_permissions`
--

DROP TABLE IF EXISTS `users_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_user_permissions_user_id_permission_id_43338c45_uniq` (`user_id`,`permission_id`),
  KEY `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_user_permissions_user_id_20aca447_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_user_permissions`
--

LOCK TABLES `users_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-28 16:51:40
