/*
SQLyog Ultimate v11.11 (32 bit)
MySQL - 5.7.29-0ubuntu0.18.04.1 : Database - goteo
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

/*Table structure for table `banner` */

DROP TABLE IF EXISTS `banner`;

CREATE TABLE `banner` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `node` varchar(50) CHARACTER SET utf8 NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Contiene nombre de archivo',
  `active` int(1) NOT NULL DEFAULT '0',
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `url` tinytext CHARACTER SET utf8,
  PRIMARY KEY (`id`),
  KEY `banner_ibfk_1` (`node`),
  KEY `banner_ibfk_2` (`project`),
  CONSTRAINT `banner_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `banner_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Proyectos en banner superior';

/*Data for the table `banner` */

/*Table structure for table `banner_lang` */

DROP TABLE IF EXISTS `banner_lang`;

CREATE TABLE `banner_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `url` tinytext COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `banner_lang` */

/*Table structure for table `bazar_lang` */

DROP TABLE IF EXISTS `bazar_lang`;

CREATE TABLE `bazar_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `title` tinytext,
  `description` text,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `bazar_lang` */

/*Table structure for table `blog` */

DROP TABLE IF EXISTS `blog`;

CREATE TABLE `blog` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(10) CHARACTER SET utf8 NOT NULL,
  `owner` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT 'la id del proyecto o nodo',
  `active` tinyint(1) NOT NULL DEFAULT '1',
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Blogs de nodo o proyecto';

/*Data for the table `blog` */

insert  into `blog`(`id`,`type`,`owner`,`active`) values (1,'node','goteo',1);

/*Table structure for table `call` */

DROP TABLE IF EXISTS `call`;

CREATE TABLE `call` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `subtitle` text COLLATE utf8mb4_unicode_ci,
  `lang` varchar(2) CHARACTER SET utf8 NOT NULL DEFAULT 'es',
  `status` int(1) NOT NULL,
  `translate` int(1) NOT NULL DEFAULT '0',
  `owner` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT 'entidad que convoca',
  `amount` int(6) NOT NULL COMMENT 'presupuesto',
  `created` date DEFAULT NULL,
  `updated` date DEFAULT NULL,
  `opened` date DEFAULT NULL,
  `published` date DEFAULT NULL,
  `success` date DEFAULT NULL,
  `closed` date DEFAULT NULL,
  `contract_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contract_nif` varchar(10) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Guardar sin espacios ni puntos ni guiones',
  `phone` varchar(20) CHARACTER SET utf8 DEFAULT NULL COMMENT 'guardar sin espacios ni puntos',
  `contract_email` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `address` tinytext COLLATE utf8mb4_unicode_ci,
  `zipcode` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `location` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `country` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `logo` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Logo. Contiene nombre de archivo',
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Imagen widget. Contiene nombre de archivo',
  `backimage` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Imagen background. Contiene nombre de archivo',
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `description_summary` text COLLATE utf8mb4_unicode_ci,
  `description_nav` text COLLATE utf8mb4_unicode_ci,
  `whom` text COLLATE utf8mb4_unicode_ci,
  `apply` text COLLATE utf8mb4_unicode_ci,
  `legal` longtext COLLATE utf8mb4_unicode_ci,
  `dossier` tinytext COLLATE utf8mb4_unicode_ci,
  `tweet` tinytext COLLATE utf8mb4_unicode_ci,
  `fbappid` tinytext COLLATE utf8mb4_unicode_ci,
  `call_location` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `resources` text COLLATE utf8mb4_unicode_ci,
  `scope` int(1) NOT NULL,
  `contract_entity` int(1) NOT NULL DEFAULT '0',
  `contract_birthdate` date DEFAULT NULL,
  `entity_office` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `entity_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `entity_cif` varchar(10) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Guardar sin espacios ni puntos ni guiones',
  `post_address` tinytext COLLATE utf8mb4_unicode_ci,
  `secondary_address` int(11) NOT NULL DEFAULT '0',
  `post_zipcode` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `post_location` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `post_country` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `days` int(2) DEFAULT NULL,
  `maxdrop` int(6) DEFAULT NULL COMMENT 'Riego maximo por aporte',
  `modemaxp` varchar(3) CHARACTER SET utf8 DEFAULT 'imp' COMMENT 'Modalidad del máximo por proyecto: imp = importe, per = porcentaje',
  `maxproj` int(6) NOT NULL COMMENT 'Riego maximo por proyecto',
  `num_projects` int(10) unsigned NOT NULL COMMENT 'Número de proyectos publicados',
  `rest` int(10) unsigned NOT NULL COMMENT 'Importe riego disponible',
  `used` int(10) unsigned NOT NULL COMMENT 'Importe riego comprometido',
  `applied` int(10) unsigned NOT NULL COMMENT 'Número de proyectos aplicados',
  `running_projects` int(10) unsigned NOT NULL COMMENT 'Número de proyectos en campaña',
  `success_projects` int(10) unsigned NOT NULL COMMENT 'Número de proyectos exitosos',
  `fee_projects_drop` int(2) NOT NULL DEFAULT '4' COMMENT 'Fee to apply in the financial report to the drop',
  `facebook_pixel` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `intro_checks` text COLLATE utf8mb4_unicode_ci COMMENT 'Intro checks in apply page',
  PRIMARY KEY (`id`),
  KEY `owner` (`owner`),
  CONSTRAINT `call_ibfk_1` FOREIGN KEY (`owner`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Convocatorias';

/*Data for the table `call` */

insert  into `call`(`id`,`name`,`subtitle`,`lang`,`status`,`translate`,`owner`,`amount`,`created`,`updated`,`opened`,`published`,`success`,`closed`,`contract_name`,`contract_nif`,`phone`,`contract_email`,`address`,`zipcode`,`location`,`country`,`logo`,`image`,`backimage`,`description`,`description_summary`,`description_nav`,`whom`,`apply`,`legal`,`dossier`,`tweet`,`fbappid`,`call_location`,`resources`,`scope`,`contract_entity`,`contract_birthdate`,`entity_office`,`entity_name`,`entity_cif`,`post_address`,`secondary_address`,`post_zipcode`,`post_location`,`post_country`,`days`,`maxdrop`,`modemaxp`,`maxproj`,`num_projects`,`rest`,`used`,`applied`,`running_projects`,`success_projects`,`fee_projects_drop`,`facebook_pixel`,`intro_checks`) values ('test-call','Test call','Description test call','es',3,0,'owner-project-passing',1000,'2020-02-19','2020-02-19','2020-02-19','2020-02-19',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,'imp',10,1,0,0,0,1,0,4,NULL,NULL),('test-call-2','Test call','Description test call','es',3,0,'owner-project-passing',1000,'2019-12-31','2019-12-31','2019-12-31','2019-12-31',NULL,'2020-03-10',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,'imp',10,1,0,0,0,1,0,4,NULL,NULL);

/*Table structure for table `call_banner` */

DROP TABLE IF EXISTS `call_banner`;

CREATE TABLE `call_banner` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `call` varchar(50) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `url` tinytext CHARACTER SET utf8,
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Contiene nombre de archivo',
  `order` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `call` (`call`),
  CONSTRAINT `call_banner_ibfk_1` FOREIGN KEY (`call`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Banners de convocatorias';

/*Data for the table `call_banner` */

/*Table structure for table `call_banner_lang` */

DROP TABLE IF EXISTS `call_banner_lang`;

CREATE TABLE `call_banner_lang` (
  `id` int(11) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  PRIMARY KEY (`id`,`lang`),
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `call_banner_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `call_banner` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `call_banner_lang` */

/*Table structure for table `call_category` */

DROP TABLE IF EXISTS `call_category`;

CREATE TABLE `call_category` (
  `call` varchar(50) CHARACTER SET utf8 NOT NULL,
  `category` int(10) unsigned NOT NULL,
  UNIQUE KEY `call_category` (`call`,`category`),
  KEY `category` (`category`),
  CONSTRAINT `call_category_ibfk_2` FOREIGN KEY (`category`) REFERENCES `category` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Categorias de las convocatorias';

/*Data for the table `call_category` */

/*Table structure for table `call_check` */

DROP TABLE IF EXISTS `call_check`;

CREATE TABLE `call_check` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `call` varchar(50) NOT NULL,
  `lang` varchar(2) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  KEY `call` (`call`),
  CONSTRAINT `call` FOREIGN KEY (`call`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Call check';

/*Data for the table `call_check` */

/*Table structure for table `call_check_lang` */

DROP TABLE IF EXISTS `call_check_lang`;

CREATE TABLE `call_check_lang` (
  `id` int(10) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `description` text NOT NULL,
  `pending` int(1) DEFAULT '0' COMMENT 'To be reviewed',
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `call_check_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `call_check` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `call_check_lang` */

/*Table structure for table `call_check_project` */

DROP TABLE IF EXISTS `call_check_project`;

CREATE TABLE `call_check_project` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `call_check` int(10) unsigned NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `response` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `call_check` (`call_check`),
  KEY `project` (`project`),
  CONSTRAINT `call_check` FOREIGN KEY (`call_check`) REFERENCES `call_check` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `call_check_project` */

/*Table structure for table `call_conf` */

DROP TABLE IF EXISTS `call_conf`;

CREATE TABLE `call_conf` (
  `call` varchar(50) CHARACTER SET utf8 NOT NULL,
  `applied` int(4) DEFAULT NULL COMMENT 'Para fijar numero de proyectos recibidos',
  `max_projects` int(4) NOT NULL COMMENT 'Max projects to campaign',
  `limit1` set('normal','minimum','unlimited','none') CHARACTER SET utf8 NOT NULL DEFAULT 'normal' COMMENT 'tipo limite riego primera ronda',
  `limit2` set('normal','minimum','unlimited','none','fullunlimited') CHARACTER SET utf8 NOT NULL DEFAULT 'none' COMMENT 'tipo limite riego segunda ronda',
  `unique_user_drop` int(1) DEFAULT '1' COMMENT 'Only drops once for user',
  `match_factor` int(2) unsigned NOT NULL DEFAULT '2',
  `buzz_first` int(1) NOT NULL DEFAULT '0' COMMENT 'Solo primer hashtag en el buzz',
  `buzz_own` int(1) NOT NULL DEFAULT '1' COMMENT 'Tweets  propios en el buzz',
  `buzz_mention` int(1) NOT NULL DEFAULT '1' COMMENT 'Menciones en el buzz',
  `map_stage1` varchar(256) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Map iframe for stage 1',
  `map_stage2` varchar(256) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Map iframe for stage 2',
  `date_stage1` date DEFAULT NULL COMMENT 'Stage 1 date',
  `date_stage1_out` date DEFAULT NULL COMMENT 'Stage 1 date out',
  `date_stage2` date DEFAULT NULL COMMENT 'Stage 2 date',
  `date_stage3` date DEFAULT NULL COMMENT 'Stage 3 date',
  PRIMARY KEY (`call`),
  CONSTRAINT `call_conf_ibfk_1` FOREIGN KEY (`call`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Configuración de convocatoria';

/*Data for the table `call_conf` */

/*Table structure for table `call_icon` */

DROP TABLE IF EXISTS `call_icon`;

CREATE TABLE `call_icon` (
  `call` varchar(50) CHARACTER SET utf8 NOT NULL,
  `icon` varchar(50) CHARACTER SET utf8 NOT NULL,
  UNIQUE KEY `call_icon` (`call`,`icon`),
  KEY `icon` (`icon`),
  CONSTRAINT `call_icon_ibfk_1` FOREIGN KEY (`call`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `call_icon_ibfk_2` FOREIGN KEY (`icon`) REFERENCES `icon` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tipos de retorno de las convocatorias';

/*Data for the table `call_icon` */

/*Table structure for table `call_lang` */

DROP TABLE IF EXISTS `call_lang`;

CREATE TABLE `call_lang` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `description_summary` text COLLATE utf8mb4_unicode_ci,
  `description_nav` text COLLATE utf8mb4_unicode_ci,
  `whom` text COLLATE utf8mb4_unicode_ci,
  `apply` text COLLATE utf8mb4_unicode_ci,
  `legal` longtext COLLATE utf8mb4_unicode_ci,
  `subtitle` text COLLATE utf8mb4_unicode_ci,
  `dossier` tinytext COLLATE utf8mb4_unicode_ci,
  `tweet` tinytext COLLATE utf8mb4_unicode_ci,
  `resources` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `call_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `call_lang` */

/*Table structure for table `call_location` */

DROP TABLE IF EXISTS `call_location`;

CREATE TABLE `call_location` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `latitude` decimal(16,14) NOT NULL,
  `longitude` decimal(16,14) NOT NULL,
  `radius` smallint(6) unsigned NOT NULL DEFAULT '0',
  `method` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT 'ip',
  `locable` tinyint(1) NOT NULL DEFAULT '0',
  `city` varchar(255) CHARACTER SET utf8 NOT NULL,
  `region` varchar(255) CHARACTER SET utf8 NOT NULL,
  `country` varchar(150) CHARACTER SET utf8 NOT NULL,
  `country_code` varchar(2) CHARACTER SET utf8 NOT NULL,
  `info` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  CONSTRAINT `call_location_ibfk_1` FOREIGN KEY (`id`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `call_location` */

insert  into `call_location`(`id`,`latitude`,`longitude`,`radius`,`method`,`locable`,`city`,`region`,`country`,`country_code`,`info`,`modified`) values ('test-call',42.90000000000000,-2.60000000000000,0,'manual',1,'Bilbo','Euskadi','Spain','ES',NULL,'2020-04-09 16:50:26'),('test-call-2',42.91000000000000,-2.61000000000000,0,'manual',1,'Bilbo','Euskadi','Spain','ES',NULL,'2020-04-09 16:50:26');

/*Table structure for table `call_post` */

DROP TABLE IF EXISTS `call_post`;

CREATE TABLE `call_post` (
  `call` varchar(50) CHARACTER SET utf8 NOT NULL,
  `post` bigint(20) unsigned NOT NULL,
  UNIQUE KEY `call_post` (`call`,`post`),
  KEY `post` (`post`),
  CONSTRAINT `call_post_ibfk_1` FOREIGN KEY (`call`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `call_post_ibfk_2` FOREIGN KEY (`post`) REFERENCES `post` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Entradas de blog asignadas a convocatorias';

/*Data for the table `call_post` */

/*Table structure for table `call_project` */

DROP TABLE IF EXISTS `call_project`;

CREATE TABLE `call_project` (
  `call` varchar(50) CHARACTER SET utf8 NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  UNIQUE KEY `call_project` (`call`,`project`),
  KEY `call_project_ibfk_2` (`project`),
  CONSTRAINT `call_project_ibfk_1` FOREIGN KEY (`call`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `call_project_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Proyectos asignados a convocatorias';

/*Data for the table `call_project` */

insert  into `call_project`(`call`,`project`) values ('test-call','project-passing-today');

/*Table structure for table `call_sphere` */

DROP TABLE IF EXISTS `call_sphere`;

CREATE TABLE `call_sphere` (
  `call_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `sphere_id` bigint(20) unsigned NOT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`call_id`,`sphere_id`),
  KEY `sphere_id` (`sphere_id`),
  CONSTRAINT `call_sphere_ibfk_1` FOREIGN KEY (`call_id`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `call_sphere_ibfk_2` FOREIGN KEY (`sphere_id`) REFERENCES `sphere` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Ámbito de convocatorias';

/*Data for the table `call_sphere` */

/*Table structure for table `call_sponsor` */

DROP TABLE IF EXISTS `call_sponsor`;

CREATE TABLE `call_sponsor` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `call` varchar(50) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `url` tinytext CHARACTER SET utf8,
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Contiene nombre de archivo',
  `order` int(11) NOT NULL DEFAULT '1',
  `amount` int(11) DEFAULT NULL,
  `main` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'Sponsor main',
  `order_landing_match` smallint(5) unsigned NOT NULL DEFAULT '1',
  `landing_match` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `call` (`call`),
  CONSTRAINT `call_sponsor_ibfk_1` FOREIGN KEY (`call`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Patrocinadores de convocatorias';

/*Data for the table `call_sponsor` */

/*Table structure for table `campaign` */

DROP TABLE IF EXISTS `campaign`;

CREATE TABLE `campaign` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `node` varchar(50) CHARACTER SET utf8 NOT NULL,
  `call` varchar(50) CHARACTER SET utf8 NOT NULL,
  `active` int(1) NOT NULL DEFAULT '0',
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `call_node` (`node`,`call`),
  KEY `call` (`call`),
  CONSTRAINT `campaign_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `campaign_ibfk_2` FOREIGN KEY (`call`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Convocatorias en portada';

/*Data for the table `campaign` */

/*Table structure for table `category` */

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `order` tinyint(3) unsigned NOT NULL DEFAULT '1',
  `social_commitment` int(10) unsigned DEFAULT NULL COMMENT 'Social commitment',
  PRIMARY KEY (`id`),
  KEY `social_commitment` (`social_commitment`),
  CONSTRAINT `category_ibfk_1` FOREIGN KEY (`social_commitment`) REFERENCES `social_commitment` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `category_ibfk_2` FOREIGN KEY (`social_commitment`) REFERENCES `social_commitment` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `category_ibfk_3` FOREIGN KEY (`social_commitment`) REFERENCES `social_commitment` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `category_ibfk_4` FOREIGN KEY (`social_commitment`) REFERENCES `social_commitment` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `category_ibfk_5` FOREIGN KEY (`social_commitment`) REFERENCES `social_commitment` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `category_ibfk_6` FOREIGN KEY (`social_commitment`) REFERENCES `social_commitment` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Categorias de los proyectos';

/*Data for the table `category` */

insert  into `category`(`id`,`name`,`description`,`order`,`social_commitment`) values (2,'Social','Proyectos que promueven el cambio social, la resolución de problemas en las relaciones humanas y/o su fortalecimiento para conseguir un mayor bienestar.',1,NULL),(6,'Comunicativo','Proyectos con el objetivo de informar, denunciar, comunicar (por ejemplo periodismo ciudadano, documentales, blogs, programas de radio).',3,NULL),(7,'Tecnológico','Desarrollos técnicos de software, hardware, herramientas etc. para solucionar problemas o necesidades concretas. ',1,NULL),(9,'Emprendedor','Proyectos que aspiran a convertirse en una iniciativa empresarial o de emprendimiento social, generando beneficios económicos. ',1,NULL),(10,'Educativo','Proyectos donde el objetivo primordial es la formación o el aprendizaje. ',5,NULL),(11,'Cultural','Proyectos con objetivos artísticos y culturales en un sentido amplio.',6,NULL),(13,'Ecológico','Proyectos relacionados con el cuidado del medio ambiente, la sostenibilidad y/o la diversidad biológica.\r\n',7,NULL),(14,'Científico','Estudios o investigaciones de alguna materia, proyectos que buscan respuestas, soluciones, explicaciones nuevas.',8,NULL),(15,'','Usuarios para pruebas en entorno real',1,NULL),(16,'Diseño','',1,NULL);

/*Table structure for table `category_footprint` */

DROP TABLE IF EXISTS `category_footprint`;

CREATE TABLE `category_footprint` (
  `footprint_id` int(10) unsigned NOT NULL,
  `category_id` int(10) unsigned NOT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`footprint_id`,`category_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `category_footprint_ibfk_1` FOREIGN KEY (`footprint_id`) REFERENCES `footprint` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `category_footprint_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `category_footprint` */

/*Table structure for table `category_lang` */

DROP TABLE IF EXISTS `category_lang`;

CREATE TABLE `category_lang` (
  `id` int(10) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  PRIMARY KEY (`id`,`lang`),
  KEY `lang` (`lang`),
  CONSTRAINT `category_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `category` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `category_lang` */

insert  into `category_lang`(`id`,`lang`,`name`,`description`,`pending`) values (2,'ca','Social','Projectes que promouen el canvi social, la resolució de problemes en les relacions humanes i/o el seu enfortiment per aconseguir un major benestar.',0),(2,'de','Gesellschaft','Projekte, die den sozialen Austausch sowie die Problemlösung in zwischenmenschlichen Beziehungen fördern und die eine Stärkung gesellschaftlicher Bindungen zur Förderung des Allgemeinwohls unterstützen.',0),(2,'el','Social','Projects that promote social change, resolve problems with or strengthen human relationshiops in order to achieve better well-being.',0),(2,'en','Social','Projects that promote social change, resolve problems with or strengthen human relationshiops in order to achieve better well-being.',0),(2,'eu','Soziala','Gizarte eraldaketa bultzatzen dituzten proiektuak, ongizate handiagoa lortzeko, giza harremanetan ematen diren arazoak ebatzi edo/eta  giza harremanak indartuz.\r\n',0),(2,'fr','Social','Des projets qui favorisent le changement social, la résolution de problèmes dans les relations humaines et/ou leur renforcement afin d\'atteindre un plus grand bien-être. ',0),(2,'gl','Social','Proxectos que promoven o cambio social, a resolución de problemas nas relacións humanas e/ou o seu fortalecemento para acadar un maior benestar.',0),(2,'it','Sociale','Progetti che promuovono il cambiamento sociale, la soluzione di problemi nel campo delle relazioni umane e/o il loro rafforzamento per incrementare il benessere collettivo. ',0),(2,'pl','Social','Projects that promote social change, resolve problems with or strengthen human relationshiops in order to achieve better well-being.',0),(6,'ca','Comunicatiu','Projectes amb l\'objectiu d\'informar, denunciar, comunicar (per exemple periodisme ciutadà, documentals, blogs, programes de ràdio).',0),(6,'de','Kommunikation','Projekte, deren Ziel es ist zu informieren, Misstände öffentlich zu machen oder die sich um Kommunikation im Allgemeinen drehen (z.B. Bürgerzeitungen, Dokumentarfilme, Blogs, Radioprogramme).',0),(6,'el','Communications','Projects whose objective is to inform, denounce and/or communicate (for example, civic journalism, documentaries, blogs, radio programs).',0),(6,'en','Communications','Projects whose objective is to inform, denounce and/or communicate (for example, civic journalism, documentaries, blogs, radio programs).',0),(6,'eu','Komunikatiboa','Berri ematea, salaketa, komunikazio helburua duten proiektuak (adibidez herri kazetaritza, dokumentalak. blogak, irrati programak).',0),(6,'fr','Communicatif','Des projets qui ont pour but d\'informer, de dénoncer, de communiquer (par exemple, le journalisme citoyen, des documentaires, des blogs, des programmes de radio).',0),(6,'gl','Comunicativo','Proxectos cun obxectivo de informar, denunciar, comunicar (por exemplo periodismo cidadán, documentais, blogs, programas de radio).',0),(6,'it','Comunicativo','Progetti che hanno l\'obiettivo di informare, denunciare, comunicare (giornalismo di cittadinanza, documentari, blog, programmi radio). ',0),(6,'pl','Communications','Projects whose objective is to inform, denounce and/or communicate (for example, civic journalism, documentaries, blogs, radio programs).',0),(7,'ca','Tecnològic','Desenvolupaments tècnics de programari, maquinari, eines etc. per solucionar problemes o necessitats concretes. ',0),(7,'de','Technologie','Technische Entwicklungen im Bereich Software, Hardware, Werkzeuge etc. die der Problemlösung dienen oder die auf konkrete Bedürfnisse eingehen.\r\n',0),(7,'el','Technological','Technical development of software, hardware, tools, etc in order to solve concrete problems or needs.',0),(7,'en','Technological','Technical development of software, hardware, tools, etc in order to solve concrete problems or needs.',0),(7,'eu','Teknologikoa','Arazo edo behar konkretuak ebazteko garapen teknikoak, software, hardware, herramintak etar.',0),(7,'fr','Technologique','Développement de logiciels, des outils, de hardware, etc. afin de résoudre des problèmes ou des besoins spécifiques.\r\n',0),(7,'gl','Tecnolóxico','Desenrolos técnicos de software, hardware, ferramentas etc. para solucionar problemas ou necesidades concretas. ',0),(7,'it','Tecnologico','Sviluppo tecnico di software, hardware, strumenti, ecc. per la soluzione di problemi o necessità concrete. ',0),(7,'pl','Technological','Technical development of software, hardware, tools, etc in order to solve concrete problems or needs.',0),(9,'ca','Comercial','Projectes que aspiren a convertir-se en una iniciativa empresarial, generant beneficis econòmics. ',0),(9,'de','Kommerziell','Projekte, die eine unternehmerische Initiative darstellen und die die Absicht haben, ökonomischen Gewinn zu generieren.',0),(9,'el','Commercial','Projects that are business initiatives, and that hope to generate profits.',0),(9,'en','Commercial','Projects that are business initiatives, and that hope to generate profits.',0),(9,'eu','Komertziala','\r\nIrabazi ekonomikoak sortuz, enpresa-ekimenen bat bihurtzeko asmoa duten propiektuak.',0),(9,'fr','Commercial','Des projets visant à devenir des initiatives d\'affaires en génerant des bénéfices économiques.\r\n',0),(9,'gl','Comercial','Proxectos que aspiran a converterse nunha iniciativa empresarial, xerando beneficios económicos. ',0),(9,'it','Imprenditoriale ','Progetti che aspirano a convertirsi in un\'iniziativa di impresa o di impresa sociale che generi benefici economici. ',0),(9,'pl','Commercial','Projects that are business initiatives, and that hope to generate profits.',0),(10,'ca','Educatiu','Projectes on l\'objectiu primordial és la formació o l\'aprenentatge. ',0),(10,'de','Bildung','Projekte, deren primäres Ziel im Bereich Bildung und Lernen liegt.',0),(10,'el','Educational','Projects whose most important objective is formation or learning. ',0),(10,'en','Educational','Projects whose most important objective is formation or learning. ',0),(10,'eu','Hezigarria','Formakuntza edo ikaskuntza helburu nagusia duten proiektuak. ',0),(10,'fr','Éducatif','Des projets qui ont pour but principal la formation ou l\'apprentissage.',0),(10,'gl','Educativo','Proxectos onde o obxectivo primordial é a formación ou a aprendizaxe.',0),(10,'it','Educativo','Progetti che hanno come obiettivo principale la formazione o l\'apprendimento.',0),(10,'pl','Educational','Projects whose most important objective is formation or learning. ',0),(11,'ca','Cultural','Projectes amb objectius artístics i culturals en un sentit ampli.',0),(11,'de','Kultur','Projekte mit künstlerischen und kulturellen Zielsetzungen im weiteren Sinne.',0),(11,'el','Cultural','Projects with artistic or cultural objectives.',0),(11,'en','Cultural','Projects with artistic or cultural objectives.',0),(11,'eu','Kulturala','Zentzu zabalean helburu artistiko eta kulturalak dituzten proiektuak. ',0),(11,'fr','Culturel','Des projets ayant des objectifs artistiques et culturels au sens large.',0),(11,'gl','Cultural','Proxectos con obxectivos artísticos e culturais nun sentido amplo.',0),(11,'it','Culturale','Progetti con obiettivi artistici e culturale in un senso lato. ',0),(11,'pl','Cultural','Projects with artistic or cultural objectives.',0),(13,'ca','Ecològic','Projectes relacionats amb la cura del medi ambient, la sostenibilitat i/o la diversitat biològica.\r\n',0),(13,'de','Ökologie','Projekte im Bereich Umweltschutz, Nachhaltigkeit und Biodiversität.',0),(13,'el','Ecological','Projects that are related to the care of the environment, sustainability, and/or biological diversity.\r\n',0),(13,'en','Ecological','Projects that are related to the care of the environment, sustainability, and/or biological diversity.\r\n',0),(13,'eu','Ekologikoa','Ingurumenaren zainketa, jasangarritasun eta/edo aniztasun biologikoarekin harremanetan dauden proiektuak.',0),(13,'fr','Écologique','Des projets liés au soin environnemental, à la durabilité et / ou à la diversité biologique.',0),(13,'gl','Ecolóxico','Proxectos relacionados co coidado do medio ambiente, a sostenibilidade e/ou a diversidade biolóxica.\r\n',0),(13,'it','Ecologico','Progetti relazionati alla tutela dell\'ambiente, la sostenibilità e/o la biodiversità. \r\n',0),(13,'pl','Ecological','Projects that are related to the care of the environment, sustainability, and/or biological diversity.\r\n',0),(14,'ca','Científic','Estudis o investigacions d\'alguna matèria, projectes que busquen respostes, solucions, explicacions noves.',0),(14,'de','Wissenschaft','Studien und Untersuchungen jeglicher Art, Projekte auf der Suche nach Antworten, Lösungen, und neuen Erklärungen.',0),(14,'el','Scientific','Studies or research, projects that look for answers, solutions, new explanations.',0),(14,'en','Scientific','Studies or research, projects that look for answers, solutions, new explanations.',0),(14,'eu','Zientifikoa','Zenbait gaien ikasketak edo ikerketak, erantzun, azalpen, ebazpen berriak bilatzen dituzten proiektuak.',0),(14,'fr','Scientifique','Des études ou des recherches dans n\'importe quel domaine, des projets qui cherchent des réponses, des solutions, des nouvelles explications.',0),(14,'gl','Científico','Estudos ou investigacións dalgunha materia, proxectos que buscan respostas, solucións, explicacións novas.',0),(14,'it','Scientifico ','Studi o ricerche di qualche disciplina, progetti che cercano risposte, soluzioni, nuove spiegazioni. ',0),(14,'pl','Scientific','Studies or research, projects that look for answers, solutions, new explanations.',0),(15,'ca','','Usuaris per a proves en entorn real',0),(15,'eu','',' Benetazko ingurunean probak egiteko erabiltzaileak.',0),(15,'fr','Nombre:','Des utilisateurs pour des tests en condition réelle',0),(15,'gl','','Usuarios para probas en entorno real',0),(15,'it','','Utenti per prove in situazioni reali ',0),(16,'ca','Disseny','',0),(16,'en','Design','',0),(16,'gl','Deseño','',0),(16,'it','Design','Design ',0);

/*Table structure for table `comment` */

DROP TABLE IF EXISTS `comment`;

CREATE TABLE `comment` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `post` bigint(20) unsigned NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `text` text COLLATE utf8mb4_unicode_ci,
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Comentarios';

/*Data for the table `comment` */

/*Table structure for table `communication` */

DROP TABLE IF EXISTS `communication`;

CREATE TABLE `communication` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `subject` char(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `template` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `filter` int(11) NOT NULL,
  `type` char(20) CHARACTER SET utf8 NOT NULL DEFAULT 'md',
  `lang` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `header` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `error` tinytext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `communication_fk_1` (`filter`),
  CONSTRAINT `communication_fk_1` FOREIGN KEY (`filter`) REFERENCES `filter` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `communication` */

/*Table structure for table `communication_lang` */

DROP TABLE IF EXISTS `communication_lang`;

CREATE TABLE `communication_lang` (
  `id` bigint(20) unsigned DEFAULT NULL,
  `lang` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subject` char(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `communication_lang_fk` FOREIGN KEY (`id`) REFERENCES `communication` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `communication_lang` */

/*Table structure for table `communication_project` */

DROP TABLE IF EXISTS `communication_project`;

CREATE TABLE `communication_project` (
  `communication` bigint(20) unsigned DEFAULT NULL,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  UNIQUE KEY `id_communicationproject` (`communication`,`project`),
  KEY `project` (`project`),
  CONSTRAINT `communication_project_ibfk_1` FOREIGN KEY (`communication`) REFERENCES `communication` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `communication_project_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `communication_project` */

/*Table structure for table `conf` */

DROP TABLE IF EXISTS `conf`;

CREATE TABLE `conf` (
  `key` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT 'Clave',
  `value` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Para guardar pares para configuraciones, bloqueos etc';

/*Data for the table `conf` */

/*Table structure for table `contract` */

DROP TABLE IF EXISTS `contract`;

CREATE TABLE `contract` (
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `number` int(11) NOT NULL AUTO_INCREMENT,
  `electronic` tinyint(1) NOT NULL DEFAULT '1',
  `date` date NOT NULL COMMENT 'dia anterior a la publicacion',
  `enddate` date NOT NULL COMMENT 'finalización, un año despues de la fecha de contrato',
  `pdf` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Archivo pdf contrato',
  `type` varchar(1) CHARACTER SET utf8 NOT NULL DEFAULT '0' COMMENT '0 = persona física; 1 = representante asociacion; 2 = apoderado entidad mercantil',
  `name` tinytext CHARACTER SET utf8,
  `nif` varchar(14) CHARACTER SET utf8 DEFAULT NULL,
  `office` tinytext CHARACTER SET utf8 COMMENT 'Cargo en la asociación o empresa',
  `address` tinytext CHARACTER SET utf8,
  `location` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `region` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `zipcode` varchar(8) CHARACTER SET utf8 DEFAULT NULL,
  `country` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `entity_name` tinytext CHARACTER SET utf8,
  `entity_cif` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `entity_address` tinytext CHARACTER SET utf8,
  `entity_location` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `entity_region` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `entity_zipcode` varchar(8) CHARACTER SET utf8 DEFAULT NULL,
  `entity_country` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `reg_name` tinytext CHARACTER SET utf8 COMMENT 'Nombre y ciudad del registro en el que esta inscrita la entidad',
  `reg_date` date DEFAULT NULL,
  `reg_number` tinytext CHARACTER SET utf8 COMMENT 'Número de registro',
  `reg_loc` tinytext CHARACTER SET utf8 COMMENT 'NO SE USA (borrar)',
  `reg_id` tinytext CHARACTER SET utf8 COMMENT 'Número de protocolo del notario',
  `reg_idname` tinytext CHARACTER SET utf8 COMMENT 'Nombre del notario',
  `reg_idloc` tinytext CHARACTER SET utf8 COMMENT 'Ciudad de actuación del notario',
  `project_name` tinytext CHARACTER SET utf8 COMMENT 'Nombre del proyecto',
  `project_url` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'URL del proyecto',
  `project_owner` tinytext CHARACTER SET utf8 COMMENT 'Nombre del impulsor',
  `project_user` tinytext CHARACTER SET utf8 COMMENT 'Nombre del usuario autor del proyecto',
  `project_profile` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'URL del perfil del autor del proyecto',
  `project_description` text CHARACTER SET utf8 COMMENT 'Breve descripción del proyecto',
  `project_invest` text CHARACTER SET utf8 COMMENT 'objetivo del crowdfunding',
  `project_return` text CHARACTER SET utf8 COMMENT 'retornos',
  `bank` tinytext CHARACTER SET utf8,
  `bank_owner` tinytext CHARACTER SET utf8,
  `paypal` tinytext CHARACTER SET utf8,
  `paypal_owner` tinytext CHARACTER SET utf8,
  `fee` int(1) NOT NULL,
  `birthdate` date DEFAULT NULL,
  PRIMARY KEY (`project`),
  UNIQUE KEY `numero` (`number`),
  CONSTRAINT `contract_ibfk_1` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Contratos';

/*Data for the table `contract` */

/*Table structure for table `contract_status` */

DROP TABLE IF EXISTS `contract_status`;

CREATE TABLE `contract_status` (
  `contract` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT 'Id del proyecto',
  `owner` int(1) NOT NULL DEFAULT '0' COMMENT 'El impulsor ha dado por rellenados los datos',
  `owner_date` date DEFAULT NULL COMMENT 'Fecha que se cambia el flag',
  `owner_user` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Usuario que cambia el flag',
  `admin` int(1) NOT NULL DEFAULT '0' COMMENT 'El admin ha comenzado a revisar los datos',
  `admin_date` date DEFAULT NULL COMMENT 'Fecha que se cambia el flag',
  `admin_user` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Usuario que cambia el flag',
  `ready` int(1) NOT NULL DEFAULT '0' COMMENT 'Datos verificados y correctos',
  `ready_date` date DEFAULT NULL COMMENT 'Fecha que se cambia el flag',
  `ready_user` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Usuario que cambia el flag',
  `pdf` int(1) NOT NULL COMMENT 'El impulsor ha descargado el pdf',
  `pdf_date` date DEFAULT NULL COMMENT 'Fecha que se cambia el flag',
  `pdf_user` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Usuario que cambia el flag',
  `received` int(1) NOT NULL DEFAULT '0' COMMENT 'Se ha recibido el contrato firmado',
  `received_date` date DEFAULT NULL COMMENT 'Fecha que se cambia el flag',
  `received_user` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Usuario que cambia el flag',
  `payed` int(1) NOT NULL DEFAULT '0' COMMENT 'Se ha realizado el pago al proyecto',
  `payed_date` date DEFAULT NULL COMMENT 'Fecha que se cambia el flag',
  `payed_user` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Usuario que cambia el flag',
  `prepay` int(1) NOT NULL DEFAULT '0' COMMENT 'Ha habido pago avanzado',
  `prepay_date` date DEFAULT NULL COMMENT 'Fecha que se cambia el flag',
  `prepay_user` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Usuario que cambia el flag',
  `closed` int(1) NOT NULL DEFAULT '0' COMMENT 'Contrato finiquitado',
  `closed_date` date DEFAULT NULL COMMENT 'Fecha que se cambia el flag',
  `closed_user` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Usuario que cambia el flag',
  PRIMARY KEY (`contract`),
  KEY `admin_user` (`admin_user`),
  KEY `closed_user` (`closed_user`),
  KEY `owner_user` (`owner_user`),
  KEY `payed_user` (`payed_user`),
  KEY `pdf_user` (`pdf_user`),
  KEY `prepay_user` (`prepay_user`),
  KEY `ready_user` (`ready_user`),
  KEY `received_user` (`received_user`),
  CONSTRAINT `contract_status_ibfk_1` FOREIGN KEY (`contract`) REFERENCES `contract` (`project`) ON UPDATE CASCADE,
  CONSTRAINT `contract_status_ibfk_2` FOREIGN KEY (`owner_user`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `contract_status_ibfk_3` FOREIGN KEY (`admin_user`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `contract_status_ibfk_4` FOREIGN KEY (`pdf_user`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `contract_status_ibfk_5` FOREIGN KEY (`payed_user`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `contract_status_ibfk_6` FOREIGN KEY (`prepay_user`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `contract_status_ibfk_7` FOREIGN KEY (`closed_user`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `contract_status_ibfk_8` FOREIGN KEY (`ready_user`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `contract_status_ibfk_9` FOREIGN KEY (`received_user`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Seguimiento de estado de contrato';

/*Data for the table `contract_status` */

/*Table structure for table `cost` */

DROP TABLE IF EXISTS `cost`;

CREATE TABLE `cost` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `cost` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `type` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `amount` int(5) DEFAULT '0',
  `required` tinyint(1) DEFAULT '0',
  `from` date DEFAULT NULL,
  `until` date DEFAULT NULL,
  `order` int(10) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `order` (`order`),
  KEY `project` (`project`),
  CONSTRAINT `cost_ibfk_1` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Desglose de costes de proyectos';

/*Data for the table `cost` */

insert  into `cost`(`id`,`project`,`cost`,`description`,`type`,`amount`,`required`,`from`,`until`,`order`) values (1,'project-passing-today','Cost name','Test description','task',100,1,'2020-03-05','2020-04-09',1),(2,'project-finishing-today','Cost 1','Description cost 1','task',50,1,'2016-05-03','2016-05-16',1),(3,'project-finishing-today','Cost 2','Description cost 2','task',150,1,'2016-05-03','2016-05-16',1),(4,'project-finishing-today','Cost 3','Description cost 3','task',200,0,'2016-05-03','2016-05-16',1),(5,'project-passed','Cost name','Test description','task',100,1,'2019-11-26','2020-04-09',1);

/*Table structure for table `cost_lang` */

DROP TABLE IF EXISTS `cost_lang`;

CREATE TABLE `cost_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `cost` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`),
  KEY `project` (`project`),
  CONSTRAINT `cost_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `cost` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `cost_lang_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `cost_lang` */

/*Table structure for table `criteria` */

DROP TABLE IF EXISTS `criteria`;

CREATE TABLE `criteria` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `section` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT 'node',
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `order` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Criterios de puntuación';

/*Data for the table `criteria` */

insert  into `criteria`(`id`,`section`,`title`,`description`,`order`) values (5,'project','Es original','donde va esta descripción? donde esta el tool tip?\r\n\r\nHola, este tooltip ira en el formulario de revision',1),(6,'project','Es eficaz en su estrategia de comunicación','',2),(7,'project','Aporta información suficiente del proyecto','',3),(8,'project','Aporta productos, servicios o valores “deseables” para la comunidad','',4),(9,'project','Es afín a la cultura abierta','',5),(10,'project','Puede crecer, es escalable','',6),(11,'project','Son coherentes los recursos solicitados con los objetivos y el tiempo de desarrollo','',7),(12,'project','Riesgo proporcional al grado de beneficios (sociales, culturales y/o económicos)','Test descripción de un criterio...',8),(13,'owner','Posee buena reputación en su sector','',1),(14,'owner','Ha trabajado con organizaciones y colectivos con buena reputación','',2),(15,'owner','Aporta información sobre experiencias anteriores (éxitos y fracasos)','',3),(16,'owner','Tiene capacidades para llevar a cabo el proyecto','',4),(17,'owner','Cuenta con un equipo formado','',5),(18,'owner','Cuenta con una comunidad de seguidores','',6),(19,'owner','Tiene visibilidad en la red','',7),(20,'reward','Es viable (su coste está incluido en la producción del proyecto)','',1),(21,'reward','Puede tener efectos positivos, transformadores (sociales, culturales, empresariales)','',2),(22,'reward','Aporta conocimiento nuevo, de difícil acceso o en proceso de desaparecer','',3),(23,'reward','Aporta oportunidades de generar economía alrededor','',4),(24,'reward','Da libertad en el uso de sus resultados (es reproductible)','',5),(25,'reward','Ofrece un retorno atractivo (por original, por útil, por inspirador... )','',6),(26,'reward','Cuenta con actualizaciones','',7),(27,'reward','Integra a la comunidad (a los seguidores, cofinanciadores, a un grupo social)','',8);

/*Table structure for table `criteria_lang` */

DROP TABLE IF EXISTS `criteria_lang`;

CREATE TABLE `criteria_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `criteria_lang` */

insert  into `criteria_lang`(`id`,`lang`,`title`,`description`,`pending`) values (5,'ca','És original',NULL,0),(5,'fr','C\'est original',NULL,0),(5,'gl','É orixinal',NULL,0),(6,'ca','És eficaç en la seva estratègia de comunicació',NULL,0),(6,'fr','Soyez efficace dans votre stratégie de communication',NULL,0),(6,'gl','É eficaz na súa estratexia de comunicación',NULL,0),(7,'ca','Aporta suficient informació del projecte',NULL,0),(7,'fr','Fournit des informations suffisantes sur le projet',NULL,0),(7,'gl','Achega información suficiente do proxecto',NULL,0),(8,'ca','Aporta productes, serveis o valors “desitjables” per a la comunitat',NULL,0),(8,'fr','Fournit des produits, des services ou des valeurs \"souhaitables\" pour la communauté',NULL,0),(8,'gl','Achega produtos, servizos ou valores \"desexables\" para a comunidade',NULL,0),(9,'ca','Es afí a la cultura oberta',NULL,0),(9,'fr','S\'apparente à la culture libre.',NULL,0),(9,'gl','É afín á cultura aberta',NULL,0),(10,'ca','Pot créixer, és escalable',NULL,0),(10,'fr','Est capable de se développer, peut être mis à l\'échelle',NULL,0),(11,'ca','Són coherents els recursos sol.licitats amb els objectius i el temps de desenvolupament',NULL,0),(11,'fr','les ressources demandées sont cohérentes avec les objectifs et le calendrier de développement',NULL,0),(11,'gl','Son coherentes os recursos solicitados cos obxectivos e o tempo de desenrolo',NULL,0),(12,'ca','Risc proporcional al grau de benefici (social, cultural i/o econòmic)',NULL,0),(12,'fr','Risque proportionnel aux bénéfices attendus (sociaux, culturels et/ou économiques)',NULL,0),(12,'gl','Risco proporcional ó grado de beneficios (sociais, culturais e/ou económicos)',NULL,0),(13,'ca','Posseeix bona reputació en el seu sector',NULL,0),(13,'fr','A bonne réputation dans son secteur',NULL,0),(13,'gl','Posúe unha boa reputación no seu sector',NULL,0),(14,'ca','Ha treballat amb organitzacions i col·lectius amb bona reputació',NULL,0),(14,'fr','A travaillé avec des organismes et des collectives ayant bonne réputation',NULL,0),(14,'gl','Traballou con organizacións e colectivos con boa reputación',NULL,0),(15,'ca','Aporta informació sobre experiències anteriors (èxits i fracassos)',NULL,0),(15,'fr','Fournit des informations sur des expériences antérieurs (les succès comme les échecs)',NULL,0),(15,'gl','Achega información sobre experiencias anteriores (éxitos ou fracasos)',NULL,0),(16,'ca','Té capacitats per dur a terme el projecte',NULL,0),(16,'fr','Possède la capacité de mener le projet à son terme',NULL,0),(16,'gl','Ten capacidades para levar a cabo o proxecto',NULL,0),(17,'ca','Compta amb un equip format',NULL,0),(17,'fr','Dispose d\'une équipe formée',NULL,0),(17,'gl','Conta cun equipo formado',NULL,0),(18,'ca','Compta amb una comunitat de seguidors',NULL,0),(18,'fr','Dispose d\'une communauté de suiveurs (followers)',NULL,0),(18,'gl','Conta cunha comunidade de seguidores',NULL,0),(19,'ca','Té visibilitat a la xarxa',NULL,0),(19,'fr','Gagne de la visibilité sur le réseau',NULL,0),(19,'gl','Ten visibilidade na rede',NULL,0),(20,'ca','És viable (el seu cost està inclòs en la producció del projecte)',NULL,0),(20,'fr','Est viable (vos coûts sont inclus dans la production du projet)',NULL,0),(20,'gl','É viable (o seu custo está incluído na produción do proxecto)',NULL,0),(21,'ca','Pot tenir efectes positius, transformadors (socials, culturals, empresarials)',NULL,0),(21,'fr','Peut avoir des conséquences positives (sociales, culturelles, entreprenariales)',NULL,0),(21,'gl','Pode ter efectos positivos, transformadores (sociais, culturais, empresariais)',NULL,0),(22,'ca','Aporta coneixement nou, de difícil accés o en procés de desaparèixer',NULL,0),(22,'fr','Donne de nouvelles connaissances, difficile d\'accès ou en voie de disparition',NULL,0),(22,'gl','Achega coñecemento novo, de difícil acceso ou en proceso de desaparecer',NULL,0),(23,'ca','Aporta oportunitats de generar economia al voltant',NULL,0),(23,'fr','Offre la possibilité de générer une économie liée (connexe)',NULL,0),(23,'gl','Achega oportunidades de xerar economía ó redor',NULL,0),(24,'ca','Dóna llibertat en l\'ús dels seus resultats (és reproduïble)',NULL,0),(24,'fr','Autorise la réutilisation de ses résultats  (reproductibilité)',NULL,0),(24,'gl','Dá liberdade no uso dos seus resultados (é reproducible)',NULL,0),(25,'ca','Ofereix un retorn atractiu (per original, per útil, per inspirador...)',NULL,0),(25,'fr','Propose des retombées séduisantes (par leur originalité, leur utilité, leur inspiration...)',NULL,0),(25,'gl','Ofrece un retorno atractivo (por orixinal, por útil, por inspirador...)',NULL,0),(26,'ca','Compta amb actualitzacions',NULL,0),(26,'fr','Compte sur les actualisations',NULL,0),(26,'gl','Conta con actualizacións',NULL,0),(27,'ca','Integra a la comunitat (a la gent seguidora, cofinançadora, a un grup social)',NULL,0),(27,'fr','S\'intègre à la communauté (des suiveurs, des cofinanceurs, à un groupe social)',NULL,0),(27,'gl','Integra á comunidade (os seguidores, cofinanceiros, a un grupo social)',NULL,0);

/*Table structure for table `document` */

DROP TABLE IF EXISTS `document`;

CREATE TABLE `document` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `contract` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` varchar(120) CHARACTER SET utf8 DEFAULT NULL,
  `size` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `contract` (`contract`),
  CONSTRAINT `document_ibfk_1` FOREIGN KEY (`contract`) REFERENCES `contract` (`project`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `document` */

/*Table structure for table `donor` */

DROP TABLE IF EXISTS `donor`;

CREATE TABLE `donor` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(50) NOT NULL,
  `amount` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `surname` varchar(255) DEFAULT NULL COMMENT 'Apellido',
  `surname2` char(255) DEFAULT NULL,
  `nif` varchar(13) DEFAULT NULL,
  `address` tinytext,
  `zipcode` varchar(10) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL COMMENT 'Provincia',
  `country` varchar(50) DEFAULT NULL,
  `countryname` varchar(255) DEFAULT NULL COMMENT 'Nombre del pais',
  `gender` char(1) DEFAULT NULL,
  `birthyear` year(4) DEFAULT NULL,
  `numproj` int(2) DEFAULT '1',
  `year` varchar(4) NOT NULL,
  `edited` int(1) NOT NULL DEFAULT '0' COMMENT 'Revisados por el usuario',
  `confirmed` int(1) NOT NULL DEFAULT '0' COMMENT 'Certificado generado',
  `pdf` varchar(255) NOT NULL DEFAULT '' COMMENT 'nombre del archivo de certificado',
  `processed` date NOT NULL COMMENT 'Si se ha presentado el certificado en hacienda',
  `created` datetime DEFAULT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user` (`user`),
  KEY `year` (`year`),
  CONSTRAINT `donor_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Datos fiscales donativo';

/*Data for the table `donor` */

/*Table structure for table `donor_invest` */

DROP TABLE IF EXISTS `donor_invest`;

CREATE TABLE `donor_invest` (
  `donor_id` bigint(20) unsigned NOT NULL,
  `invest_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`donor_id`,`invest_id`),
  KEY `invest_id` (`invest_id`),
  CONSTRAINT `donor_invest_ibfk_1` FOREIGN KEY (`donor_id`) REFERENCES `donor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `donor_invest_ibfk_2` FOREIGN KEY (`invest_id`) REFERENCES `invest` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `donor_invest` */

/*Table structure for table `donor_location` */

DROP TABLE IF EXISTS `donor_location`;

CREATE TABLE `donor_location` (
  `id` bigint(20) unsigned NOT NULL,
  `latitude` decimal(16,14) NOT NULL,
  `longitude` decimal(16,14) NOT NULL,
  `radius` smallint(6) unsigned NOT NULL DEFAULT '0',
  `method` varchar(50) NOT NULL DEFAULT 'ip',
  `locable` tinyint(1) NOT NULL DEFAULT '0',
  `city` varchar(255) NOT NULL,
  `region` varchar(255) NOT NULL,
  `country` varchar(150) NOT NULL,
  `country_code` varchar(2) NOT NULL,
  `info` varchar(255) DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `locable` (`locable`),
  CONSTRAINT `donor_location_ibfk_1` FOREIGN KEY (`id`) REFERENCES `donor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `donor_location` */

/*Table structure for table `event` */

DROP TABLE IF EXISTS `event`;

CREATE TABLE `event` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `type` char(20) CHARACTER SET utf8 NOT NULL DEFAULT 'communication',
  `action` char(100) CHARACTER SET utf8 NOT NULL,
  `hash` char(32) CHARACTER SET utf8 NOT NULL,
  `result` char(255) CHARACTER SET utf8 DEFAULT NULL,
  `created` datetime NOT NULL,
  `finalized` datetime DEFAULT NULL,
  `succeeded` tinyint(1) DEFAULT '0',
  `error` char(255) CHARACTER SET utf8 DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `hash` (`hash`),
  KEY `succeeded` (`succeeded`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `event` */

/*Table structure for table `faq` */

DROP TABLE IF EXISTS `faq`;

CREATE TABLE `faq` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `node` varchar(50) CHARACTER SET utf8 NOT NULL,
  `section` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT 'node',
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `order` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `node` (`node`),
  CONSTRAINT `faq_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Preguntas frecuentes';

/*Data for the table `faq` */

/*Table structure for table `faq_lang` */

DROP TABLE IF EXISTS `faq_lang`;

CREATE TABLE `faq_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `faq_lang` */

/*Table structure for table `feed` */

DROP TABLE IF EXISTS `feed`;

CREATE TABLE `feed` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `url` tinytext CHARACTER SET utf8,
  `datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `scope` varchar(50) CHARACTER SET utf8 NOT NULL,
  `type` varchar(50) CHARACTER SET utf8 NOT NULL,
  `html` text COLLATE utf8mb4_unicode_ci,
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Contiene nombre de archivo',
  `target_type` varchar(10) CHARACTER SET utf8 DEFAULT NULL COMMENT 'tipo de objetivo',
  `target_id` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'registro objetivo',
  `post` int(20) unsigned DEFAULT NULL COMMENT 'Entrada de blog',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `scope` (`scope`),
  KEY `type` (`type`),
  KEY `target_type` (`target_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Log de eventos';

/*Data for the table `feed` */

/*Table structure for table `filter` */

DROP TABLE IF EXISTS `filter`;

CREATE TABLE `filter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `cert` tinyint(1) DEFAULT NULL,
  `role` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `startdate` date DEFAULT NULL,
  `enddate` date DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `typeofdonor` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `foundationdonor` tinyint(1) DEFAULT NULL,
  `wallet` tinyint(1) DEFAULT NULL,
  `project_latitude` decimal(16,14) DEFAULT NULL,
  `project_longitude` decimal(16,14) DEFAULT NULL,
  `project_radius` smallint(6) unsigned DEFAULT NULL,
  `project_location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `forced` tinyint(1) DEFAULT NULL COMMENT 'If the filter does not consider user_prefer.mailing',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `filter` */

/*Table structure for table `filter_call` */

DROP TABLE IF EXISTS `filter_call`;

CREATE TABLE `filter_call` (
  `filter` int(11) NOT NULL,
  `call` varchar(50) CHARACTER SET utf8 NOT NULL,
  UNIQUE KEY `id_filtercalls` (`filter`,`call`),
  KEY `call` (`call`),
  CONSTRAINT `filter_call_ibfk_1` FOREIGN KEY (`filter`) REFERENCES `filter` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `filter_call_ibfk_2` FOREIGN KEY (`call`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `filter_call` */

/*Table structure for table `filter_footprint` */

DROP TABLE IF EXISTS `filter_footprint`;

CREATE TABLE `filter_footprint` (
  `filter` int(11) NOT NULL,
  `footprint` int(10) unsigned NOT NULL,
  UNIQUE KEY `id_filterfootprint` (`filter`,`footprint`),
  KEY `footprint` (`footprint`),
  CONSTRAINT `filter_footprint_ibfk_1` FOREIGN KEY (`filter`) REFERENCES `filter` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `filter_footprint_ibfk_2` FOREIGN KEY (`footprint`) REFERENCES `footprint` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `filter_footprint` */

/*Table structure for table `filter_matcher` */

DROP TABLE IF EXISTS `filter_matcher`;

CREATE TABLE `filter_matcher` (
  `filter` int(11) NOT NULL,
  `matcher` varchar(50) CHARACTER SET utf8 NOT NULL,
  UNIQUE KEY `id_filtermatcher` (`filter`,`matcher`),
  KEY `matcher` (`matcher`),
  CONSTRAINT `filter_matcher_ibfk_1` FOREIGN KEY (`filter`) REFERENCES `filter` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `filter_matcher_ibfk_2` FOREIGN KEY (`matcher`) REFERENCES `matcher` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `filter_matcher` */

/*Table structure for table `filter_project` */

DROP TABLE IF EXISTS `filter_project`;

CREATE TABLE `filter_project` (
  `filter` int(11) NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  UNIQUE KEY `id_filterprojects` (`filter`,`project`),
  KEY `project` (`project`),
  CONSTRAINT `filter_project_ibfk_1` FOREIGN KEY (`filter`) REFERENCES `filter` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `filter_project_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `filter_project` */

/*Table structure for table `filter_sdg` */

DROP TABLE IF EXISTS `filter_sdg`;

CREATE TABLE `filter_sdg` (
  `filter` int(11) NOT NULL,
  `sdg` int(10) unsigned NOT NULL,
  UNIQUE KEY `id_filtersdg` (`filter`,`sdg`),
  KEY `sdg` (`sdg`),
  CONSTRAINT `filter_sdg_ibfk_1` FOREIGN KEY (`filter`) REFERENCES `filter` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `filter_sdg_ibfk_2` FOREIGN KEY (`sdg`) REFERENCES `sdg` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `filter_sdg` */

/*Table structure for table `footprint` */

DROP TABLE IF EXISTS `footprint`;

CREATE TABLE `footprint` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `icon` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `footprint` */

insert  into `footprint`(`id`,`name`,`icon`,`description`,`modified`) values (1,'A/ Huella ecologica',NULL,'','2018-09-27 01:36:38'),(2,'B/ Huella social',NULL,'','2018-09-27 01:36:38'),(3,'C/ Huella democratica',NULL,'','2018-09-27 01:36:38');

/*Table structure for table `footprint_lang` */

DROP TABLE IF EXISTS `footprint_lang`;

CREATE TABLE `footprint_lang` (
  `id` int(10) unsigned NOT NULL,
  `lang` varchar(2) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `pending` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`,`lang`),
  CONSTRAINT `footprint_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `footprint` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `footprint_lang` */

insert  into `footprint_lang`(`id`,`lang`,`name`,`description`,`pending`) values (1,'ca','A/ Petjada ecològica','',0),(1,'en','A/ Ecological footprint','',0),(2,'ca','B/ Petjada social','',0),(2,'en','B/ Social footprint','',0),(3,'ca','C/ Petjada democràtica','',0),(3,'en','C/ Democratic footprint','',0);

/*Table structure for table `glossary` */

DROP TABLE IF EXISTS `glossary`;

CREATE TABLE `glossary` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `text` longtext COLLATE utf8mb4_unicode_ci,
  `media` tinytext CHARACTER SET utf8,
  `legend` text COLLATE utf8mb4_unicode_ci,
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Imagen principal',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Entradas para el glosario';

/*Data for the table `glossary` */

/*Table structure for table `glossary_image` */

DROP TABLE IF EXISTS `glossary_image`;

CREATE TABLE `glossary_image` (
  `glossary` bigint(20) unsigned NOT NULL,
  `image` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT 'Contiene nombre de archivo',
  `order` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`glossary`,`image`),
  CONSTRAINT `glossary_image_ibfk_1` FOREIGN KEY (`glossary`) REFERENCES `glossary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `glossary_image` */

/*Table structure for table `glossary_lang` */

DROP TABLE IF EXISTS `glossary_lang`;

CREATE TABLE `glossary_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `text` longtext COLLATE utf8mb4_unicode_ci,
  `legend` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `glossary_lang` */

/*Table structure for table `home` */

DROP TABLE IF EXISTS `home`;

CREATE TABLE `home` (
  `item` varchar(10) CHARACTER SET utf8 NOT NULL,
  `type` varchar(5) CHARACTER SET utf8 NOT NULL DEFAULT 'main' COMMENT 'lateral o central',
  `node` varchar(50) CHARACTER SET utf8 NOT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  UNIQUE KEY `item_node` (`item`,`node`),
  KEY `node` (`node`),
  CONSTRAINT `home_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Elementos en portada';

/*Data for the table `home` */

insert  into `home`(`item`,`type`,`node`,`order`) values ('promotes','main','goteo',1);

/*Table structure for table `icon` */

DROP TABLE IF EXISTS `icon`;

CREATE TABLE `icon` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 NOT NULL,
  `description` tinytext COLLATE utf8mb4_unicode_ci,
  `group` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'exclusivo para grupo',
  `order` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Iconos para retorno/recompensa';

/*Data for the table `icon` */

insert  into `icon`(`id`,`name`,`description`,`group`,`order`) values ('code','Código fuente','Por código fuente entendemos programas y software en general.','social',0),('design','Diseño','Los diseños pueden ser de planos o patrones, esquemas, esbozos, diagramas de flujo, etc.','social',0),('file','Archivos digitales','Los archivos digitales pueden ser de música, vídeo, documentos de texto, etc.','',0),('manual','Manuales','Documentos prácticos detallando pasos, materiales formativos, bussiness plans, “how tos”, recetas, etc.','social',0),('money','Dinero','Retornos económicos proporcionales a la inversión realizada, que se deben detallar en cantidad pero también forma de pago.','individual',50),('other','Otro','Sorpréndenos con esta nueva tipología, realmente nos interesa :) ','',99),('product','Producto','Los productos pueden ser los que se han producido, en edición limitada, o fragmentos u obras derivadas del original.','individual',0),('service','Servicios','Acciones y/o sesiones durante tiempo determinado para satisfacer una necesidad individual o de grupo: una formación, una ayuda técnica, un asesoramiento, etc.','',0),('thanks','Reconocimiento','Agradecimiento o reconocimiento','individual',90);

/*Table structure for table `icon_lang` */

DROP TABLE IF EXISTS `icon_lang`;

CREATE TABLE `icon_lang` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `description` tinytext COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `icon_lang` */

insert  into `icon_lang`(`id`,`lang`,`name`,`description`,`pending`) values ('code','ca','Codi font','Per codi font entenem programes i programari en general.',0),('code','el','Source code','By source code, we mean programs and software in general.',0),('code','en','Source code','By source code, we mean programs and software in general.',0),('code','eu','Iturri Kodea','Iturri Kode bezala ulertzen dugu  programak eta sofwareak orokorrean\r\n\r\n',0),('code','fr','Code source','Par code source nous entendons tous programmes et logiciels en général.',0),('code','it','Codice sorgente','Per codice sorgente intendiamo genericamente programmi e software ',0),('code','pl','Source code','By source code, we mean programs and software in general.',0),('design','ca','Disseny','Els dissenys poden ser de plànols o patrons, esquemes, esbossos, diagrames de flux, etc.',0),('design','el','Design','Designs can be drawings, patterns, sketches, rough drafts, flowcharts, etc.',0),('design','en','Design','Designs can be drawings, patterns, sketches, rough drafts, flowcharts, etc.',0),('design','eu','Diseinua','Diseinuak, planoak, ereduak, eskemak, ideia orokorrak, fluxu-diagramak etab. izan daitezke\r\n',0),('design','fr','Plans','Les plans peuvent être des dessins et patrons, des modèles, schémas, croquis, diagrammes de flux etc.',0),('design','it','Design','Il design può essere costituito da piani, schemi, bozze, diagrammi di flusso, ecc.',0),('design','pl','Design','Designs can be drawings, patterns, sketches, rough drafts, flowcharts, etc.',0),('file','ca','Arxius digitals','Els arxius digitals poden ser de música, vídeo, documents de text, etc.',0),('file','el','Digital files','Digital files may be music, video, text documents, etc.',0),('file','en','Digital files','Digital files may be music, video, text documents, etc.',0),('file','eu','Artxibategi digitalak','Artxibategi dilitalak,  musika, bideo, testu dokumentuak etab., izan daitezke',0),('file','fr','Archives numériques','Les archives numériques peuvent être de type audio, vidéo, des documents textes, etc.',0),('file','it','Archivi digitali ','Gli archivi digitali possono essere musicali, video, documenti di testo, ecc.',0),('file','pl','Digital files','Digital files may be music, video, text documents, etc.',0),('manual','ca','Manuals','Documents pràctics detallant passos, materials formatius, plans de negoci, “how tos”, receptes, etc.',0),('manual','el','Manuals','Practical documentation that details step-by-step instructions, tutorials, business plans, how-to\'s, code cookbooks, etc. ',0),('manual','en','Manuals','Practical documentation that details step-by-step instructions, tutorials, business plans, how-to\'s, code cookbooks, etc. ',0),('manual','eu','Gidaliburuak','  Eman behar diren pausuak, formaziorako materialak, bussiness plans, “how tos”, errezetak, etab. agertzen diren dokumentu praktikoak',0),('manual','fr','Modes d\'emploi','Documents pratiques détaillant les étapes, les matériaux et équipements, les \"business plans\", des manuels et recettes, etc.',0),('manual','it','Manuali','Documenti pratici che spiegano gli step, materiale informativo, bussiness plans, “how tos”, ricette, ecc.',0),('manual','pl','Manuals','Practical documentation that details step-by-step instructions, tutorials, business plans, how-to\'s, code cookbooks, etc. ',0),('money','ca','Diners','Retorns econòmics proporcionals a la inversió realitzada, que s\'han de detallar en quantitat però també forma de pagament.',0),('money','el','Money','Economic benefits that are proportional to the investment made, with details about quantity and also form of payment',0),('money','en','Money','Economic benefits that are proportional to the investment made, with details about quantity and also form of payment',0),('money','eu','Dirua','Egindako inbertsioen itzulera ekonomiko proportzionalak, kantitatean zehaztu beharrekoa, baina baita ordaindu beharreko forman ere\r\n\r\n',0),('money','fr','Argent','Les retombées économiques proportionnelles à l\'investissement, qui doivent être détaillées en quantité comme en mode de paiement.',0),('money','it','Denaro ','Benefici economici proporzionali all\'investimento realizzato le cui quantità devono essere specificate in forma di pagamento. ',0),('money','pl','Money','Economic benefits that are proportional to the investment made, with details about quantity and also form of payment',0),('other','ca','Altres','Sorprèn-nos amb aquesta nova tipologia, realment ens interessa :) ',0),('other','el','Other','Surprise us with this category, we\'re really interested!',0),('other','en','Other','Surprise us with this category, we\'re really interested!',0),('other','eu','Beste bat','Harritu gaitzazu tipologi berri honekin, benetan interesatzen gaitu :)\r\n\r\n',0),('other','fr','Divers','Surprenez-nous avec une nouvelle catégorie, cela nous intéresse vraiment ;-)',0),('other','it','Altro',' Sorprendici con questa nuova metodologia, ci interessa davvero :)',0),('other','pl','Other','Surprise us with this category, we\'re really interested!',0),('product','ca','Producte','Els productes poden ser els que s\'han produït, en edició limitada, o fragments o obres derivades de l\'original.',0),('product','el','Product','Products can be limited editions or prototypes, or pieces or works derived from the original.',0),('product','en','Product','Products can be limited editions or prototypes, or pieces or works derived from the original.',0),('product','eu','Produktua','Produktuak edizio mugatuan, edo zati, zein jatorritik deribatuta dauden lanetatik ekoiztutakoak izan daitezke\r\n',0),('product','fr','Objets','Ces objets peuvent être produits par vos soins, en édition limitée, ou des fragments et œuvres dérivées de l\'\'original.',0),('product','it','Prodotto','I prodotti possono essere quelli che si sono realizzati, in edizione limitada, frammantaria o opere derivate dall\'originale.',0),('product','pl','Product','Products can be limited editions or prototypes, or pieces or works derived from the original.',0),('service','ca','Serveis','Accions i/o sessions durant temps determinat per satisfer una necessitat individual o de grup: una formació, una ajuda tècnica, un assessorament, etc.',0),('service','el','Services','Actions or sessions during a specific period of time which satisfy an individual or group need: education, technical assistance, advice, etc. ',0),('service','en','Services','Actions or sessions during a specific period of time which satisfy an individual or group need: education, technical assistance, advice, etc. ',0),('service','eu','Zerbitzuak','Taldeko zein bakarkako beharrizanak asetzeko  egindako ekintza edo/eta saioak denbora jakin batean: formazioa, laguntza teknikoa, aholkularitza, etab. ...\r\n\r\n',0),('service','fr','Services','Actions ou sessions à durée déterminée destinées à satisfaire un besoin individuel ou collectif: une formation, une assistance technique, du conseil, etc.',0),('service','it','Servizi','Azioni e/o sessioni per un tempo determinato per soddisfare una necessità individuale o di gruppo: formazione, aiuto tecnico, consulenza, ecc. ',0),('service','pl','Services','Actions or sessions during a specific period of time which satisfy an individual or group need: education, technical assistance, advice, etc. ',0),('thanks','ca','Reconeixement','Agraïment o reconeixement',0),('thanks','el','Acknowledgment','Gratitude or acknowledgment',0),('thanks','en','Acknowledgment','Gratitude or acknowledgment',0),('thanks','fr','Remerciements','Remerciements',0),('thanks','it','Riconoscenza','Ringraziamento o riconoscenza',0),('thanks','pl','Acknowledgment','Gratitude or acknowledgment',0);

/*Table structure for table `icon_license` */

DROP TABLE IF EXISTS `icon_license`;

CREATE TABLE `icon_license` (
  `icon` varchar(50) CHARACTER SET utf8 NOT NULL,
  `license` varchar(50) CHARACTER SET utf8 NOT NULL,
  UNIQUE KEY `icon` (`icon`,`license`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Licencias para cada icono, solo social';

/*Data for the table `icon_license` */

insert  into `icon_license`(`icon`,`license`) values ('code','agpl'),('code','apache'),('code','balloon'),('code','bsd'),('code','cernohl'),('code','gpl'),('code','gpl2'),('code','lgpl'),('code','mit'),('code','mpl'),('code','odbl'),('code','odcby'),('code','oshw'),('code','pd'),('code','php'),('code','tapr'),('code','xoln'),('design','balloon'),('design','cc0'),('design','ccby'),('design','ccbync'),('design','ccbyncnd'),('design','ccbyncsa'),('design','ccbynd'),('design','ccbysa'),('design','cernohl'),('design','fal'),('design','fdl'),('design','gpl'),('design','gpl2'),('design','oshw'),('design','pd'),('design','tapr'),('file','cc0'),('file','ccby'),('file','ccbync'),('file','ccbyncnd'),('file','ccbyncsa'),('file','ccbynd'),('file','ccbysa'),('file','fal'),('manual','cc0'),('manual','ccby'),('manual','ccbync'),('manual','ccbyncnd'),('manual','ccbyncsa'),('manual','ccbynd'),('manual','ccbysa'),('manual','cernohl'),('manual','fal'),('manual','fdl'),('manual','freebsd'),('manual','pd');

/*Table structure for table `image` */

DROP TABLE IF EXISTS `image`;

CREATE TABLE `image` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `type` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `size` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `image` */

/*Table structure for table `info` */

DROP TABLE IF EXISTS `info`;

CREATE TABLE `info` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `node` varchar(50) CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `text` longtext COLLATE utf8mb4_unicode_ci,
  `media` tinytext CHARACTER SET utf8,
  `publish` tinyint(1) NOT NULL DEFAULT '0',
  `order` int(11) DEFAULT '1',
  `legend` text COLLATE utf8mb4_unicode_ci,
  `gallery` varchar(2000) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Galería de imagenes',
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Imagen principal',
  `share_facebook` tinytext COLLATE utf8mb4_unicode_ci,
  `share_twitter` tinytext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `node` (`node`),
  CONSTRAINT `info_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Entradas about';

/*Data for the table `info` */

/*Table structure for table `info_image` */

DROP TABLE IF EXISTS `info_image`;

CREATE TABLE `info_image` (
  `info` bigint(20) unsigned NOT NULL,
  `image` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT 'Contiene nombre de archivo',
  `order` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`info`,`image`),
  CONSTRAINT `info_image_ibfk_1` FOREIGN KEY (`info`) REFERENCES `info` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `info_image` */

/*Table structure for table `info_lang` */

DROP TABLE IF EXISTS `info_lang`;

CREATE TABLE `info_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `text` longtext COLLATE utf8mb4_unicode_ci,
  `legend` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  `share_facebook` tinytext COLLATE utf8mb4_unicode_ci,
  `share_twitter` tinytext COLLATE utf8mb4_unicode_ci,
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `info_lang` */

/*Table structure for table `invest` */

DROP TABLE IF EXISTS `invest`;

CREATE TABLE `invest` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `account` varchar(256) CHARACTER SET utf8 NOT NULL COMMENT 'Solo para aportes de cash',
  `amount` int(6) NOT NULL,
  `amount_original` int(6) DEFAULT NULL COMMENT 'Importe introducido por el usuario',
  `currency` varchar(4) CHARACTER SET utf8 NOT NULL DEFAULT 'EUR' COMMENT 'Divisa al aportar',
  `currency_rate` decimal(9,5) NOT NULL DEFAULT '1.00000' COMMENT 'Ratio de conversión a eurio al aportar',
  `donate_amount` int(10) NOT NULL,
  `status` int(1) NOT NULL COMMENT '-1 en proceso, 0 pendiente, 1 cobrado, 2 devuelto, 3 pagado al proyecto',
  `anonymous` tinyint(1) NOT NULL DEFAULT '0',
  `resign` tinyint(1) NOT NULL DEFAULT '0',
  `invested` date DEFAULT NULL,
  `charged` date DEFAULT NULL,
  `returned` date DEFAULT NULL,
  `preapproval` varchar(256) CHARACTER SET utf8 DEFAULT NULL COMMENT 'PreapprovalKey',
  `payment` varchar(256) CHARACTER SET utf8 DEFAULT NULL COMMENT 'PayKey',
  `transaction` varchar(256) CHARACTER SET utf8 DEFAULT NULL COMMENT 'PaypalId',
  `method` varchar(20) CHARACTER SET utf8 NOT NULL COMMENT 'Metodo de pago',
  `admin` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Admin que creó el aporte manual',
  `campaign` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'si es un aporte de capital riego',
  `datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `drops` bigint(20) unsigned DEFAULT NULL COMMENT 'id del aporte que provoca este riego',
  `droped` bigint(20) unsigned DEFAULT NULL COMMENT 'id del riego generado por este aporte',
  `call` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'campaña dedonde sale el dinero',
  `matcher` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `issue` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Problemas con el cobro del aporte',
  `pool` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'A reservar si el proyecto falla',
  `extra_info` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `usuario` (`user`),
  KEY `proyecto` (`project`),
  KEY `convocatoria` (`call`),
  KEY `matcher` (`matcher`),
  KEY `datetime` (`datetime`),
  KEY `invested` (`invested`),
  CONSTRAINT `invest_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `invest_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `invest_ibfk_3` FOREIGN KEY (`call`) REFERENCES `call` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `invest_ibfk_4` FOREIGN KEY (`matcher`) REFERENCES `matcher` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Aportes monetarios a proyectos';

/*Data for the table `invest` */

insert  into `invest`(`id`,`user`,`project`,`account`,`amount`,`amount_original`,`currency`,`currency_rate`,`donate_amount`,`status`,`anonymous`,`resign`,`invested`,`charged`,`returned`,`preapproval`,`payment`,`transaction`,`method`,`admin`,`campaign`,`datetime`,`drops`,`droped`,`call`,`matcher`,`issue`,`pool`,`extra_info`) values (1,'backer-1-passing-project','project-passing-today','',200,200,'EUR',1.00000,0,1,0,1,'2020-03-05','2020-03-05',NULL,NULL,'',NULL,'dummy',NULL,0,'2020-02-09 16:50:25',NULL,NULL,NULL,NULL,0,1,NULL),(2,'backer-2-passing-project','project-passing-today','',40,40,'EUR',1.00000,0,1,0,0,'2020-03-10','2020-03-10',NULL,'',NULL,NULL,'dummy',NULL,0,'2020-01-30 16:50:25',NULL,NULL,NULL,NULL,0,0,NULL),(3,'backer-1-finishing-project','project-finishing-today','',200,200,'EUR',1.00000,0,1,0,1,'2020-02-09','2020-02-09',NULL,'727025821','1200387012150822204948007100','','dummy',NULL,0,'2020-02-09 16:50:25',NULL,NULL,NULL,NULL,0,0,NULL),(4,'backer-2-finishing-project','project-finishing-today','',200,200,'EUR',1.00000,0,1,0,0,'2020-02-04','2020-02-04',NULL,'727001105','1200386948150822192936007100','','dummy',NULL,0,'2020-02-04 16:50:25',NULL,NULL,NULL,NULL,0,1,NULL),(5,'backer-3-finishing-project','project-finishing-today','',40,40,'EUR',1.00000,0,1,0,0,'2020-01-30',NULL,NULL,'PA-7X430535Y6705613F',NULL,NULL,'dummy',NULL,0,'2020-01-30 16:50:25',NULL,NULL,NULL,NULL,0,0,NULL),(6,'backer-1-passed','project-passed','',200,200,'EUR',1.00000,0,1,0,1,'2019-11-26','2019-11-26',NULL,NULL,'',NULL,'dummy',NULL,0,'2020-02-09 16:50:26',NULL,NULL,NULL,NULL,0,1,NULL),(7,'backer-2-passed','project-passed','',200,200,'EUR',1.00000,0,1,0,1,'2019-11-26','2019-11-26',NULL,NULL,'',NULL,'dummy',NULL,0,'2020-02-09 16:50:26',NULL,NULL,NULL,NULL,0,1,NULL),(8,'backer-3-passed','project-passed','',40,40,'EUR',1.00000,0,1,0,0,'2019-12-01','2019-12-01',NULL,'',NULL,NULL,'dummy',NULL,0,'2020-01-30 16:50:26',NULL,NULL,NULL,NULL,0,0,NULL);

/*Table structure for table `invest_address` */

DROP TABLE IF EXISTS `invest_address`;

CREATE TABLE `invest_address` (
  `invest` bigint(20) unsigned NOT NULL,
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `address` tinytext CHARACTER SET utf8,
  `zipcode` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `location` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `country` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `nif` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `namedest` tinytext CHARACTER SET utf8,
  `emaildest` tinytext CHARACTER SET utf8,
  `regalo` int(1) DEFAULT '0',
  `message` text CHARACTER SET utf8,
  PRIMARY KEY (`invest`),
  KEY `user` (`user`),
  CONSTRAINT `invest_address_ibfk_1` FOREIGN KEY (`invest`) REFERENCES `invest` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `invest_address_ibfk_2` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Dirección de entrega de recompensa';

/*Data for the table `invest_address` */

/*Table structure for table `invest_detail` */

DROP TABLE IF EXISTS `invest_detail`;

CREATE TABLE `invest_detail` (
  `invest` bigint(20) unsigned NOT NULL,
  `type` varchar(30) CHARACTER SET utf8 NOT NULL,
  `log` text COLLATE utf8mb4_unicode_ci,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `invest_type` (`invest`,`type`),
  KEY `invest` (`invest`),
  CONSTRAINT `invest_detail_ibfk_1` FOREIGN KEY (`invest`) REFERENCES `invest` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Detalles de los aportes';

/*Data for the table `invest_detail` */

/*Table structure for table `invest_location` */

DROP TABLE IF EXISTS `invest_location`;

CREATE TABLE `invest_location` (
  `id` bigint(20) unsigned NOT NULL,
  `latitude` decimal(16,14) NOT NULL,
  `longitude` decimal(16,14) NOT NULL,
  `radius` smallint(6) unsigned NOT NULL DEFAULT '0',
  `method` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT 'ip',
  `locable` tinyint(1) NOT NULL DEFAULT '0',
  `city` varchar(255) CHARACTER SET utf8 NOT NULL,
  `region` varchar(255) CHARACTER SET utf8 NOT NULL,
  `country` varchar(150) CHARACTER SET utf8 NOT NULL,
  `country_code` varchar(2) CHARACTER SET utf8 NOT NULL,
  `info` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `locable` (`locable`),
  CONSTRAINT `invest_location_ibfk_1` FOREIGN KEY (`id`) REFERENCES `invest` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `invest_location` */

/*Table structure for table `invest_msg` */

DROP TABLE IF EXISTS `invest_msg`;

CREATE TABLE `invest_msg` (
  `invest` bigint(20) unsigned NOT NULL,
  `msg` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`invest`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Mensaje de apoyo al proyecto tras aportar';

/*Data for the table `invest_msg` */

/*Table structure for table `invest_node` */

DROP TABLE IF EXISTS `invest_node`;

CREATE TABLE `invest_node` (
  `user_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `user_node` varchar(50) CHARACTER SET utf8 NOT NULL,
  `project_id` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `project_node` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `invest_id` bigint(20) unsigned NOT NULL,
  `invest_node` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT 'Nodo en el que se hace el aporte',
  UNIQUE KEY `invest` (`invest_id`),
  KEY `invest_id` (`invest_id`),
  KEY `invest_node` (`invest_node`),
  KEY `project_id` (`project_id`),
  KEY `project_node` (`project_node`),
  KEY `user_id` (`user_id`),
  KEY `user_node` (`user_node`),
  CONSTRAINT `invest_node_ibfk_1` FOREIGN KEY (`user_node`) REFERENCES `node` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `invest_node_ibfk_2` FOREIGN KEY (`project_node`) REFERENCES `node` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `invest_node_ibfk_3` FOREIGN KEY (`invest_node`) REFERENCES `node` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `invest_node_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `invest_node_ibfk_5` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `invest_node_ibfk_6` FOREIGN KEY (`invest_id`) REFERENCES `invest` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Aportes por usuario/nodo a proyecto/nodo';

/*Data for the table `invest_node` */

insert  into `invest_node`(`user_id`,`user_node`,`project_id`,`project_node`,`invest_id`,`invest_node`) values ('backer-1-passing-project','goteo','project-passing-today','goteo',1,'goteo'),('backer-2-passing-project','goteo','project-passing-today','goteo',2,'goteo'),('backer-1-finishing-project','goteo','project-finishing-today','goteo',3,'goteo'),('backer-2-finishing-project','goteo','project-finishing-today','goteo',4,'goteo'),('backer-3-finishing-project','goteo','project-finishing-today','goteo',5,'goteo'),('backer-1-passed','goteo','project-passed','goteo',6,'goteo'),('backer-2-passed','goteo','project-passed','goteo',7,'goteo'),('backer-3-passed','goteo','project-passed','goteo',8,'goteo');

/*Table structure for table `invest_reward` */

DROP TABLE IF EXISTS `invest_reward`;

CREATE TABLE `invest_reward` (
  `invest` bigint(20) unsigned NOT NULL,
  `reward` bigint(20) unsigned NOT NULL,
  `fulfilled` tinyint(1) NOT NULL DEFAULT '0',
  UNIQUE KEY `invest` (`invest`,`reward`),
  KEY `reward` (`reward`),
  CONSTRAINT `invest_reward_ibfk_1` FOREIGN KEY (`invest`) REFERENCES `invest` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `invest_reward_ibfk_2` FOREIGN KEY (`reward`) REFERENCES `reward` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Recompensas elegidas al aportar';

/*Data for the table `invest_reward` */

/*Table structure for table `lang` */

DROP TABLE IF EXISTS `lang`;

CREATE TABLE `lang` (
  `id` varchar(2) CHARACTER SET utf8 NOT NULL COMMENT 'Código ISO-639',
  `name` varchar(20) CHARACTER SET utf8 NOT NULL,
  `active` int(1) NOT NULL DEFAULT '0',
  `short` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `locale` varchar(5) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Idiomas';

/*Data for the table `lang` */

/*Table structure for table `license` */

DROP TABLE IF EXISTS `license`;

CREATE TABLE `license` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `group` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'grupo de restriccion de menor a mayor',
  `url` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `order` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Licencias de distribucion';

/*Data for the table `license` */

insert  into `license`(`id`,`name`,`description`,`group`,`url`,`order`) values ('agpl','Affero General Public License','Licencia pública general de Affero para software libre que corra en servidores de red','','http://www.affero.org/oagf.html',2),('apache','Apache License','Licencia Apache de software libre, que no exige que las obras derivadas se distribuyan usando la misma licencia ni como software libre','','http://www.apache.org/licenses/LICENSE-2.0',10),('balloon','Balloon Open Hardware License','Licencia para hardware libre de los procesadores Balloon','','http://balloonboard.org/licence.html',20),('bsd','Berkeley Software Distribution','Licencia de software libre permisiva, con pocas restricciones y que permite el uso del código fuente en software no libre','open','http://es.wikipedia.org/wiki/Licencia_BSD',5),('cc0','CC0 Universal (Dominio Público)','Licencia Creative Commons de obra dedicada al dominio público, mediante renuncia a todos los derechos de autoría sobre la misma','','http://creativecommons.org/publicdomain/zero/1.0/deed.es',25),('ccby','CC - Reconocimiento','Licencia Creative Commons (bienes comunes creativos) con reconocimiento de autoría','open','http://creativecommons.org/licenses/by/4.0/deed.es_ES',12),('ccbync','CC - Reconocimiento - NoComercial','Licencia Creative Commons (bienes comunes creativos) con reconocimiento de autoría y sin que se pueda hacer uso comercial','','http://creativecommons.org/licenses/by-nc/2.0/deed.es_ES',13),('ccbyncnd','CC - Reconocimiento - NoComercial - SinObraDerivada','Licencia Creative Commons (bienes comunes creativos) con reconocimiento de autoría, sin que se pueda hacer uso comercial ni otras obras derivadas','','http://creativecommons.org/licenses/by-nc-nd/2.0/deed.es_ES',15),('ccbyncsa','CC - Reconocimiento - NoComercial - CompartirIgual','Licencia Creative Commons (bienes comunes creativos) con reconocimiento de autoría, sin que se pueda hacer uso comercial y a compartir en idénticas condiciones','','http://creativecommons.org/licenses/by-nc-sa/3.0/deed.es_ES',14),('ccbynd','CC - Reconocimiento - SinObraDerivada','Licencia Creative Commons (bienes comunes creativos) con reconocimiento de autoría, sin que se puedan hacer obras derivadas ','','http://creativecommons.org/licenses/by-nd/2.0/deed.es_ES',17),('ccbysa','CC - Reconocimiento - CompartirIgual','Licencia Creative Commons (bienes comunes creativos) con reconocimiento de autoría y a compartir en idénticas condiciones','open','http://creativecommons.org/licenses/by-sa/2.0/deed.es_ES',16),('cernohl','CERN OHL Open Hardware Licence','Licencia desarollada por el CERN - Laboratorio Europeo de Física de Partículas Elementales para poryectos de Hardware','open','http://www.ohwr.org/projects/cernohl/wiki',98),('fal','Free Art License','Licencia de arte libre','','http://artlibre.org/lal/es',99),('fdl','Free Documentation License ','Licencia de documentación libre de GNU, pudiendo ser ésta copiada, redistribuida, modificada e incluso vendida siempre y cuando se mantenga bajo los términos de esa misma licencia','open','http://www.gnu.org/copyleft/fdl.html',4),('freebsd','FreeBSD Documentation License','Licencia de documentación libre para el sistema operativo FreeBSD','open','http://www.freebsd.org/copyright/freebsd-doc-license.html',6),('gpl','General Public License','Licencia Pública General de GNU para la libre distribución, modificación y uso de software','open','http://www.gnu.org/licenses/gpl.html',1),('gpl2','General Public License (v.2)','Licencia Pública General de GNU para la libre distribución, modificación y uso de software','open','http://www.gnu.org/licenses/gpl-2.0.html',1),('lgpl','Lesser General Public License','Licencia Pública General Reducida de GNU, para software libre que puede ser utilizado por un programa no-GPL, que a su vez puede ser software libre o no','open','http://www.gnu.org/copyleft/lesser.html',3),('mit','MIT / X11 License','Licencia tanto para software libre como para software no libre, que permite no liberar los cambios realizados sobre el programa original','','http://es.wikipedia.org/wiki/MIT_License',8),('mpl','Mozilla Public License','Licencia pública de Mozilla de software libre, que posibilita la reutilización no libre del software, sin restringir la reutilización del código ni el relicenciamiento bajo la misma licencia','','http://www.mozilla.org/MPL/',7),('odbl','Open Database License ','Licencia de base de datos abierta, que permite compartir, modificar y utilizar bases de datos en idénticas condiciones','open','http://www.opendatacommons.org/licenses/odbl/',22),('odcby','Open Data Commons Attribution License','Licencia de datos abierta, que permite compartir, modificar y utilizar los datos en idénticas condiciones atribuyendo la fuente original','open','http://www.opendatacommons.org/licenses/by/',23),('oshw','TAPR Open Hardware License','Licencia para obras de hardware libre','open','http://www.tapr.org/OHL',18),('pd','Dominio público','La obra puede ser libremente reproducida, distribuida, transmitida, usada, modificada, editada u objeto de cualquier otra forma de explotación para el propósito que sea, comercial o no','','http://creativecommons.org/licenses/publicdomain/deed.es',24),('php','PHP License','Licencia bajo la que se publica el lenguaje de programación PHP','','http://www.php.net/license/',9),('tapr','TAPR Noncommercial Hardware License','Licencia para obras de hardware libre con limitación en su comercialización ','','http://www.tapr.org/NCL.html',19),('xoln','Procomún de la XOLN','Licencia de red abierta, libre y neutral, como acuerdo de interconexión entre iguales promovido por Guifi.net','open','http://guifi.net/es/ProcomunXOLN',21);

/*Table structure for table `license_lang` */

DROP TABLE IF EXISTS `license_lang`;

CREATE TABLE `license_lang` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `url` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `license_lang` */

insert  into `license_lang`(`id`,`lang`,`name`,`description`,`url`,`pending`) values ('agpl','ca','Affero General Public License','Llicència pública general d\'Affero per a programari lliure que corri en servidors de xarxa','http://www.affero.org/oagf.html',0),('agpl','el','Affero General Public License','Affero General Public License for open networked software','http://www.affero.org/oagf.html',0),('agpl','en','Affero General Public License','Affero General Public License for open networked software','http://www.affero.org/oagf.html',0),('agpl','eu','Affero General Public License',' Afferoren lizentzia publiko orokorra, sare zebitzarietan iragaten den  software libreetzako. \r\n\r\n','http://www.affero.org/oagf.html',0),('agpl','gl','Affero General Public License','Licenza pública xeral de Affero para software libre que corran en servidores de rede','http://www.affero.org/oagf.html',0),('agpl','pl','Affero General Public License','Affero General Public License for open networked software','http://www.affero.org/oagf.html',0),('apache','ca','Apache License','Llicencia Apatxe de programari lliure, que no exigeix que les obres derivades es distribueixin usant la mateixa llicència ni com a programari lliure','http://www.apache.org/licenses/LICENSE-2.0',0),('apache','el','Apache License','Apache License for open software, that does not require that derivative works be distributed with the same license, or even as open software','http://www.apache.org/licenses/LICENSE-2.0',0),('apache','en','Apache License','Apache License for open software, that does not require that derivative works be distributed with the same license, or even as open software','http://www.apache.org/licenses/LICENSE-2.0',0),('apache','eu','Apache License','Sofware libredun Apache Lizentzia, ez du eskatzen lan deribatuak lizentzia berdinarekin  edota sofware libre moduan banatzea.\r\n\r\n','http://www.apache.org/licenses/LICENSE-2.0',0),('apache','gl','Apache License','Licenza Apache de software libre, que non esixe que as obras derivadas se distribúan empregando a mesma licenza nin como software libre','http://www.apache.org/licenses/LICENSE-2.0',0),('apache','pl','Apache License','Apache License for open software, that does not require that derivative works be distributed with the same license, or even as open software','http://www.apache.org/licenses/LICENSE-2.0',0),('balloon','ca','Balloon Open Hardware License','Llicència per a maquinari lliure dels processadors Balloon','http://balloonboard.org/licence.html',0),('balloon','el','Balloon Open Hardware License','License for open Balloon boards','http://balloonboard.org/licence.html',0),('balloon','en','Balloon Open Hardware License','License for open Balloon boards','http://balloonboard.org/licence.html',0),('balloon','eu','Balloon Open Hardware License','Ballon prozesadoreen hardwadre libreen lizentzia\r\n\r\n','http://balloonboard.org/licence.html',0),('balloon','gl','Balloon Open Hardware License','Licenza para hardware libre dos procesadores Balloon','http://balloonboard.org/licence.html',0),('balloon','pl','Balloon Open Hardware License','License for open Balloon boards','http://balloonboard.org/licence.html',0),('bsd','ca','Berkeley Software Distribution','Llicència de programari lliure permissiva, amb poques restriccions i que permet l\'ús del codi font en programari no lliure','http://es.wikipedia.org/wiki/Licencia_BSD',0),('bsd','el','Berkeley Software Distribution Licenses','Permissive free software licenses, with few restrictions, that permit the use of source code in non-free software','http://en.wikipedia.org/wiki/BSD_licenses',0),('bsd','en','Berkeley Software Distribution Licenses','Permissive free software licenses, with few restrictions, that permit the use of source code in non-free software','http://en.wikipedia.org/wiki/BSD_licenses',0),('bsd','eu','Berkeley Software Distribution','Software aske permisiboaren lizentzia, murrizketa gutxirekin eta iturri kodearen erabilera baimentzen duen librea ez den sofware.\r\n\r\n','http://es.wikipedia.org/wiki/Licencia_BSD',0),('bsd','gl','Berkeley Software Distribution','Licenza de software libre permisiva, con poucas restricións e que permite o emprego do código fonte en software non libre','http://gl.wikipedia.org/wiki/Licenza_BSD',0),('bsd','pl','Berkeley Software Distribution Licenses','Permissive free software licenses, with few restrictions, that permit the use of source code in non-free software','http://en.wikipedia.org/wiki/BSD_licenses',0),('cc0','ca','CC0 Universal (Domini Públic)','Llicència Creative Commons d\'obra dedicada al domini públic, mitjançant renúncia a tots els drets d\'autoria sobre la mateixa','http://creativecommons.org/publicdomain/zero/1.0/deed.ca',0),('cc0','el','CC0 Universal (Public Domain)','Creative Commons License for works dedicated to the public domain, by which all intellectual property rights over a work are waived','http://creativecommons.org/publicdomain/zero/1.0/deed.en',0),('cc0','en','CC0 Universal (Public Domain)','Creative Commons License for works dedicated to the public domain, by which all intellectual property rights over a work are waived','http://creativecommons.org/publicdomain/zero/1.0/deed.en',0),('cc0','eu','CC0 Universal (Domeinu publikoa)','Creative Commons Lizentzia domeinu publikora eskeinia, beraren gainetik autoretza eskubideari uko egitearen bitartez\r\n\r\n','http://creativecommons.org/publicdomain/zero/1.0/deed.es',0),('cc0','gl','CC0 Universal (Dominio Público)','Licenza Creative Commons de obra adicada ó dominio público, mediante renuncia a todos os dereitos de autoría sobre a mesma','http://creativecommons.org/publicdomain/zero/1.0/deed.es',0),('cc0','pl','CC0 Universal (Public Domain)','Creative Commons License for works dedicated to the public domain, by which all intellectual property rights over a work are waived','http://creativecommons.org/publicdomain/zero/1.0/deed.en',0),('ccby','ca','CC - Reconeixement','Llicència Creative Commons (béns comuns creatius) amb reconeixement d\'autoria','http://creativecommons.org/licenses/by/2.0/deed.ca',0),('ccby','el','CC - Attribution','Creative Commons License with attribution','http://creativecommons.org/licenses/by/2.0/deed.en',0),('ccby','en','CC - Attribution','Creative Commons License with attribution','http://creativecommons.org/licenses/by/2.0/deed.en',0),('ccby','eu','CC - Onarpena ','Creative Commons Lizentzia (ondasun arrunt sortzaileak) egiletzaren onarpenarekin\r\n\r\n','http://creativecommons.org/licenses/by/2.0/deed.es_ES',0),('ccby','gl','CC - Recoñecemento','Licenza Creative Commons (bens comúns creativos) con recoñecemento de autoría','http://creativecommons.org/licenses/by/4.0/deed.es_ES',0),('ccby','pl','CC - Attribution','Creative Commons License with attribution','http://creativecommons.org/licenses/by/2.0/deed.en',0),('ccbync','ca','CC - Reconeixement - NoComercial','Llicència Creative Commons (béns comuns creatius) amb reconeixement d\'autoria i sense que es pugui fer ús comercial','http://creativecommons.org/licenses/by-nc/2.0/deed.ca',0),('ccbync','el','CC - Attribution-NonCommercial','Creative Commons License with attribution that does not permit commercial use','http://creativecommons.org/licenses/by-nc/2.0/deed.en',0),('ccbync','en','CC - Attribution-NonCommercial','Creative Commons License with attribution that does not permit commercial use','http://creativecommons.org/licenses/by-nc/2.0/deed.en',0),('ccbync','eu','CC - Onarpena - EzKomertziala','Creative Coomons Lizentzia (ondasun arrunt sortzaileak) egiletzaren onarpenarekin eta ezin daitekeena erabilera komertzialerako erabili\r\n\r\n','http://creativecommons.org/licenses/by-nc/2.0/deed.es_ES',0),('ccbync','gl','CC - Recoñecemento - NonComercial','Licenza Creative Commons (bens comúns creativos) con recoñecemento de autoría e sen que se poida facer uso comercial','http://creativecommons.org/licenses/by-nc/2.0/deed.es_ES',0),('ccbync','pl','CC - Attribution-NonCommercial','Creative Commons License with attribution that does not permit commercial use','http://creativecommons.org/licenses/by-nc/2.0/deed.en',0),('ccbyncnd','ca','CC - Reconeixement - NoComercial - SenseObraDerivada','Llicència Creative Commons (béns comuns creatius) amb reconeixement d\'autoria, sense que es pugui fer ús comercial ni altres obres derivades','http://creativecommons.org/licenses/by-nc-nd/2.0/deed.ca',0),('ccbyncnd','el','CC - Attribution  - NonCommercial - NoDerivs','Creative Commons License with attribution, that does not allow commercial use nor derivative works','http://creativecommons.org/licenses/by-nc-nd/2.0/deed.en',0),('ccbyncnd','en','CC - Attribution  - NonCommercial - NoDerivs','Creative Commons License with attribution, that does not allow commercial use nor derivative works','http://creativecommons.org/licenses/by-nc-nd/2.0/deed.en',0),('ccbyncnd','eu','CC - Onarpena - EzKomertziala - LanDeribatuGabea','Creative Commons Lizentzia (ondasun arrunt sortzaileak) egiletzaren onarpenarekin, ezin daitekeena erabilera komertzialetarako erabili ezta beste lan deribatuetarako ere\r\n\r\n','http://creativecommons.org/licenses/by-nc-nd/2.0/deed.es_ES',0),('ccbyncnd','gl','CC - Recoñecemento - NonComercial - SenObraDerivada','Licenza Creative Commons (bens comúns creativos) con recoñecemento de autoría, sen que se poida facer uso comercial nin outras obras derivadas','http://creativecommons.org/licenses/by-nc-nd/2.0/deed.es_ES',0),('ccbyncnd','pl','CC - Attribution  - NonCommercial - NoDerivs','Creative Commons License with attribution, that does not allow commercial use nor derivative works','http://creativecommons.org/licenses/by-nc-nd/2.0/deed.en',0),('ccbyncsa','ca','CC - Reconeixement - NoComercial - CompartirIgual','Llicència Creative Commons (béns comuns creatius) amb reconeixement d\'autoria, sense que es pugui fer ús comercial i a compartir en idèntiques condicions','http://creativecommons.org/licenses/by-nc-sa/3.0/deed.ca',0),('ccbyncsa','el','CC - Attribution - NonCommercial - ShareAlike','Creative Commons License with attribution, that does not allow commercial use, and only allows sharing under identical licensing conditions','http://creativecommons.org/licenses/by-nc-sa/3.0/deed.en',0),('ccbyncsa','en','CC - Attribution - NonCommercial - ShareAlike','Creative Commons License with attribution, that does not allow commercial use, and only allows sharing under identical licensing conditions','http://creativecommons.org/licenses/by-nc-sa/3.0/deed.en',0),('ccbyncsa','eu','CC - Onarpena - EzKomertziala - BerdinPartekatua','Creative Commons Lizentzia (ondasun arrunt sortzaileak) egiletzaren onarpenarekin, ezin daitekeena erabilera komertzialerako erabili eta baldintza berdinetan partekatua','http://creativecommons.org/licenses/by-nc-sa/3.0/deed.es_ES',0),('ccbyncsa','gl','CC - Recoñecemento - NonComercial - PartillarIgual','Licenza Creative Commons (bens comúns creativos) con recoñecemento de autoría, sen que se poida facer uso comercial e a partillar en idénticas condicións','http://creativecommons.org/licenses/by-nc-sa/3.0/deed.es_ES',0),('ccbyncsa','pl','CC - Attribution - NonCommercial - ShareAlike','Creative Commons License with attribution, that does not allow commercial use, and only allows sharing under identical licensing conditions','http://creativecommons.org/licenses/by-nc-sa/3.0/deed.en',0),('ccbynd','ca','CC - Reconeixement - SenseObraDerivada','Llicència Creative Commons (béns comuns creatius) amb reconeixement d\'autoria, sense que s\'en puguin fer obres derivades ','http://creativecommons.org/licenses/by-nd/2.0/deed.ca',0),('ccbynd','el','CC - Attribution - NoDerivs','Creative Commons License with attribution that does not allow derivative works','http://creativecommons.org/licenses/by-nd/2.0/deed.en',0),('ccbynd','en','CC - Attribution - NoDerivs','Creative Commons License with attribution that does not allow derivative works','http://creativecommons.org/licenses/by-nd/2.0/deed.en',0),('ccbynd','eu','CC - Onarpena - LanDeribatuGabea','Creative Commons lizentzia (ondasun arrunt sortzaileak) egiletzaren onarpenarekin, ezin daitekeena lan deribaturik egin\r\n','http://creativecommons.org/licenses/by-nd/2.0/deed.es_ES',0),('ccbynd','gl','CC - Recoñecemento - SenObraDerivada','Licenza Creative Commons (bens comúns creativos) con recoñecemento de autoría, sen que se poidan facer obras derivadas ','http://creativecommons.org/licenses/by-nd/2.0/deed.es_ES',0),('ccbynd','pl','CC - Attribution - NoDerivs','Creative Commons License with attribution that does not allow derivative works','http://creativecommons.org/licenses/by-nd/2.0/deed.en',0),('ccbysa','ca','CC - Reconeixement - CompartirIgual','Llicència Creative Commons (béns comuns creatius) amb reconeixement d\'autoria i a compartir en idèntiques condicions','http://creativecommons.org/licenses/by-sa/2.0/deed.ca',0),('ccbysa','el','CC - Attribution - ShareAlike','Creative Commons License with attribution that only allows sharing under identical licensing conditions','http://creativecommons.org/licenses/by-sa/2.0/deed.en',0),('ccbysa','en','CC - Attribution - ShareAlike','Creative Commons License with attribution that only allows sharing under identical licensing conditions','http://creativecommons.org/licenses/by-sa/2.0/deed.en',0),('ccbysa','eu','CC - Onarpena - BerdinPartekatua','Creative Commons Lizentzia (ondasun arrunt sortzailea) egiletzaren onarpenarekin eta baldintza berdinetan partekatua\r\n\r\n','http://creativecommons.org/licenses/by-sa/2.0/deed.es_ES',0),('ccbysa','gl','CC - Recoñecemento - PartillarIgual','Licenza Creative Commons (bens comúns creativos) con recoñecemento de autoría e ó partillar en idénticas condicións','http://creativecommons.org/licenses/by-sa/2.0/deed.es_ES',0),('ccbysa','pl','CC - Attribution - ShareAlike','Creative Commons License with attribution that only allows sharing under identical licensing conditions','http://creativecommons.org/licenses/by-sa/2.0/deed.en',0),('cernohl','ca','CERN OHL Open Hardware Licence','Llicència desenvolupada pel CERN - Laboratori Europeu de Física de Partícules Elementals per a projectes de Hardware','http://www.ohwr.org/projects/cernohl/wiki',0),('cernohl','en','CERN OHL Open Hardware Licence','Licenza sviluppata dal CERN - Laboratorio Europeo di Fisica della Particelle Elementari per progetti di Hardware','http://www.ohwr.org/projects/cernohl/wiki',0),('cernohl','gl','CERN OHL Open Hardware Licence','Licenza desenrolada polo CERN - Laboratorio Europeo de Física de Partículas Elementais para proxectos de Hardware','http://www.ohwr.org/projects/cernohl/wiki',0),('fal','ca','Free Art License','Llicència d\'art lliure','http://artlibre.org/licence/lal/es',0),('fal','el','Free Art License','Free art license','http://artlibre.org/licence/lal/en',0),('fal','en','Free Art License','Free art license','http://artlibre.org/licence/lal/en',0),('fal','eu','Free Art License','Arte librerako Lizentzia\r\n','http://artlibre.org/licence/lal/es',0),('fal','gl','Free Art License','Licenza de arte libre','http://artlibre.org/licence/lal/es',0),('fal','pl','Free Art License','Free art license','http://artlibre.org/licence/lal/en',0),('fdl','ca','Free Documentation License ','Llicència de documentació lliure de GNU, podent ser aquesta copiada, redistribuïda, modificada i fins i tot venuda sempre que es mantingui sota els termes d\'aquesta mateixa llicència','http://www.gnu.org/copyleft/fdl.html',0),('fdl','el','Free Documentation License ','GNU free documentation license, which can be copied, redistributed, modified and even sold, as long as the original terms of this same license are maintained.','http://www.gnu.org/copyleft/fdl.html',0),('fdl','en','Free Documentation License ','GNU free documentation license, which can be copied, redistributed, modified and even sold, as long as the original terms of this same license are maintained.','http://www.gnu.org/copyleft/fdl.html',0),('fdl','eu','Free Documentation License ','GNUren dokumentazio librerako lizentzia. Hau, kopiatua, birbanatua, eraldatua eta baita ere saldua izan daiteke beti ere lizentzia horren balditzetan oinarritzen bada\r\n','http://www.gnu.org/copyleft/fdl.html',0),('fdl','gl','Free Documentation License ','Licenza de documentación libre de GNU, podendo ser ésta copiada, redistribuída, modificada e incluso vendida sempre e cando se manteña baixo os térmos desa mesma licenza','http://www.gnu.org/copyleft/fdl.html',0),('fdl','pl','Free Documentation License ','GNU free documentation license, which can be copied, redistributed, modified and even sold, as long as the original terms of this same license are maintained.','http://www.gnu.org/copyleft/fdl.html',0),('freebsd','ca','FreeBSD Documentation License','Llicència de documentació lliure per al sistema operatiu FreeBSD','http://www.freebsd.org/copyright/freebsd-doc-license.html',0),('freebsd','el','FreeBSD Documentation License','Free Documentation License for the FreeBSD operating system','http://www.freebsd.org/copyright/freebsd-doc-license.html',0),('freebsd','en','FreeBSD Documentation License','Free Documentation License for the FreeBSD operating system','http://www.freebsd.org/copyright/freebsd-doc-license.html',0),('freebsd','eu','FreeBSD Documentation License','Dokumentazio libreko FreeBSD sistema eragilearentzako lizentzia\r\n\r\n','http://www.freebsd.org/copyright/freebsd-doc-license.html',0),('freebsd','gl','FreeBSD Documentation License','Licenza de documentación libre para o sistema operativo FreeBSD','http://www.freebsd.org/copyright/freebsd-doc-license.html',0),('freebsd','pl','FreeBSD Documentation License','Free Documentation License for the FreeBSD operating system','http://www.freebsd.org/copyright/freebsd-doc-license.html',0),('gpl','ca','General Public License','Llicència Pública General de GNU per a la lliure distribució, modificació i ús de programari','http://www.gnu.org/licenses/gpl.html',0),('gpl','el','General Public License','GNU General Public License for the free distribution, modification, and use of software','http://www.gnu.org/licenses/gpl.html',0),('gpl','en','General Public License','GNU General Public License for the free distribution, modification, and use of software','http://www.gnu.org/licenses/gpl.html',0),('gpl','eu','General Public License','GNUren Lizentzia Publiko Orokorra, sofware-aren banaketa, aldaketa eta erabilera libre baterako\r\n\r\n','http://www.gnu.org/licenses/gpl.html',0),('gpl','gl','General Public License','Licenza Pública Xeral de GNU para a libre distribución, modificación e uso de software','http://www.gnu.org/licenses/gpl.html',0),('gpl','pl','General Public License','GNU General Public License for the free distribution, modification, and use of software','http://www.gnu.org/licenses/gpl.html',0),('gpl2','ca','General Public License (v.2)','Llicència Pública General de GNU per a la lliure distribució, modificació i ús de programari','http://www.gnu.org/licenses/gpl-2.0.html',0),('gpl2','el','General Public License (v.2)','GNU General Public License for the free distribution, modification, and use of software','http://www.gnu.org/licenses/gpl-2.0.html',0),('gpl2','en','General Public License (v.2)','GNU General Public License for the free distribution, modification, and use of software','http://www.gnu.org/licenses/gpl-2.0.html',0),('gpl2','eu','General Public License (v.2)','GNUren Litzentzia Publico Orokorra, banaketa, aldakera eta sofwarearen erabilera libre baterako \r\n\r\n','http://www.gnu.org/licenses/gpl-2.0.html',0),('gpl2','gl','General Public License (v.2)','Licenza Pública General de GNU para a libre distribución, modificación e uso de software','http://www.gnu.org/licenses/gpl-2.0.html',0),('gpl2','pl','General Public License (v.2)','GNU General Public License for the free distribution, modification, and use of software','http://www.gnu.org/licenses/gpl-2.0.html',0),('lgpl','ca','Lesser General Public License','Llicència Pública General Reduïda de GNU, per a programari lliure que pot ser utilitzat per un programa no-GPL, que al seu torn pot ser programari lliure o no','http://www.gnu.org/copyleft/lesser.html',0),('lgpl','el','Lesser General Public License','GNU Lesser General Public License for free software that can be used by a non-GPL program, which in turn can be free software or not. ','http://www.gnu.org/copyleft/lesser.html',0),('lgpl','en','Lesser General Public License','GNU Lesser General Public License for free software that can be used by a non-GPL program, which in turn can be free software or not. ','http://www.gnu.org/copyleft/lesser.html',0),('lgpl','eu','Lesser General Public License','GNUren Lizentzia Publiko Orokorra, no-GPL programa erabili dezakeen software libre baterako, baina honekin batera softwarea librea izan daiteke edo ez\r\n\r\n','http://www.gnu.org/copyleft/lesser.html',0),('lgpl','gl','Lesser General Public License','Licenza Pública Xeral Reducida de GNU, para software libre que pode ser empregado por un programa non-GPL, que á súa vez pode ser software libre ou non','http://www.gnu.org/copyleft/lesser.html',0),('lgpl','pl','Lesser General Public License','GNU Lesser General Public License for free software that can be used by a non-GPL program, which in turn can be free software or not. ','http://www.gnu.org/copyleft/lesser.html',0),('mit','ca','MIT / X11 License','Llicència tant per a programari lliure com per a programari no lliure, que permet no alliberar els canvis realitzats sobre el programa original','http://ca.wikipedia.org/wiki/Llic%C3%A8ncia_X11',0),('mit','el','MIT / X11 License','License both for open and closed software, that allows changes made to the original program to be protected','http://es.wikipedia.org/wiki/MIT_License',0),('mit','en','MIT / X11 License','License both for open and closed software, that allows changes made to the original program to be protected','http://es.wikipedia.org/wiki/MIT_License',0),('mit','eu','MIT / X11 License','Software libreentzako  zein librea ez denarentzako lizentzia, jatorrizko programan egon diren aldaketak ez askatzea onartzen duena\r\n','http://es.wikipedia.org/wiki/MIT_License',0),('mit','gl','MIT / X11 License','Licenza tanto para software libre coma para software non libre, que permite non liberar os cambios feitos sobre o programa orixinal','http://es.wikipedia.org/wiki/MIT_License',0),('mit','pl','MIT / X11 License','License both for open and closed software, that allows changes made to the original program to be protected','http://es.wikipedia.org/wiki/MIT_License',0),('mpl','ca','Mozilla Public License','Llicència pública de Mozilla de programari lliure, que possibilita la reutilització no lliure del programari, sense restringir-ne la reutilització del codi ni el rellicenciament sota la mateixa llicència','http://www.mozilla.org/MPL/',0),('mpl','el','Mozilla Public License','Mozilla Public License for open software that makes possible the non-open reuse of software, without restricting the reuse of the code or the relicensing under the same license. ','http://www.mozilla.org/MPL/',0),('mpl','en','Mozilla Public License','Mozilla Public License for open software that makes possible the non-open reuse of software, without restricting the reuse of the code or the relicensing under the same license. ','http://www.mozilla.org/MPL/',0),('mpl','eu','Mozilla Public License','Mozilla software librearen Lizentzia publikoa, softwarearen erabilera ez librea ahalbidetzen duena eta  kodearen bererabilera baita lizentzia berdinaren barruan birlizentziamentua ez duena murrizten\r\n','http://www.mozilla.org/MPL/',0),('mpl','gl','Mozilla Public License','Licenza pública de Mozilla de software libre, que posibilita a reutilización non libre do software, sen restrinxir a reutilización do código nin o relicenzamento baixo a mesma licenza','http://www.mozilla.org/MPL/',0),('mpl','pl','Mozilla Public License','Mozilla Public License for open software that makes possible the non-open reuse of software, without restricting the reuse of the code or the relicensing under the same license. ','http://www.mozilla.org/MPL/',0),('odbl','ca','Open Database License ','Llicència de base de dades oberta, que permet compartir, modificar i utilitzar bases de dades en idèntiques condicions','http://www.opendatacommons.org/licenses/odbl/',0),('odbl','el','Open Database License ','Open Database License that allows for sharing, modifying, and using databases in identical conditions','http://www.opendatacommons.org/licenses/odbl/',0),('odbl','en','Open Database License ','Open Database License that allows for sharing, modifying, and using databases in identical conditions','http://www.opendatacommons.org/licenses/odbl/',0),('odbl','eu','Open Database License ','Datu-base irekiaren Lizentzia, banatzea, aldatzea eta baldintza berdinetan erabili ahal diren base-datuak  baimentzen dituena\r\n\r\n','http://www.opendatacommons.org/licenses/odbl/',0),('odbl','gl','Open Database License ','Licenza de base de datos aberta, que permite partillar, modificar e empregar bases de datos en idénticas condicións','http://www.opendatacommons.org/licenses/odbl/',0),('odbl','it','Open Database License ','Licenza di dati aperta che permette condividere, modificare e utilizzare base di dati con le stesse condizioni ','http://www.opendatacommons.org/licenses/odbl/',0),('odbl','pl','Open Database License ','Open Database License that allows for sharing, modifying, and using databases in identical conditions','http://www.opendatacommons.org/licenses/odbl/',0),('odcby','ca','Open Data Commons Attribution License','Llicència de dades oberta, que permet compartir, modificar i utilitzar les dades en idèntiques condicions atribuint-hi la font original','http://www.opendatacommons.org/licenses/by/',0),('odcby','el','Open Data Commons Attribution License','Open data license that allows for sharing, modifying and using data under identical conditions, as long as attribution is given for the original source','http://www.opendatacommons.org/licenses/by/',0),('odcby','en','Open Data Commons Attribution License','Open data license that allows for sharing, modifying and using data under identical conditions, as long as attribution is given for the original source','http://www.opendatacommons.org/licenses/by/',0),('odcby','eu','Open Data Commons Attribution License','Datu irekien Lizentzia, banatzea, aldatzen eta datuak baldintza berdinetan erabiliz  jatorrizko iturritik egotziz baimentzen duena\r\n\r\n','http://www.opendatacommons.org/licenses/by/',0),('odcby','gl','Open Data Commons Attribution License','Licenza de datos aberta, que permite partillar, modificar e empregar os datos en idénticas condicións atribuíndo a fonte orixinal','http://www.opendatacommons.org/licenses/by/',0),('odcby','it','Open Data Commons Attribution License','Licenza di dati aperta che permette condividere, modificare e utilizzare i dati nelle stesse condizioni con l\'attribuzione della source originale ','http://www.opendatacommons.org/licenses/by/',0),('odcby','pl','Open Data Commons Attribution License','Open data license that allows for sharing, modifying and using data under identical conditions, as long as attribution is given for the original source','http://www.opendatacommons.org/licenses/by/',0),('oshw','ca','Open Hardware License','Llicència per a obres de maquinari lliure','http://www.tapr.org/OHL',0),('oshw','el','Open Hardware License','Open Hardware License','http://www.tapr.org/OHL',0),('oshw','en','TAPR Open Hardware License','TAPR Open Hardware License','http://www.tapr.org/OHL',0),('oshw','eu','Open Hardware License','Hardware libre dun lanentzako Lizentzia \r\n\r\n','http://www.tapr.org/OHL',0),('oshw','gl','TAPR Open Hardware License','Licenza para obras de hardware libre','http://www.tapr.org/OHL',0),('oshw','it','TAPR Open Hardware License','Licenza per opera di hardware libero','http://www.tapr.org/OHL',0),('oshw','pl','Open Hardware License','Open Hardware License','http://www.tapr.org/OHL',0),('pd','ca','Domini públic','L\'obra pot ser lliurement reproduïda, distribuïda, transmesa, usada, modificada, editada o objecte de qualsevol altra forma d\'explotació per al propòsit que sigui, comercial o no','http://creativecommons.org/licenses/publicdomain/deed.ca',0),('pd','el','Public Domain','The work may be freely reproduced, distributed, transmitted, used, modified, edited, or subject to any other form of exploitation for any commerical or non-commercial use.','http://creativecommons.org/licenses/publicdomain/deed.en',0),('pd','en','Public Domain','The work may be freely reproduced, distributed, transmitted, used, modified, edited, or subject to any other form of exploitation for any commerical or non-commercial use.','http://creativecommons.org/licenses/publicdomain/deed.en',0),('pd','eu','Eremu Publikoa','Lana libreki errepikatua, banatua, igorria, erabilia, eraldatua, argitaratua edo beste edozein explotaziorako objetu bezala izan daiteke edozein helbururekin  komertziala izan zein ez izan\r\n\r\n','http://creativecommons.org/licenses/publicdomain/deed.es',0),('pd','gl','Dominio público','A obra pode ser libremente reproducida, distribuída, transmitida, empregada, modificada, editada ou obxecto de calqueira outra forma de explotación para o propósito que sexa, comercial ou non','http://creativecommons.org/licenses/publicdomain/deed.es',0),('pd','it','Dominio pubblico','L\'opera può essere liberamene prodotta, distribuita, trasmessa, usata, modificata, cosí come oggetto di qualsiasi tipo di utilizzo per qualsiasi finalità commerciale o no ','http://creativecommons.org/licenses/publicdomain/deed.es',0),('pd','pl','Public Domain','The work may be freely reproduced, distributed, transmitted, used, modified, edited, or subject to any other form of exploitation for any commerical or non-commercial use.','http://creativecommons.org/licenses/publicdomain/deed.en',0),('php','ca','PHP License','Llicència sota la que es publica el llenguatge de programació PHP','http://www.php.net/license/',0),('php','el','PHP License','License under which the PHP programming language is published','http://www.php.net/license/',0),('php','en','PHP License','License under which the PHP programming language is published','http://www.php.net/license/',0),('php','eu','PHP License','PHP hizkuntza programazioaren pean argitaratu den Lizentzia\r\n\r\n','http://www.php.net/license/',0),('php','gl','PHP License','Licenza baixo a que se publica a linguaxe de programación PHP','http://www.php.net/license/',0),('php','it','PHP License','Licenza con cui si pubblica il linguaggio di programmazione PHP','http://www.php.net/license/',0),('php','pl','PHP License','License under which the PHP programming language is published','http://www.php.net/license/',0),('tapr','ca','TAPR Noncommercial Hardware License','Llicència per a obres de maquinari lliure amb limitació en la seva comercialització ','http://www.tapr.org/NCL.html',0),('tapr','el','TAPR Noncommercial Hardware License','TAPR Noncommercial Hardware License','http://www.tapr.org/NCL.html',0),('tapr','en','TAPR Noncommercial Hardware License','TAPR Noncommercial Hardware License','http://www.tapr.org/NCL.html',0),('tapr','eu','TAPR Noncommercial Hardware License','Bere komentzializaziorako limitazioak dituen hardwar libreko obrentzako lizentzia\r\n\r\n','http://www.tapr.org/NCL.html',0),('tapr','gl','TAPR Noncommercial Hardware License','Licenza para obras de hardware libre con limitación na súa comercialización ','http://www.tapr.org/NCL.html',0),('tapr','it','TAPR Noncommercial Hardware License','Licenza per opere con hardware libero con limitazioni alla sua commercializzazione ','http://www.tapr.org/NCL.html',0),('tapr','pl','TAPR Noncommercial Hardware License','TAPR Noncommercial Hardware License','http://www.tapr.org/NCL.html',0),('xoln','ca','Procomú de la XOLN','Llicència de xarxa oberta, lliure i neutral, com a acord d\'interconnexió entre iguals promogut per Guifi.net','http://guifi.net/es/ProcomunXOLN',0),('xoln','el','XOLN Common Good License','License for an open, free, neutral network, as an agreement of interconnection among equals, promoted by Guifi.net ','http://guifi.net/es/ProcomunXOLN',0),('xoln','en','XOLN Common Good License','License for an open, free, neutral network, as an agreement of interconnection among equals, promoted by Guifi.net ','http://guifi.net/es/ProcomunXOLN',0),('xoln','eu','Procomún de la XOLN','Sare irekiaren Lizentzia, libre eta neutrala, berdinen arteko elkar-lotzea Guifi.net-ek sustatutako akordioa bezala\r\n\r\n','http://guifi.net/es/ProcomunXOLN',0),('xoln','gl','Procomún da XOLN','Licenza de rede aberta, libre e neutral, coma acordo de interconexión entre iguais promovido por Guifi.net','http://guifi.net/es/ProcomunXOLN',0),('xoln','it','Common della XOLN','Licenza di rete aperta, libera e neutrale, dall\'accordo di connessioni tra uguali promosso da Guifi.net','http://guifi.net/es/ProcomunXOLN',0),('xoln','pl','XOLN Common Good License','License for an open, free, neutral network, as an agreement of interconnection among equals, promoted by Guifi.net ','http://guifi.net/es/ProcomunXOLN',0);

/*Table structure for table `log` */

DROP TABLE IF EXISTS `log`;

CREATE TABLE `log` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `scope` varchar(50) CHARACTER SET utf8 NOT NULL,
  `user_id` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `target_type` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'tipo de objetivo',
  `target_id` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'registro objetivo',
  `text` text COLLATE utf8mb4_unicode_ci,
  `url` tinytext CHARACTER SET utf8,
  `datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `scope` (`scope`),
  KEY `target_id` (`target_id`),
  KEY `target_type` (`target_type`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Log de cosas';

/*Data for the table `log` */

/*Table structure for table `mail` */

DROP TABLE IF EXISTS `mail`;

CREATE TABLE `mail` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `email` char(255) NOT NULL,
  `subject` char(255) DEFAULT NULL,
  `content` longtext NOT NULL,
  `template` varchar(100) DEFAULT NULL,
  `node` varchar(50) DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lang` varchar(2) DEFAULT NULL COMMENT 'Idioma en el que se solicitó la plantilla',
  `sent` tinyint(4) DEFAULT NULL,
  `error` tinytext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`,`email`),
  KEY `email` (`email`),
  KEY `node` (`node`),
  KEY `template` (`template`),
  CONSTRAINT `mail_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mail_ibfk_2` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Contenido enviado por email para el -si no ves-';

/*Data for the table `mail` */

/*Table structure for table `mail_stats` */

DROP TABLE IF EXISTS `mail_stats`;

CREATE TABLE `mail_stats` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `mail_id` bigint(20) unsigned NOT NULL,
  `email` char(150) NOT NULL,
  `metric_id` bigint(20) unsigned NOT NULL,
  `counter` int(10) unsigned NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`,`mail_id`,`email`,`metric_id`),
  KEY `email` (`email`),
  KEY `metric` (`metric_id`),
  KEY `mail_id` (`mail_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `mail_stats` */

/*Table structure for table `mail_stats_location` */

DROP TABLE IF EXISTS `mail_stats_location`;

CREATE TABLE `mail_stats_location` (
  `id` bigint(20) unsigned NOT NULL,
  `latitude` decimal(16,14) NOT NULL,
  `longitude` decimal(16,14) NOT NULL,
  `radius` smallint(6) unsigned NOT NULL DEFAULT '0',
  `method` varchar(50) NOT NULL DEFAULT 'ip',
  `locable` tinyint(1) NOT NULL DEFAULT '0',
  `city` varchar(255) NOT NULL,
  `region` varchar(255) NOT NULL,
  `country` varchar(150) NOT NULL,
  `country_code` varchar(2) NOT NULL,
  `info` varchar(255) DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `locable` (`locable`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `mail_stats_location` */

/*Table structure for table `mailer_content` */

DROP TABLE IF EXISTS `mailer_content`;

CREATE TABLE `mailer_content` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `active` int(1) NOT NULL DEFAULT '1',
  `mail` bigint(20) unsigned NOT NULL,
  `datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `blocked` int(1) DEFAULT NULL,
  `reply` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Email remitente',
  `reply_name` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `mail` (`mail`),
  CONSTRAINT `mailer_content_ibfk_1` FOREIGN KEY (`mail`) REFERENCES `mail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Contenido a enviar';

/*Data for the table `mailer_content` */

/*Table structure for table `mailer_control` */

DROP TABLE IF EXISTS `mailer_control`;

CREATE TABLE `mailer_control` (
  `email` char(150) CHARACTER SET utf8 NOT NULL,
  `bounces` int(10) unsigned NOT NULL,
  `complaints` int(10) unsigned NOT NULL,
  `action` enum('allow','deny') CHARACTER SET utf8 DEFAULT 'allow',
  `last_reason` char(255) CHARACTER SET utf8 DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Lista negra para bounces y complaints';

/*Data for the table `mailer_control` */

/*Table structure for table `mailer_limit` */

DROP TABLE IF EXISTS `mailer_limit`;

CREATE TABLE `mailer_limit` (
  `hora` time NOT NULL COMMENT 'Hora envio',
  `num` int(5) unsigned NOT NULL DEFAULT '0' COMMENT 'Cuantos',
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`hora`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Para limitar el número de envios diarios';

/*Data for the table `mailer_limit` */

/*Table structure for table `mailer_send` */

DROP TABLE IF EXISTS `mailer_send`;

CREATE TABLE `mailer_send` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `mailing` int(20) unsigned NOT NULL COMMENT 'Id de mailer_content',
  `user` varchar(50) NOT NULL,
  `email` varchar(256) NOT NULL,
  `name` varchar(100) NOT NULL,
  `datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `sent` int(1) DEFAULT NULL,
  `error` text,
  `blocked` int(1) DEFAULT NULL,
  UNIQUE KEY `id` (`id`),
  KEY `mailing` (`mailing`),
  CONSTRAINT `mailer_send_ibfk_1` FOREIGN KEY (`mailing`) REFERENCES `mailer_content` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Destinatarios pendientes y realizados';

/*Data for the table `mailer_send` */

/*Table structure for table `matcher` */

DROP TABLE IF EXISTS `matcher`;

CREATE TABLE `matcher` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT 'open',
  `logo` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `lang` varchar(2) CHARACTER SET utf8 NOT NULL,
  `owner` varchar(50) CHARACTER SET utf8 NOT NULL,
  `terms` longtext COLLATE utf8mb4_unicode_ci,
  `fee` int(2) unsigned NOT NULL DEFAULT '0',
  `processor` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT 'ID for the MatcherProcessor that handles the logic of this matcher',
  `vars` text COLLATE utf8mb4_unicode_ci,
  `amount` int(10) unsigned NOT NULL DEFAULT '0',
  `used` int(10) unsigned NOT NULL DEFAULT '0',
  `crowd` int(10) unsigned NOT NULL DEFAULT '0',
  `projects` int(10) unsigned NOT NULL DEFAULT '0',
  `matcher_location` char(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `created` date DEFAULT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `owner` (`owner`),
  CONSTRAINT `matcher_ibfk_1` FOREIGN KEY (`owner`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `matcher` */

/*Table structure for table `matcher_lang` */

DROP TABLE IF EXISTS `matcher_lang`;

CREATE TABLE `matcher_lang` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `terms` longtext COLLATE utf8mb4_unicode_ci,
  UNIQUE KEY `id` (`id`,`lang`),
  CONSTRAINT `matcher_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `matcher` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `matcher_lang` */

/*Table structure for table `matcher_location` */

DROP TABLE IF EXISTS `matcher_location`;

CREATE TABLE `matcher_location` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `latitude` decimal(16,14) NOT NULL,
  `longitude` decimal(16,14) NOT NULL,
  `radius` smallint(6) unsigned NOT NULL DEFAULT '0',
  `method` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT 'ip',
  `locable` tinyint(1) NOT NULL DEFAULT '0',
  `city` varchar(255) CHARACTER SET utf8 NOT NULL,
  `region` varchar(255) CHARACTER SET utf8 NOT NULL,
  `country` varchar(150) CHARACTER SET utf8 NOT NULL,
  `country_code` varchar(2) CHARACTER SET utf8 NOT NULL,
  `info` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  CONSTRAINT `matcher_location_ibfk_1` FOREIGN KEY (`id`) REFERENCES `matcher` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `matcher_location` */

/*Table structure for table `matcher_project` */

DROP TABLE IF EXISTS `matcher_project`;

CREATE TABLE `matcher_project` (
  `matcher_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `project_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `status` varchar(10) CHARACTER SET utf8 NOT NULL DEFAULT 'pending' COMMENT 'pending, accepted, active (funding ok), rejected (discarded by user), discarded (by admin)',
  `score` int(3) DEFAULT '0',
  PRIMARY KEY (`matcher_id`,`project_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `matcher_project_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `matcher_project_ibfk_2` FOREIGN KEY (`matcher_id`) REFERENCES `matcher` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `matcher_project` */

/*Table structure for table `matcher_sphere` */

DROP TABLE IF EXISTS `matcher_sphere`;

CREATE TABLE `matcher_sphere` (
  `matcher_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `sphere_id` bigint(20) unsigned NOT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`matcher_id`,`sphere_id`),
  KEY `sphere_id` (`sphere_id`),
  CONSTRAINT `matcher_sphere_ibfk_1` FOREIGN KEY (`matcher_id`) REFERENCES `matcher` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `matcher_sphere_ibfk_2` FOREIGN KEY (`sphere_id`) REFERENCES `sphere` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `matcher_sphere` */

/*Table structure for table `matcher_user` */

DROP TABLE IF EXISTS `matcher_user`;

CREATE TABLE `matcher_user` (
  `matcher_id` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT 'Matcher campaign',
  `user_id` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT 'User owner',
  `pool` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'Use owner''s pool as funding source',
  `admin` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'If the user is admin',
  PRIMARY KEY (`matcher_id`,`user_id`),
  KEY `matcher_user_ibfk_1` (`user_id`),
  CONSTRAINT `matcher_user_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `matcher_user_ibfk_2` FOREIGN KEY (`matcher_id`) REFERENCES `matcher` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `matcher_user` */

/*Table structure for table `message` */

DROP TABLE IF EXISTS `message`;

CREATE TABLE `message` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `thread` bigint(20) unsigned DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `message` text COLLATE utf8mb4_unicode_ci,
  `blocked` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'No se puede modificar ni borrar',
  `closed` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'No se puede responder',
  `private` tinyint(1) NOT NULL DEFAULT '0',
  `shared` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `project` (`project`),
  KEY `thread` (`thread`),
  KEY `user` (`user`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`thread`) REFERENCES `message` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `message_ibfk_2` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `message_ibfk_3` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Mensajes de usuarios en proyecto';

/*Data for the table `message` */

insert  into `message`(`id`,`user`,`project`,`thread`,`date`,`message`,`blocked`,`closed`,`private`,`shared`) values (1,'owner-project-passing','project-passing-today',NULL,'2020-04-09 16:50:25','Test message',0,0,0,0),(2,'owner-project-passing','project-passed',NULL,'2020-04-09 16:50:26','Test message',0,0,0,0);

/*Table structure for table `message_lang` */

DROP TABLE IF EXISTS `message_lang`;

CREATE TABLE `message_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `message_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `message` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `message_lang` */

/*Table structure for table `message_user` */

DROP TABLE IF EXISTS `message_user`;

CREATE TABLE `message_user` (
  `message_id` bigint(20) unsigned NOT NULL,
  `user_id` char(50) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`message_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `message_user_ibfk_1` FOREIGN KEY (`message_id`) REFERENCES `message` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `message_user_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `message_user` */

/*Table structure for table `metric` */

DROP TABLE IF EXISTS `metric`;

CREATE TABLE `metric` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `metric` char(255) CHARACTER SET utf8 NOT NULL,
  `desc` char(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `metric` (`metric`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `metric` */

/*Table structure for table `milestone` */

DROP TABLE IF EXISTS `milestone`;

CREATE TABLE `milestone` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `bot_message` text COLLATE utf8mb4_unicode_ci,
  `image_emoji` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `twitter_msg` text COLLATE utf8mb4_unicode_ci,
  `facebook_msg` text COLLATE utf8mb4_unicode_ci,
  `twitter_msg_owner` text COLLATE utf8mb4_unicode_ci,
  `facebook_msg_owner` text COLLATE utf8mb4_unicode_ci,
  `link` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Milestones';

/*Data for the table `milestone` */

/*Table structure for table `milestone_lang` */

DROP TABLE IF EXISTS `milestone_lang`;

CREATE TABLE `milestone_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `bot_message` text COLLATE utf8mb4_unicode_ci,
  `twitter_msg` text COLLATE utf8mb4_unicode_ci,
  `facebook_msg` text COLLATE utf8mb4_unicode_ci,
  `twitter_msg_owner` text COLLATE utf8mb4_unicode_ci,
  `facebook_msg_owner` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `milestone_lang` */

/*Table structure for table `news` */

DROP TABLE IF EXISTS `news`;

CREATE TABLE `news` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `url` tinytext CHARACTER SET utf8 NOT NULL,
  `order` int(11) NOT NULL DEFAULT '1',
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Contiene nombre de archivo',
  `press_banner` tinyint(1) DEFAULT '0' COMMENT 'Para aparecer en banner prensa',
  `media_name` tinytext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Noticias en la cabecera';

/*Data for the table `news` */

/*Table structure for table `news_lang` */

DROP TABLE IF EXISTS `news_lang`;

CREATE TABLE `news_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `url` tinytext CHARACTER SET utf8,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `news_lang` */

/*Table structure for table `node` */

DROP TABLE IF EXISTS `node`;

CREATE TABLE `node` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8 NOT NULL,
  `active` tinyint(1) NOT NULL,
  `project_creation_open` tinyint(1) NOT NULL DEFAULT '1',
  `show_team` tinyint(1) NOT NULL DEFAULT '0',
  `url` varchar(255) CHARACTER SET utf8 NOT NULL,
  `subtitle` text COLLATE utf8mb4_unicode_ci,
  `logo` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Contiene nombre de archivo',
  `location` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `hashtag` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `premium` tinyint(1) NOT NULL,
  `call_to_action_description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `twitter` tinytext CHARACTER SET utf8,
  `facebook` tinytext CHARACTER SET utf8,
  `google` tinytext CHARACTER SET utf8,
  `linkedin` tinytext CHARACTER SET utf8,
  `label` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `owner_background` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Color de background módulo owner',
  `default_consultant` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Asesor por defecto para el proyecto',
  `sponsors_limit` int(2) DEFAULT NULL COMMENT 'Número de sponsors permitidos para el canal',
  `home_img` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Imagen para módulo canales en home',
  `owner_font_color` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Color de fuente módulo owner',
  `call_to_action_background_color` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `owner_social_color` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Color de iconos sociales módulo owner',
  `iframe` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `terms` longtext CHARACTER SET utf8,
  `chatbot_url` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `chatbot_id` int(11) DEFAULT NULL,
  `tip_msg` tinytext CHARACTER SET utf8,
  PRIMARY KEY (`id`),
  KEY `default_consultant` (`default_consultant`),
  CONSTRAINT `node_ibfk_1` FOREIGN KEY (`default_consultant`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Nodos';

/*Data for the table `node` */

insert  into `node`(`id`,`name`,`email`,`active`,`project_creation_open`,`show_team`,`url`,`subtitle`,`logo`,`location`,`description`,`hashtag`,`premium`,`call_to_action_description`,`twitter`,`facebook`,`google`,`linkedin`,`label`,`owner_background`,`default_consultant`,`sponsors_limit`,`home_img`,`owner_font_color`,`call_to_action_background_color`,`owner_social_color`,`iframe`,`terms`,`chatbot_url`,`chatbot_id`,`tip_msg`) values ('goteo','Goteo Central','',1,1,0,'',NULL,NULL,NULL,NULL,NULL,0,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL);

/*Table structure for table `node_data` */

DROP TABLE IF EXISTS `node_data`;

CREATE TABLE `node_data` (
  `node` varchar(50) CHARACTER SET utf8 NOT NULL,
  `projects` smallint(5) unsigned DEFAULT '0',
  `active` tinyint(3) unsigned DEFAULT '0',
  `success` smallint(5) unsigned DEFAULT '0',
  `investors` smallint(5) unsigned DEFAULT '0',
  `supporters` smallint(5) unsigned DEFAULT '0',
  `amount` mediumint(8) unsigned DEFAULT '0',
  `budget` mediumint(8) unsigned DEFAULT '0',
  `rest` mediumint(8) unsigned DEFAULT '0',
  `calls` tinyint(3) unsigned DEFAULT '0',
  `campaigns` tinyint(3) unsigned DEFAULT '0',
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`node`),
  CONSTRAINT `node_data_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Datos resumen nodo';

/*Data for the table `node_data` */

/*Table structure for table `node_lang` */

DROP TABLE IF EXISTS `node_lang`;

CREATE TABLE `node_lang` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `subtitle` text COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `call_to_action_description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  `terms` longtext CHARACTER SET utf8,
  `tip_msg` longtext CHARACTER SET utf8,
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `node_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `node_lang` */

/*Table structure for table `node_post` */

DROP TABLE IF EXISTS `node_post`;

CREATE TABLE `node_post` (
  `node_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `post_id` bigint(20) unsigned NOT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`node_id`,`post_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `node_post_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `node_post_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `node_post` */

/*Table structure for table `node_project` */

DROP TABLE IF EXISTS `node_project`;

CREATE TABLE `node_project` (
  `node_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `project_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`node_id`,`project_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `node_project_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `node_project_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `node_project` */

/*Table structure for table `node_resource` */

DROP TABLE IF EXISTS `node_resource`;

CREATE TABLE `node_resource` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `node_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `icon` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `action` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_url` tinytext COLLATE utf8mb4_unicode_ci,
  `lang` varchar(6) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `action_icon` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `node_resources_ibfk_1` (`node_id`),
  CONSTRAINT `node_resource_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `node_resource` */

/*Table structure for table `node_resource_lang` */

DROP TABLE IF EXISTS `node_resource_lang`;

CREATE TABLE `node_resource_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(6) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `action` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_url` tinytext COLLATE utf8mb4_unicode_ci,
  `pending` tinyint(1) DEFAULT NULL,
  KEY `id` (`id`),
  CONSTRAINT `node_resource_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `node_resource` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `node_resource_lang` */

/*Table structure for table `node_sponsor` */

DROP TABLE IF EXISTS `node_sponsor`;

CREATE TABLE `node_sponsor` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `node_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `url` char(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `node_sponsor_ibfk_1` (`node_id`),
  CONSTRAINT `node_sponsor_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `node_sponsor` */

/*Table structure for table `node_stories` */

DROP TABLE IF EXISTS `node_stories`;

CREATE TABLE `node_stories` (
  `node_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `stories_id` bigint(20) unsigned NOT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`node_id`,`stories_id`),
  KEY `stories_id` (`stories_id`),
  CONSTRAINT `node_stories_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `node_stories_ibfk_2` FOREIGN KEY (`stories_id`) REFERENCES `stories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `node_stories` */

/*Table structure for table `node_workshop` */

DROP TABLE IF EXISTS `node_workshop`;

CREATE TABLE `node_workshop` (
  `node_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `workshop_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`node_id`,`workshop_id`),
  KEY `workshop_id` (`workshop_id`),
  CONSTRAINT `node_workshop_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `node_workshop_ibfk_2` FOREIGN KEY (`workshop_id`) REFERENCES `workshop` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `node_workshop` */

/*Table structure for table `open_tag` */

DROP TABLE IF EXISTS `open_tag`;

CREATE TABLE `open_tag` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `order` tinyint(3) unsigned NOT NULL DEFAULT '1',
  `post` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Agrupacion de los proyectos';

/*Data for the table `open_tag` */

/*Table structure for table `open_tag_lang` */

DROP TABLE IF EXISTS `open_tag_lang`;

CREATE TABLE `open_tag_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `open_tag_lang` */

/*Table structure for table `origin` */

DROP TABLE IF EXISTS `origin`;

CREATE TABLE `origin` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `tag` char(50) CHARACTER SET utf8 NOT NULL,
  `category` char(50) CHARACTER SET utf8 NOT NULL,
  `type` enum('referer','ua') CHARACTER SET utf8 NOT NULL COMMENT 'referer, ua',
  `project_id` char(50) CHARACTER SET utf8 DEFAULT NULL,
  `invest_id` bigint(20) unsigned DEFAULT NULL,
  `call_id` char(50) CHARACTER SET utf8 DEFAULT NULL,
  `counter` int(10) unsigned NOT NULL DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project` (`tag`,`project_id`,`type`,`category`),
  KEY `project_id` (`project_id`),
  KEY `invest_id` (`invest_id`),
  KEY `call_id` (`call_id`),
  KEY `call` (`tag`,`category`,`type`,`call_id`),
  KEY `invest` (`tag`,`category`,`type`,`invest_id`),
  CONSTRAINT `origin_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `origin_ibfk_2` FOREIGN KEY (`invest_id`) REFERENCES `invest` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `origin_ibfk_3` FOREIGN KEY (`call_id`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `origin` */

/*Table structure for table `page` */

DROP TABLE IF EXISTS `page`;

CREATE TABLE `page` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `type` char(20) CHARACTER SET utf8 NOT NULL DEFAULT 'html',
  `url` tinytext CHARACTER SET utf8,
  `content` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Páginas institucionales';

/*Data for the table `page` */

insert  into `page`(`id`,`name`,`description`,`type`,`url`,`content`) values ('about','About','About','html','/about',NULL),('big-error','BIG error','Internal server error and so on','html','/about/fail',NULL),('contact','Contact','Contact form','html','/contact',NULL),('error','Standard error','Url dont match controller','html','/about/error',NULL),('howto','Crete a project','How to create a project','html','/about/howto',NULL),('legal','Legal','Legal','html','/about/legal',NULL),('maintenance','Maintenance','Maintenance','html','/about/maintenance',NULL),('privacy','Privacy','Privacy','html','/legal/privacy',NULL),('terms','Terms and conditions','Terms and conditions','html','/legal/terms',NULL);

/*Table structure for table `page_lang` */

DROP TABLE IF EXISTS `page_lang`;

CREATE TABLE `page_lang` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `content` longtext COLLATE utf8mb4_unicode_ci,
  `pending` tinyint(1) DEFAULT NULL,
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `page_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `page` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `page_lang` */

/*Table structure for table `page_node` */

DROP TABLE IF EXISTS `page_node`;

CREATE TABLE `page_node` (
  `page` varchar(50) NOT NULL,
  `node` varchar(50) NOT NULL,
  `lang` varchar(2) NOT NULL,
  `name` tinytext,
  `description` text,
  `content` longtext,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `page` (`page`,`node`,`lang`),
  KEY `node` (`node`),
  CONSTRAINT `page_node_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Contenidos de las paginas';

/*Data for the table `page_node` */

insert  into `page_node`(`page`,`node`,`lang`,`name`,`description`,`content`,`pending`) values ('about','goteo','en',NULL,NULL,'<p>\r\n    SiteName is a social network for collective financing (monetary donations) and distributed cooperations (services, infrastructures, etc). A platform for investments in projects that cointribute to the common good and are open source and open knowledge. A community for the development of autonomous, creative and innovative projects in the socia, cultural, technical or educational area, and that create new opportunities for the whole of society.</p>\r\n<p>\r\n  &nbsp;</p>\r\n',0),('about','goteo','es',NULL,NULL,'<p>\r\n    SiteName es una red social de financiaci&oacute;n colectiva (aportaciones monetarias) y colaboraci&oacute;n distribuida (servicios, infraestructuras, microtareas y otros recursos). Una plataforma para la inversi&oacute;n de &ldquo;capital riego&rdquo; en proyectos que contribuyan al desarrollo del procom&uacute;n, el c&oacute;digo abierto y/o el conocimiento libre. Una comunidad para apoyar el desarrollo aut&oacute;nomo de iniciativas creativas e innovadoras cuyos fines sean de car&aacute;cter social, cultural, cient&iacute;fico, educativo, tecnol&oacute;gico o ecol&oacute;gico, que generen nuevas oportunidades para la mejora constante de la sociedad.</p>\r\n<p>\r\n  &nbsp;</p>\r\n',0),('contact','goteo','en',NULL,NULL,'<div class=\"contact-info\" style=\"color: #58595b; width: 360px; font-size: 12px;  padding: 5px; line-height: 16px;\">\r\n  <span class=\"intro-tit\" style=\"font-size: 21px; font-weight: bold; line-height: 24px;\">Use these links to quickly find what you are looking for: </span>\r\n    <ul style=\"margin-left: 0;  padding-left: 0;\">\r\n      <li style=\"color: #38b5b1;  margin-left: 0; padding-left: 0; list-style-position: inside; padding-top: 2px; padding-bottom: 2px;\">\r\n          <a href=\"/faq\" style=\"color: #38b5b1; text-decoration: none;\" target=\"_blank\">FAQ - Preguntas frecuentes</a></li>\r\n       <li style=\"color: #38b5b1;  margin-left: 0; padding-left: 0; list-style-position: inside; padding-top: 2px; padding-bottom: 2px;\">\r\n          <a href=\"/glossary\" style=\"color: #38b5b1; text-decoration: none;\" target=\"_blank\">El Glosario de la microfinanciaci&oacute;n</a></li>\r\n      <li style=\"color: #38b5b1;  margin-left: 0; padding-left: 0; list-style-position: inside; padding-top: 2px; padding-bottom: 2px;\">\r\n          <a href=\"/press\" style=\"color: #38b5b1; text-decoration: none;\" target=\"_blank\">Kit de prensa SiteName</a></li>\r\n     <li style=\"color: #38b5b1;  margin-left: 0; padding-left: 0; list-style-position: inside; padding-top: 2px; padding-bottom: 2px;\">\r\n          <a href=\"/service/workshop\" style=\"color: #38b5b1; text-decoration: none;\" target=\"_blank\">Talleres</a></li>\r\n    </ul>\r\n   SiteName is a social network for collective financing (monetary donations) and distributed cooperations (services, infrastructures, etc). A platform for investments in projects that cointribute to the common good and are open source and open content. </div>\r\n',0),('contact','goteo','es',NULL,NULL,'<div class=\"contact-info\" style=\"color: #58595b; width: 360px; font-size: 12px;  padding: 5px; line-height: 16px;\">\r\n  <span class=\"intro-tit\" style=\"font-size: 21px; font-weight: bold; line-height: 24px;\">Quiz&aacute;s estos links resuelvan r&aacute;pidamente lo que buscas: </span>\r\n    <ul style=\"margin-left: 0;  padding-left: 0;\">\r\n      <li style=\"color: #38b5b1;  margin-left: 0; padding-left: 0; list-style-position: inside; padding-top: 2px; padding-bottom: 2px;\">\r\n          <a href=\"/faq\" style=\"color: #38b5b1; text-decoration: none;\" target=\"_blank\">FAQ - Preguntas frecuentes</a></li>\r\n       <li style=\"color: #38b5b1;  margin-left: 0; padding-left: 0; list-style-position: inside; padding-top: 2px; padding-bottom: 2px;\">\r\n          <a href=\"/glossary\" style=\"color: #38b5b1; text-decoration: none;\" target=\"_blank\">El Glosario de la microfinanciaci&oacute;n</a></li>\r\n      <li style=\"color: #38b5b1;  margin-left: 0; padding-left: 0; list-style-position: inside; padding-top: 2px; padding-bottom: 2px;\">\r\n          <a href=\"/press\" style=\"color: #38b5b1; text-decoration: none;\" target=\"_blank\">Kit de prensa SiteName</a></li>\r\n     <li style=\"color: #38b5b1;  margin-left: 0; padding-left: 0; list-style-position: inside; padding-top: 2px; padding-bottom: 2px;\">\r\n          <a href=\"/service/workshop\" style=\"color: #38b5b1; text-decoration: none;\" target=\"_blank\">Talleres</a></li>\r\n    </ul>\r\n   SiteName es una plataforma digital para la financiaci&oacute;n colectiva, colaboraci&oacute;n y distribuci&oacute;n de recursos para el desarrollo de proyectos sociales, culturales, educativos, tecnol&oacute;gicos... que contribuyan al fortalecimiento del procom&uacute;n, el c&oacute;digo abierto y/o el conocimiento libre.</div>\r\n',0),('howto','goteo','en',NULL,NULL,'<div style=\"width:430px; float:left\">\r\n  <div style=\"font-size:14px; line-height:19px; padding-right:16px; margin-top:16px;\">\r\n        SiteName is a platform for investments in projects that cointribute to the common good and are open source and open knowledge. A community for the development of autonomous, creative and innovative projects that have the objective to give a type of collective return, governed by a free or open license (for example Creative Commons or GPL).\r\n       <p>\r\n         That is, projects that yield open DNA, open data, knowledge, digital content and other recourses related to the activity that you want to find financing for.<br />\r\n         <br />\r\n          SiteName is guided by the following conditions and requirements, that you must know if you want to propose a project for co-financing and support by the community of SiteName. If you need any more information on any of the following points we recommend you read <a href=\"/faq\">our FAQ</a>.</p>\r\n   </div>\r\n  <p>\r\n     &nbsp;</p>\r\n  <form action=\"/project/create\" method=\"post\">\r\n       <input class=\"checkbox\" id=\"create_accept\" name=\"confirm\" type=\"checkbox\" value=\"true\" />&nbsp;<span style=\"font-size:12px;\"><label class=\"unselected\" for=\"create_accept\">He le&iacute;do, entiendo y acepto las condiciones y requisitos para crear un proyecto en SiteName, as&iacute; como la <a href=\"/legal/privacy\">pol&iacute;tica de privacidad</a> de la plataforma.</label><br />\r\n        </span>\r\n     <p>\r\n         <span style=\"font-size:12px;\">&nbsp;</span></p>\r\n     <span style=\"font-size:12px;\"><button class=\"disabled\" disabled=\"disabled\" id=\"create_continue\" name=\"action\" type=\"submit\" value=\"continue\">Continuar</button></span></form>\r\n</div>\r\n<div style=\"width:430px; float:right; padding-right:16px; margin-top:16px;\">\r\n <span style=\"font-size:14px;\">Conditions</span>\r\n <p>\r\n     <span style=\"color:#808285; line-height:16px;\">1. If my project offers individual rewards in exchange for certain economic contributions, I will fulfil the commitment established to the platform and my co-financers in case I obtain the minimum amount I asked for.<br />\r\n       <br />\r\n      <strong>2</strong>. I must also comply with commitment to publish the promised collective returns, connected to the SiteName platform under the license chosen at the moment I asked for financing In compliance with a legal contract with the Open Source Foundation.<br />\r\n       <br />\r\n      <strong>3.</strong> I shall request a co-funding minimum to carry out the project optimally. Raising the minimum cofinancing will coincide with the start of production, on which I will send information periodically, allowing me to undertake a second round of cofinancing until I reach the optimal financing. &nbsp;<br />\r\n        <br />\r\n      <strong>4</strong>. The purpose of the project is not the sale of products or already produced services, neither of financing campaigns of charity, politics or of any other type, not criminal or aimed against other people.</span></p>\r\n   <p>\r\n     &nbsp;</p>\r\n  <p>\r\n     <span style=\"font-size:14px;\">Qualifications\n  <p>\r\n     <span style=\"color:#808285; line-height:16px;\">&middot; I am older that 18.</span><br />\r\n        <span style=\"color:#808285; line-height:16px;\">&middot; I have a bank account>\r\n<div style=\"font-size:11px; color:#808285; float:left; clear:left; margin-top:20px; margin-right:10px; \">\r\n You give your consent for the treatment of your personal data. For this purpose, the responsible of the portal has established a  <a href=\"/legal/privacy\">pricacy policy</a>  where you will be able to know the purpose that will be given to the data provided through this form, as well as the rights of that person.</div>\r\n',0),('howto','goteo','es',NULL,NULL,'<div style=\"width:430px; float:left\">\r\n  <div style=\"font-size:14px; line-height:19px; padding-right:16px; margin-top:16px;\">\r\n        SiteName es una plataforma para apoyar proyectos de emprendedores, innovadores sociales y creativos que tengan entre sus objetivos, formato y/o resultado final, de forma total o significativa, alg&uacute;n tipo de retorno colectivo regido por una licencia libre o abierta (por ejemplo Creative Commons o GPL).\r\n       <p>\r\n         Esto es, proyectos con &quot;ADN abierto&quot; en los que se comparte informaci&oacute;n, conocimiento, contenidos digitales y/u otros recursos relacionados con la actividad para la que se busca financiaci&oacute;n.<br />\r\n           <br />\r\n          SiteName se gu&iacute;a por las siguientes condiciones y requisitos, que debes conocer si quieres proponer un proyecto para que opte a ser cofinanciado y recibir la ayuda de la comunidad de SiteName. Si necesitas m&aacute;s informaci&oacute;n sobre cualquiera de los siguientes puntos te recomendamos leer <a href=\"/faq\">nuestras FAQ</a>.</p>\r\n  </div>\r\n  <p>\r\n     &nbsp;</p>\r\n  <form action=\"/project/create\" method=\"post\">\r\n       <input class=\"checkbox\" id=\"create_accept\" name=\"confirm\" type=\"checkbox\" value=\"true\" />&nbsp;<span style=\"font-size:12px;\"><label class=\"unselected\" for=\"create_accept\">He le&iacute;do, entiendo y acepto las condiciones y requisitos para crear un proyecto en SiteName, as&iacute; como la <a href=\"/legal/privacy\">pol&iacute;tica de privacidad</a> de la plataforma.</label><br />\r\n        </span>\r\n     <p>\r\n         <span style=\"font-size:12px;\">&nbsp;</span></p>\r\n     <span style=\"font-size:12px;\"><button class=\"disabled\" disabled=\"disabled\" id=\"create_continue\" name=\"action\" type=\"submit\" value=\"continue\">Continuar</button></span></form>\r\n</div>\r\n<div style=\"width:430px; float:right; padding-right:16px; margin-top:16px;\">\r\n <span style=\"font-size:14px;\">Condiciones</span>\r\n    <p>\r\n     <span style=\"color:#808285; line-height:16px;\">1. Cuando mi proyecto ofrezca recompensas individuales a cambio de aportaciones econ&oacute;micas determinadas, deber&eacute; cumplir con el compromiso establecido con la plataforma y mis cofinanciadores en caso de obtener la financiaci&oacute;n m&iacute;nima solicitada.<br />\r\n        <br />\r\n      <strong>2</strong>. Deber&eacute; cumplir igualmente con el compromiso de publicar los retornos colectivos prometidos, enlaz&aacute;ndolos desde la plataforma SiteName bajo la licencia elegida en el momento de solicitar la financiaci&oacute;n, en cumplimiento de un contrato legal con la Fundaci&oacute;n Goteo.<br />\r\n       <br />\r\n      <strong>3.</strong> Solicitar&eacute; una cofinanciaci&oacute;n m&iacute;nima para llevar a cabo el proyecto y otra &oacute;ptima. La recaudaci&oacute;n de la cofinanciaci&oacute;n m&iacute;nima coincidir&aacute; con el inicio de la producci&oacute;n, sobre la que deber&eacute; ir informando peri&oacute;dicamente, lo que me permitir&aacute; emprender una segunda ronda de cofinanciaci&oacute;n hasta llegar a la financiaci&oacute;n &oacute;ptima. &nbsp;<br />\r\n       <br />\r\n      <strong>4</strong>. La finalidad del proyecto no es la venta encubierta de productos o servicios ya producidos, ni de financiar campa&ntilde;as de beneficencia, pol&iacute;ticas o de cualquier otro tipo, ni delictiva o para atentar contra la dignidad de las personas.</span></p>\r\n  <p>\r\n     &nbsp;</p>\r\n  <p>\r\n     <span style=\"font-size:14px;\">Requisitos</span></p>\r\n <p>\r\n     <span style=\"color:#808285; line-height:16px;\">&middot; Soy mayor de 18 a&ntilde;os.</span><br />\r\n       <span style=\"color:#808285; line-height:16px;\">&middot; Dispongo de una cuenta bancaria.</span></p>\r\n</div>\r\n<div style=\"font-size:11px; color:#808285; float:left; clear:left; margin-top:20px; margin-right:10px; \">\r\n  Ud. presta su consentimiento para el tratamiento de sus datos personales. A tal efecto, el responsable del portal ha establecido una <a href=\"/legal/privacy\">pol&iacute;tica de privacidad</a> donde Ud. podr&aacute; conocer la finalidad que se le dar&aacute;n a los datos suministrados a trav&eacute;s del presente formulario, as&iacute; como los derechos que le asisten.</div>\r\n',0),('privacy','goteo','en',NULL,NULL,'',0),('privacy','goteo','es',NULL,NULL,'',0),('terms','goteo','en',NULL,NULL,'',0),('terms','goteo','es',NULL,NULL,'',0);

/*Table structure for table `patron` */

DROP TABLE IF EXISTS `patron`;

CREATE TABLE `patron` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `node` varchar(50) NOT NULL,
  `project` varchar(50) NOT NULL,
  `user` varchar(50) NOT NULL,
  `title` tinytext,
  `description` text,
  `link` tinytext,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  `active` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_project_node` (`node`,`project`,`user`),
  KEY `project` (`project`),
  CONSTRAINT `patron_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `patron_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Proyectos recomendados por padrinos';

/*Data for the table `patron` */

/*Table structure for table `patron_lang` */

DROP TABLE IF EXISTS `patron_lang`;

CREATE TABLE `patron_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `title` tinytext,
  `description` text,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `patron_lang` */

/*Table structure for table `patron_order` */

DROP TABLE IF EXISTS `patron_order`;

CREATE TABLE `patron_order` (
  `id` varchar(50) NOT NULL,
  `order` tinyint(3) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Orden de los padrinos';

/*Data for the table `patron_order` */

/*Table structure for table `post` */

DROP TABLE IF EXISTS `post`;

CREATE TABLE `post` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `blog` bigint(20) unsigned NOT NULL,
  `slug` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `subtitle` tinytext COLLATE utf8mb4_unicode_ci,
  `section` tinytext COLLATE utf8mb4_unicode_ci,
  `text` longtext COLLATE utf8mb4_unicode_ci,
  `glossary` tinytext COLLATE utf8mb4_unicode_ci,
  `media` tinytext CHARACTER SET utf8,
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Contiene nombre de archivo',
  `header_image` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `date` date NOT NULL COMMENT 'fehca de publicacion',
  `order` int(11) DEFAULT '1',
  `allow` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'Permite comentarios',
  `home` tinyint(1) DEFAULT '0' COMMENT 'para los de portada',
  `footer` tinyint(1) DEFAULT '0' COMMENT 'Para los del footer',
  `publish` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Publicado',
  `legend` text COLLATE utf8mb4_unicode_ci,
  `author` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `num_comments` int(10) unsigned DEFAULT NULL COMMENT 'Número de comentarios que recibe el post',
  `type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'md',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `portada` (`home`),
  KEY `pie` (`footer`),
  KEY `publicadas` (`publish`),
  KEY `post_ibfk_1` (`blog`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`blog`) REFERENCES `blog` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Entradas para la portada';

/*Data for the table `post` */

/*Table structure for table `post_image` */

DROP TABLE IF EXISTS `post_image`;

CREATE TABLE `post_image` (
  `post` bigint(20) unsigned NOT NULL,
  `image` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT 'Contiene nombre de archivo',
  `order` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`post`,`image`),
  CONSTRAINT `post_image_ibfk_1` FOREIGN KEY (`post`) REFERENCES `post` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `post_image` */

/*Table structure for table `post_lang` */

DROP TABLE IF EXISTS `post_lang`;

CREATE TABLE `post_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `blog` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `subtitle` tinytext COLLATE utf8mb4_unicode_ci,
  `text` longtext COLLATE utf8mb4_unicode_ci,
  `legend` text COLLATE utf8mb4_unicode_ci,
  `media` tinytext CHARACTER SET utf8,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`),
  KEY `blog` (`blog`),
  CONSTRAINT `post_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `post` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `post_lang_ibfk_2` FOREIGN KEY (`blog`) REFERENCES `blog` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `post_lang` */

/*Table structure for table `post_node` */

DROP TABLE IF EXISTS `post_node`;

CREATE TABLE `post_node` (
  `post` bigint(20) unsigned NOT NULL,
  `node` varchar(50) CHARACTER SET utf8 NOT NULL,
  `order` int(11) DEFAULT '1',
  PRIMARY KEY (`post`,`node`),
  KEY `node` (`node`),
  CONSTRAINT `post_node_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `post_node_ibfk_2` FOREIGN KEY (`post`) REFERENCES `post` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Entradas para la portada de nodos';

/*Data for the table `post_node` */

/*Table structure for table `post_tag` */

DROP TABLE IF EXISTS `post_tag`;

CREATE TABLE `post_tag` (
  `post` bigint(20) unsigned NOT NULL,
  `tag` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`post`,`tag`),
  KEY `post_tag_ibfk_2` (`tag`),
  CONSTRAINT `post_tag_ibfk_1` FOREIGN KEY (`post`) REFERENCES `post` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `post_tag_ibfk_2` FOREIGN KEY (`tag`) REFERENCES `tag` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tags de las entradas';

/*Data for the table `post_tag` */

/*Table structure for table `project` */

DROP TABLE IF EXISTS `project`;

CREATE TABLE `project` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `subtitle` tinytext COLLATE utf8mb4_unicode_ci,
  `lang` varchar(2) CHARACTER SET utf8 DEFAULT 'es',
  `currency` varchar(4) CHARACTER SET utf8 NOT NULL DEFAULT 'EUR' COMMENT 'Divisa del proyecto',
  `currency_rate` decimal(9,5) NOT NULL DEFAULT '1.00000' COMMENT 'Ratio al crear el proyecto',
  `status` int(1) NOT NULL,
  `translate` int(1) NOT NULL DEFAULT '0',
  `progress` int(3) NOT NULL,
  `owner` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT 'usuario que lo ha creado',
  `node` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT 'nodo en el que se ha creado',
  `amount` int(6) DEFAULT NULL COMMENT 'acumulado actualmente',
  `mincost` int(5) DEFAULT NULL COMMENT 'minimo coste',
  `maxcost` int(5) DEFAULT NULL COMMENT 'optimo',
  `days` int(3) NOT NULL DEFAULT '0' COMMENT 'Dias restantes',
  `num_investors` int(10) unsigned DEFAULT NULL COMMENT 'Numero inversores',
  `popularity` int(10) unsigned DEFAULT NULL COMMENT 'Popularidad del proyecto',
  `num_messengers` int(10) unsigned DEFAULT NULL COMMENT 'Número de personas que envían mensajes',
  `num_posts` int(10) unsigned DEFAULT NULL COMMENT 'Número de post',
  `created` date DEFAULT NULL,
  `updated` date DEFAULT NULL,
  `published` date DEFAULT NULL,
  `success` date DEFAULT NULL,
  `closed` date DEFAULT NULL,
  `passed` date DEFAULT NULL,
  `contract_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contract_nif` varchar(15) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Guardar sin espacios ni puntos ni guiones',
  `phone` varchar(20) CHARACTER SET utf8 DEFAULT NULL COMMENT 'guardar talcual',
  `contract_email` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `address` tinytext COLLATE utf8mb4_unicode_ci,
  `zipcode` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `location` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `country` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Contiene nombre de archivo',
  `description` text COLLATE utf8mb4_unicode_ci,
  `motivation` text COLLATE utf8mb4_unicode_ci,
  `video` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `video_usubs` int(1) NOT NULL DEFAULT '0',
  `about` text COLLATE utf8mb4_unicode_ci,
  `goal` text COLLATE utf8mb4_unicode_ci,
  `related` text COLLATE utf8mb4_unicode_ci,
  `spread` text COLLATE utf8mb4_unicode_ci,
  `reward` text COLLATE utf8mb4_unicode_ci,
  `category` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `keywords` tinytext COLLATE utf8mb4_unicode_ci,
  `media` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `media_usubs` int(1) NOT NULL DEFAULT '0',
  `currently` int(1) DEFAULT NULL,
  `project_location` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `scope` int(1) DEFAULT NULL COMMENT 'Ambito de alcance',
  `resource` text COLLATE utf8mb4_unicode_ci,
  `comment` text COLLATE utf8mb4_unicode_ci,
  `contract_entity` int(1) NOT NULL DEFAULT '0',
  `contract_birthdate` date DEFAULT NULL,
  `entity_office` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `entity_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `entity_cif` varchar(10) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Guardar sin espacios ni puntos ni guiones',
  `post_address` tinytext COLLATE utf8mb4_unicode_ci,
  `secondary_address` int(11) NOT NULL DEFAULT '0',
  `post_zipcode` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `post_location` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `post_country` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `amount_users` int(10) unsigned DEFAULT NULL COMMENT 'Recaudación proveniente de los usuarios',
  `amount_call` int(10) unsigned DEFAULT NULL COMMENT 'Recaudación proveniente de la convocatoria',
  `maxproj` int(5) DEFAULT NULL COMMENT 'Dinero que puede conseguir un proyecto de la convocatoria',
  `analytics_id` varchar(30) CHARACTER SET utf8 DEFAULT NULL,
  `facebook_pixel` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `social_commitment` int(10) unsigned DEFAULT NULL COMMENT 'Social commitment of the project',
  `social_commitment_description` text COLLATE utf8mb4_unicode_ci,
  `execution_plan` text COLLATE utf8mb4_unicode_ci,
  `sustainability_model` text COLLATE utf8mb4_unicode_ci,
  `execution_plan_url` tinytext CHARACTER SET utf8,
  `sustainability_model_url` tinytext CHARACTER SET utf8,
  PRIMARY KEY (`id`),
  KEY `owner` (`owner`),
  KEY `nodo` (`node`),
  KEY `estado` (`status`),
  KEY `passed` (`passed`),
  KEY `published` (`published`),
  KEY `social_commitment` (`social_commitment`),
  KEY `success` (`success`),
  KEY `updated` (`updated`),
  CONSTRAINT `project_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `project_ibfk_2` FOREIGN KEY (`owner`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `project_ibfk_3` FOREIGN KEY (`social_commitment`) REFERENCES `social_commitment` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Proyectos de la plataforma';

/*Data for the table `project` */

insert  into `project`(`id`,`name`,`subtitle`,`lang`,`currency`,`currency_rate`,`status`,`translate`,`progress`,`owner`,`node`,`amount`,`mincost`,`maxcost`,`days`,`num_investors`,`popularity`,`num_messengers`,`num_posts`,`created`,`updated`,`published`,`success`,`closed`,`passed`,`contract_name`,`contract_nif`,`phone`,`contract_email`,`address`,`zipcode`,`location`,`country`,`image`,`description`,`motivation`,`video`,`video_usubs`,`about`,`goal`,`related`,`spread`,`reward`,`category`,`keywords`,`media`,`media_usubs`,`currently`,`project_location`,`scope`,`resource`,`comment`,`contract_entity`,`contract_birthdate`,`entity_office`,`entity_name`,`entity_cif`,`post_address`,`secondary_address`,`post_zipcode`,`post_location`,`post_country`,`amount_users`,`amount_call`,`maxproj`,`analytics_id`,`facebook_pixel`,`social_commitment`,`social_commitment_description`,`execution_plan`,`sustainability_model`,`execution_plan_url`,`sustainability_model_url`) values ('project-finishing-today','Project finishing today','Description Project finishing today','es','EUR',1.00000,3,1,110,'owner-project-finishing','goteo',440,200,400,1,3,0,0,0,'2019-12-31','2020-01-21','2020-01-21',NULL,NULL,'2020-03-01','User testing','00000000-N','00340000000000','tester@goteo.org','Dir tester','00000','Barcelona','España','7_10.jpg','Testing project diseño participativo y auto-construcción',NULL,'https://vimeo.com/81621213',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,'City, country',NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),('project-passed','Project passed','Description Project passed','es','EUR',1.00000,4,1,110,'owner-project-passed','goteo',440,200,400,141,2,0,0,0,'2019-11-16','2019-11-22','2019-11-22','2020-02-10',NULL,'2020-01-01','User testing','00000000-N','00340000000000','tester@example.org','Dir tester','00000','Barcelona','España','7_10.jpg','Testing project',NULL,'https://www.youtube.com/watch?v=3On4rAJdeKg',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,'City, country',NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),('project-passing-today','Project passing today','Description Project passing today','es','EUR',1.00000,3,1,110,'owner-project-passing','goteo',220,200,400,41,2,0,0,0,'2020-02-24','2020-03-01','2020-03-01',NULL,NULL,NULL,'User testing','00000000-N','00340000000000','tester@example.org','Dir tester','00000','Barcelona','España','7_10.jpg','Testing project',NULL,'https://www.youtube.com/watch?v=3On4rAJdeKg',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,'City, country',NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);

/*Table structure for table `project_account` */

DROP TABLE IF EXISTS `project_account`;

CREATE TABLE `project_account` (
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `bank` tinytext CHARACTER SET utf8,
  `bank_owner` tinytext CHARACTER SET utf8,
  `paypal` tinytext CHARACTER SET utf8,
  `paypal_owner` tinytext CHARACTER SET utf8,
  `allowpp` int(1) DEFAULT NULL,
  `fee` int(1) NOT NULL DEFAULT '5' COMMENT 'porcentaje de comisión goteo',
  `vat` int(2) NOT NULL DEFAULT '21' COMMENT '(Value Added Tax) to apply in the financial report',
  `tax_base_percentage` int(3) DEFAULT '100',
  `skip_login` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`project`),
  CONSTRAINT `project_account_ibfk_1` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Cuentas bancarias de proyecto';

/*Data for the table `project_account` */

/*Table structure for table `project_bot` */

DROP TABLE IF EXISTS `project_bot`;

CREATE TABLE `project_bot` (
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `platform` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `channel_id` int(11) NOT NULL,
  UNIQUE KEY `project_platform_channel` (`project`,`platform`,`channel_id`),
  CONSTRAINT `project_bot_ibfk_1` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `project_bot` */

/*Table structure for table `project_category` */

DROP TABLE IF EXISTS `project_category`;

CREATE TABLE `project_category` (
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `category` int(10) unsigned NOT NULL,
  UNIQUE KEY `project_category` (`project`,`category`),
  KEY `category` (`category`),
  KEY `project` (`project`),
  CONSTRAINT `project_category_ibfk_1` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project_category_ibfk_2` FOREIGN KEY (`category`) REFERENCES `category` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Categorias de los proyectos';

/*Data for the table `project_category` */

insert  into `project_category`(`project`,`category`) values ('project-passed',2),('project-passing-today',2);

/*Table structure for table `project_conf` */

DROP TABLE IF EXISTS `project_conf`;

CREATE TABLE `project_conf` (
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `noinvest` int(1) NOT NULL DEFAULT '0' COMMENT 'No se permiten más aportes',
  `watch` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Vigilar el proyecto',
  `days_round1` int(4) DEFAULT '40' COMMENT 'Días que dura la primera ronda desde la publicación del proyecto',
  `days_round2` int(4) DEFAULT '40' COMMENT 'Días que dura la segunda ronda desde la publicación del proyecto',
  `one_round` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Si el proyecto tiene una unica ronda',
  `help_license` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Si necesita ayuda en licencias',
  `help_cost` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Si necesita ayuda en costes',
  `mincost_estimation` int(11) DEFAULT NULL,
  `publishing_estimation` date DEFAULT NULL,
  PRIMARY KEY (`project`),
  CONSTRAINT `project_conf_ibfk_1` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Configuraciones para proyectos';

/*Data for the table `project_conf` */

/*Table structure for table `project_data` */

DROP TABLE IF EXISTS `project_data`;

CREATE TABLE `project_data` (
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `invested` int(6) unsigned NOT NULL DEFAULT '0' COMMENT 'Mostrado en termometro al cerrar',
  `fee` int(6) unsigned NOT NULL DEFAULT '0' COMMENT 'comisiones cobradas por bancos y paypal a goteo',
  `issue` int(6) unsigned NOT NULL DEFAULT '0' COMMENT 'importe de las incidencias',
  `amount` int(6) unsigned NOT NULL DEFAULT '0' COMMENT 'recaudaro realmente',
  `goteo` int(6) unsigned NOT NULL DEFAULT '0' COMMENT 'comision goteo',
  `percent` int(1) unsigned NOT NULL DEFAULT '8' COMMENT 'porcentaje comision goteo',
  `comment` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`project`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='datos de informe financiero';

/*Data for the table `project_data` */

/*Table structure for table `project_image` */

DROP TABLE IF EXISTS `project_image`;

CREATE TABLE `project_image` (
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `image` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '' COMMENT 'Contiene nombre de archivo',
  `section` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `url` tinytext CHARACTER SET utf8,
  `order` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`project`,`image`),
  KEY `proyecto-seccion` (`project`,`section`),
  CONSTRAINT `project_image_ibfk_1` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `project_image` */

/*Table structure for table `project_lang` */

DROP TABLE IF EXISTS `project_lang`;

CREATE TABLE `project_lang` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `motivation` text COLLATE utf8mb4_unicode_ci,
  `video` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `about` text COLLATE utf8mb4_unicode_ci,
  `goal` text COLLATE utf8mb4_unicode_ci,
  `related` text COLLATE utf8mb4_unicode_ci,
  `reward` text COLLATE utf8mb4_unicode_ci,
  `keywords` tinytext COLLATE utf8mb4_unicode_ci,
  `media` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `subtitle` tinytext COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  `social_commitment_description` text COLLATE utf8mb4_unicode_ci,
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `project_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `project_lang` */

insert  into `project_lang`(`id`,`lang`,`description`,`motivation`,`video`,`about`,`goal`,`related`,`reward`,`keywords`,`media`,`subtitle`,`pending`,`social_commitment_description`) values ('project-passed','ca','Catalan test',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Catalan short desc',0,NULL),('project-passed','en','English test',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'English short desc',0,NULL),('project-passing-today','ca','Catalan test',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Catalan short desc',0,NULL),('project-passing-today','en','English test',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'English short desc',0,NULL);

/*Table structure for table `project_location` */

DROP TABLE IF EXISTS `project_location`;

CREATE TABLE `project_location` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `latitude` decimal(16,14) NOT NULL,
  `longitude` decimal(16,14) NOT NULL,
  `radius` smallint(6) NOT NULL DEFAULT '0',
  `method` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT 'ip',
  `locable` tinyint(1) NOT NULL DEFAULT '0',
  `city` varchar(255) CHARACTER SET utf8 NOT NULL,
  `region` varchar(255) CHARACTER SET utf8 NOT NULL,
  `country` varchar(150) CHARACTER SET utf8 NOT NULL,
  `country_code` varchar(2) CHARACTER SET utf8 NOT NULL,
  `info` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `locable` (`locable`),
  CONSTRAINT `project_location_ibfk_1` FOREIGN KEY (`id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `project_location` */

insert  into `project_location`(`id`,`latitude`,`longitude`,`radius`,`method`,`locable`,`city`,`region`,`country`,`country_code`,`info`,`modified`) values ('project-passed',41.30000000000000,2.10000000000000,0,'ip',1,'Barcelona','','Spain','ES',NULL,'2020-04-09 16:50:26'),('project-passing-today',41.30000000000000,2.10000000000000,0,'ip',1,'Barcelona','','Spain','ES',NULL,'2020-04-09 16:50:25');

/*Table structure for table `project_milestone` */

DROP TABLE IF EXISTS `project_milestone`;

CREATE TABLE `project_milestone` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `milestone` bigint(20) unsigned DEFAULT NULL,
  `date` date DEFAULT NULL,
  `post` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `milestone` (`milestone`),
  KEY `post` (`post`),
  KEY `project` (`project`),
  CONSTRAINT `project_milestone_ibfk_1` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project_milestone_ibfk_2` FOREIGN KEY (`milestone`) REFERENCES `milestone` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project_milestone_ibfk_3` FOREIGN KEY (`post`) REFERENCES `post` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Project milestones';

/*Data for the table `project_milestone` */

/*Table structure for table `project_open_tag` */

DROP TABLE IF EXISTS `project_open_tag`;

CREATE TABLE `project_open_tag` (
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `open_tag` int(12) NOT NULL,
  UNIQUE KEY `project_open_tag` (`project`,`open_tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Agrupacion de los proyectos';

/*Data for the table `project_open_tag` */

/*Table structure for table `promote` */

DROP TABLE IF EXISTS `promote`;

CREATE TABLE `promote` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `node` varchar(50) CHARACTER SET utf8 NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  `active` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_node` (`node`,`project`),
  UNIQUE KEY `id` (`id`),
  KEY `activos` (`active`),
  KEY `project` (`project`),
  CONSTRAINT `promote_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `promote_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Proyectos destacados';

/*Data for the table `promote` */

insert  into `promote`(`id`,`node`,`project`,`title`,`description`,`order`,`active`) values (1,'goteo','project-passing-today',NULL,NULL,1,1);

/*Table structure for table `promote_lang` */

DROP TABLE IF EXISTS `promote_lang`;

CREATE TABLE `promote_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `promote_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `promote` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `promote_lang` */

/*Table structure for table `purpose` */

DROP TABLE IF EXISTS `purpose`;

CREATE TABLE `purpose` (
  `text` varchar(50) NOT NULL,
  `purpose` text NOT NULL,
  `html` tinyint(1) DEFAULT NULL COMMENT 'Si el texto lleva formato html',
  `group` varchar(50) NOT NULL DEFAULT 'general' COMMENT 'Agrupacion de uso',
  PRIMARY KEY (`text`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Explicación del propósito de los textos';

/*Data for the table `purpose` */

/*Table structure for table `purpose_copy` */

DROP TABLE IF EXISTS `purpose_copy`;

CREATE TABLE `purpose_copy` (
  `text` varchar(50) NOT NULL,
  `purpose` text NOT NULL,
  `html` tinyint(1) DEFAULT NULL COMMENT 'Si el texto lleva formato html',
  `group` varchar(50) NOT NULL DEFAULT 'general' COMMENT 'Agrupacion de uso',
  PRIMARY KEY (`text`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Explicación del propósito de los textos';

/*Data for the table `purpose_copy` */

/*Table structure for table `question` */

DROP TABLE IF EXISTS `question`;

CREATE TABLE `question` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `questionnaire` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` text COLLATE utf8mb4_unicode_ci,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  `max_score` int(2) NOT NULL DEFAULT '0',
  `vars` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `questions_ibfk_1` (`questionnaire`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`questionnaire`) REFERENCES `questionnaire` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `question` */

/*Table structure for table `question_answer` */

DROP TABLE IF EXISTS `question_answer`;

CREATE TABLE `question_answer` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `question` bigint(20) unsigned NOT NULL,
  `answer` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `question_answer_question` (`question`),
  CONSTRAINT `question_answer_question` FOREIGN KEY (`question`) REFERENCES `question` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `question_answer` */

/*Table structure for table `question_answer_project` */

DROP TABLE IF EXISTS `question_answer_project`;

CREATE TABLE `question_answer_project` (
  `answer` bigint(20) unsigned NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  KEY `question_answer_ibfk` (`answer`),
  KEY `question_answer_project_ibfk` (`project`),
  CONSTRAINT `question_answer_ibfk` FOREIGN KEY (`answer`) REFERENCES `question_answer` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `question_answer_project_ibfk` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `question_answer_project` */

/*Table structure for table `question_lang` */

DROP TABLE IF EXISTS `question_lang`;

CREATE TABLE `question_lang` (
  `question` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `lang` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` text COLLATE utf8mb4_unicode_ci,
  KEY `question_lang_ibfk_1` (`question`),
  CONSTRAINT `question_lang_ibfk_1` FOREIGN KEY (`question`) REFERENCES `question` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `question_lang` */

/*Table structure for table `question_score` */

DROP TABLE IF EXISTS `question_score`;

CREATE TABLE `question_score` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `question` bigint(20) unsigned NOT NULL,
  `answer` bigint(20) unsigned NOT NULL,
  `score` int(3) NOT NULL,
  `evaluator` varchar(50) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_score_question` (`question`),
  KEY `question_score_evaluator` (`evaluator`),
  KEY `question_score_answer` (`answer`),
  CONSTRAINT `question_score_answer` FOREIGN KEY (`answer`) REFERENCES `question_answer` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `question_score_evaluator` FOREIGN KEY (`evaluator`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `question_score_question` FOREIGN KEY (`question`) REFERENCES `question` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `question_score` */

/*Table structure for table `questionnaire` */

DROP TABLE IF EXISTS `questionnaire`;

CREATE TABLE `questionnaire` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `lang` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `questionnaire` */

/*Table structure for table `questionnaire_matcher` */

DROP TABLE IF EXISTS `questionnaire_matcher`;

CREATE TABLE `questionnaire_matcher` (
  `questionnaire` bigint(20) unsigned NOT NULL,
  `matcher` varchar(50) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`questionnaire`),
  KEY `questionnaire_matcher_ibfk_2` (`matcher`),
  CONSTRAINT `questionnaire_matcher_ibfk` FOREIGN KEY (`questionnaire`) REFERENCES `questionnaire` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `questionnaire_matcher_ibfk_2` FOREIGN KEY (`matcher`) REFERENCES `matcher` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `questionnaire_matcher` */

/*Table structure for table `relief` */

DROP TABLE IF EXISTS `relief`;

CREATE TABLE `relief` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `year` int(4) NOT NULL,
  `percentage` int(2) NOT NULL,
  `country` varchar(10) DEFAULT NULL,
  `limit_amount` int(10) NOT NULL,
  `type` int(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `year` (`year`,`country`,`limit_amount`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Desgravaciones fiscales';

/*Data for the table `relief` */

/*Table structure for table `review` */

DROP TABLE IF EXISTS `review`;

CREATE TABLE `review` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `to_checker` text COLLATE utf8mb4_unicode_ci,
  `to_owner` text COLLATE utf8mb4_unicode_ci,
  `score` int(2) NOT NULL DEFAULT '0',
  `max` int(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `project` (`project`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Revision para evaluacion de proyecto';

/*Data for the table `review` */

/*Table structure for table `review_comment` */

DROP TABLE IF EXISTS `review_comment`;

CREATE TABLE `review_comment` (
  `review` bigint(20) unsigned NOT NULL,
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `section` varchar(50) CHARACTER SET utf8 NOT NULL,
  `evaluation` text COLLATE utf8mb4_unicode_ci,
  `recommendation` text COLLATE utf8mb4_unicode_ci,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review`,`user`,`section`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Comentarios de revision';

/*Data for the table `review_comment` */

/*Table structure for table `review_score` */

DROP TABLE IF EXISTS `review_score`;

CREATE TABLE `review_score` (
  `review` bigint(20) unsigned NOT NULL,
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `criteria` bigint(20) unsigned NOT NULL,
  `score` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`review`,`user`,`criteria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Puntuacion por citerio';

/*Data for the table `review_score` */

/*Table structure for table `reward` */

DROP TABLE IF EXISTS `reward`;

CREATE TABLE `reward` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `reward` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `type` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `icon` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `other` tinytext COLLATE utf8mb4_unicode_ci,
  `license` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `amount` int(5) DEFAULT NULL,
  `units` int(5) DEFAULT NULL,
  `fulsocial` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Retorno colectivo cumplido',
  `url` tinytext CHARACTER SET utf8 COMMENT 'Localización del Retorno cumplido',
  `order` tinyint(4) NOT NULL DEFAULT '1' COMMENT 'Orden para retornos colectivos',
  `bonus` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Retorno colectivo adicional',
  `category` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Category social impact',
  `extra_info_message` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `project` (`project`),
  KEY `icon` (`icon`),
  KEY `type` (`type`),
  KEY `order` (`order`),
  CONSTRAINT `reward_ibfk_1` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Retornos colectivos e individuales';

/*Data for the table `reward` */

insert  into `reward`(`id`,`project`,`reward`,`description`,`type`,`icon`,`other`,`license`,`amount`,`units`,`fulsocial`,`url`,`order`,`bonus`,`category`,`extra_info_message`) values (1,'project-passing-today','Test reward 1','reward description','social','code',NULL,'agpl',NULL,NULL,0,NULL,1,0,NULL,NULL),(2,'project-passing-today','Test reward 2','reward description','individual','thanks',NULL,NULL,100,100,0,NULL,2,0,NULL,NULL),(3,'project-passed','Test reward 1','reward description','social','code',NULL,'agpl',NULL,NULL,0,NULL,1,0,NULL,NULL),(4,'project-passed','Test reward 2','reward description','individual','thanks',NULL,NULL,100,100,0,NULL,2,0,NULL,NULL);

/*Table structure for table `reward_lang` */

DROP TABLE IF EXISTS `reward_lang`;

CREATE TABLE `reward_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `reward` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `other` tinytext COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  `extra_info_message` text COLLATE utf8mb4_unicode_ci,
  UNIQUE KEY `id_lang` (`id`,`lang`),
  KEY `project` (`project`),
  CONSTRAINT `reward_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `reward` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reward_lang_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `reward_lang` */

/*Table structure for table `role` */

DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `name` varchar(50) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `role` */

insert  into `role`(`id`,`name`) values ('admin','Administrador'),('caller','Convocador'),('checker','Revisor de proyectos'),('manager','Gestor de contratos'),('root','ROOT'),('superadmin','Super administrador'),('translator','Traductor de contenidos'),('vip','Padrino');

/*Table structure for table `schema_version` */

DROP TABLE IF EXISTS `schema_version`;

CREATE TABLE `schema_version` (
  `version` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `schema_version` */

insert  into `schema_version`(`version`) values ('20200324105949');

/*Table structure for table `sdg` */

DROP TABLE IF EXISTS `sdg`;

CREATE TABLE `sdg` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `icon` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `link` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `sdg` */

insert  into `sdg`(`id`,`name`,`icon`,`description`,`link`,`modified`) values (1,'Fin de la pobreza',NULL,'Poner fin a la pobreza en todas sus formas en todo el mundo','https://www.un.org/sustainabledevelopment/es/poverty/','2018-09-27 01:36:38'),(2,'Hambre cero',NULL,'Poner fin al hambre, lograr la seguridad alimentaria y la mejora de la nutrición y promover la agricultura sostenible','https://www.un.org/sustainabledevelopment/es/hunger/','2018-09-27 01:36:38'),(3,'Salud y bienestar',NULL,'Garantizar una vida sana y promover el bienestar para todos en todas las edades','https://www.un.org/sustainabledevelopment/es/health/','2018-09-27 01:36:38'),(4,'Educación de calidad',NULL,'Garantizar una educación inclusiva, equitativa y de calidad y promover oportunidades de aprendizaje durante toda la vida para todos','https://www.un.org/sustainabledevelopment/es/education/','2018-09-27 01:36:38'),(5,'Igualdad de género',NULL,'Lograr la igualdad entre los géneros y empoderar a todas las mujeres y las niñas','https://www.un.org/sustainabledevelopment/es/gender-equality/','2018-09-27 01:36:38'),(6,'Agua limpia y saneamiento',NULL,'Garantizar la disponibilidad de agua y su gestión sostenible y el saneamiento para todos','https://www.un.org/sustainabledevelopment/es/water-and-sanitation/','2018-09-27 01:36:38'),(7,'Energía asequible y no contaminante',NULL,'Garantizar el acceso a una energía asequible, segura, sostenible y moderna para todos','https://www.un.org/sustainabledevelopment/es/energy/','2018-09-27 01:36:38'),(8,'Trabajo decente y crecimiento económico',NULL,'Promover el crecimiento económico sostenido, inclusivo y sostenible, el empleo pleno y productivo y el trabajo decente para todos','https://www.un.org/sustainabledevelopment/es/economic-growth/','2018-09-27 01:36:38'),(9,'Industria, innovación e infraestructuras',NULL,'Las inversiones en infraestructura son cruciales para lograr un desarrollo sostenible.','https://www.un.org/sustainabledevelopment/es/infrastructure/','2018-09-27 01:36:38'),(10,'Reducción de la desigualdad',NULL,'Reducir la desigualdad en y entre los países','https://www.un.org/sustainabledevelopment/es/inequality/','2018-09-27 01:36:38'),(11,'Ciudades y comunidades sostenibles',NULL,'Lograr que las ciudades y los asentamientos humanos sean inclusivos, seguros, resilientes y sostenibles','https://www.un.org/sustainabledevelopment/es/cities/','2018-09-27 01:36:38'),(12,'Producción y consumo responsables',NULL,'Garantizar modalidades de consumo y producción sostenibles','https://www.un.org/sustainabledevelopment/es/sustainable-consumption-production/','2018-09-27 01:36:38'),(13,'Acción por el clima',NULL,'Adoptar medidas urgentes para combatir el cambio climático y sus efectos','https://www.un.org/sustainabledevelopment/es/climate-change-2/','2018-09-27 01:36:38'),(14,'Vida submarina',NULL,'Conservar y utilizar en forma sostenible los océanos, los mares y los recursos marinos para el desarrollo sostenible','https://www.un.org/sustainabledevelopment/es/oceans/','2018-09-27 01:36:38'),(15,'Vida de ecosistemas terrestres',NULL,'Gestionar sosteniblemente los bosques, luchar contra la desertificación, detener e invertir la degradación de las tierras y detener la pérdida de biodiversidad','https://www.un.org/sustainabledevelopment/es/biodiversity/','2018-09-27 01:36:38'),(16,'Paz, justicia e instituciones sólidas',NULL,'Promover sociedades, justas, pacíficas e inclusivas','https://www.un.org/sustainabledevelopment/es/peace-justice/','2018-09-27 01:36:38'),(17,'Alianzas para lograr los objetivos',NULL,'Revitalizar la Alianza Mundial para el Desarrollo Sostenible','https://www.un.org/sustainabledevelopment/es/globalpartnerships/','2018-09-27 01:36:38');

/*Table structure for table `sdg_category` */

DROP TABLE IF EXISTS `sdg_category`;

CREATE TABLE `sdg_category` (
  `sdg_id` int(10) unsigned NOT NULL,
  `category_id` int(10) unsigned NOT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`sdg_id`,`category_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `sdg_category_ibfk_1` FOREIGN KEY (`sdg_id`) REFERENCES `sdg` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sdg_category_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `sdg_category` */

insert  into `sdg_category`(`sdg_id`,`category_id`,`order`) values (2,2,1),(2,7,1),(2,9,1),(2,10,1),(2,11,1),(2,14,1),(3,2,1),(3,7,1),(3,9,1),(3,10,1),(3,11,1),(3,14,1),(4,2,1),(4,7,1),(4,9,1),(4,10,1),(4,11,1),(4,14,1),(5,6,1),(5,9,1),(5,11,1),(5,14,1),(7,13,1),(7,14,1),(8,2,1),(8,7,1),(8,9,1),(8,10,1),(8,11,1),(8,14,1),(9,2,1),(9,7,1),(9,9,1),(9,10,1),(9,11,1),(9,14,1),(11,2,1),(11,6,1),(11,7,1),(11,9,1),(11,10,1),(11,11,1),(11,14,1),(12,13,1),(12,14,1),(13,13,1),(15,13,1),(15,14,1),(16,6,1),(16,7,1),(16,11,1),(16,14,1);

/*Table structure for table `sdg_footprint` */

DROP TABLE IF EXISTS `sdg_footprint`;

CREATE TABLE `sdg_footprint` (
  `sdg_id` int(10) unsigned NOT NULL,
  `footprint_id` int(10) unsigned NOT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`sdg_id`,`footprint_id`),
  KEY `footprint_id` (`footprint_id`),
  CONSTRAINT `sdg_footprint_ibfk_1` FOREIGN KEY (`sdg_id`) REFERENCES `sdg` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sdg_footprint_ibfk_2` FOREIGN KEY (`footprint_id`) REFERENCES `footprint` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `sdg_footprint` */

insert  into `sdg_footprint`(`sdg_id`,`footprint_id`,`order`) values (1,2,1),(2,2,1),(3,2,1),(4,2,1),(5,3,1),(6,1,1),(7,1,1),(8,2,1),(9,2,1),(10,2,1),(11,2,1),(11,3,1),(12,1,1),(13,1,1),(14,1,1),(15,1,1),(16,3,1),(17,3,1);

/*Table structure for table `sdg_lang` */

DROP TABLE IF EXISTS `sdg_lang`;

CREATE TABLE `sdg_lang` (
  `id` int(10) unsigned NOT NULL,
  `lang` varchar(2) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `link` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pending` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`,`lang`),
  CONSTRAINT `sdg_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `sdg` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `sdg_lang` */

insert  into `sdg_lang`(`id`,`lang`,`name`,`description`,`link`,`pending`) values (1,'ca','Fi de la pobresa','Posar fi a la pobresa en totes les seves formes a tot el món','',0),(1,'en','No poverty','Economic growth must be inclusive to provide sustainable jobs and promote equality.','https://www.un.org/sustainabledevelopment/poverty/',0),(2,'ca','Fam zero','Posar fi a la fam, aconseguir seguretat alimentària, la millora de la nutrició i promoure l\'agricultura sostenible','',0),(2,'en','Zero Hunger','The food and agriculture sector offers key solutions for development, and is central for hunger and poverty eradication.','https://www.un.org/sustainabledevelopment/hunger/',0),(3,'ca','Salut i benestar','Garantir una vida sana i promoure el benestar per a tothom en totes les edats','',0),(3,'en','Good Health and Well-Being','Ensuring healthy lives and promoting the well-being for all at all ages is essential to sustainable development.','https://www.un.org/sustainabledevelopment/health/',0),(4,'ca','Educació de qualitat','Garantir una educació inclusiva, equitativa i de qualitat i promoure oportunitats d\'aprenentatge durant tota la vida per a tots','',0),(4,'en','Quality Education','Obtaining a quality education is the foundation to improving people’s lives and sustainable development.','https://www.un.org/sustainabledevelopment/education/',0),(5,'ca','Igualtat de gènere','Aconseguir la igualtat entre els gèneres i donar poder a totes les dones i nenes','',0),(5,'en','Gender Equality','Gender equality is not only a fundamental human right, but a necessary foundation for a peaceful, prosperous and sustainable world.','https://www.un.org/sustainabledevelopment/gender-equality/',0),(6,'ca','Aigua neta i sanejament','Garantir la disponibilitat d\'aigua i la seva gestió sostenible i el sanejament per a tots','',0),(6,'en','Clean Water and Sanitation','Clean, accessible water for all is an essential part of the world we want to live in.','https://www.un.org/sustainabledevelopment/water-and-sanitation/',0),(7,'ca','Energia assequible i no contaminant','Garantir l\'accés a una energia assequible, segura, sostenible i moderna per a tots','',0),(7,'en','Affordable and Clean Energy','Energy is central to nearly every major challenge and opportunity.','https://www.un.org/sustainabledevelopment/energy/',0),(8,'ca','Treball decent i creixement econòmic','Promoure el creixement econòmic sostingut, inclusiu i sostenible, l\'ocupació plena i productiva i el treball decent per a tots','',0),(8,'en','Decent Work and Economic Growth','Sustainable economic growth will require societies to create the conditions that allow people to have quality jobs.','https://www.un.org/sustainabledevelopment/economic-growth/',0),(9,'ca','Indústria, innovació i infraestructures','Les inversions en infraestructura són crucials per aconseguir un desenvolupament sostenible.','',0),(9,'en','Industry, Innovation and Infrastructure','Investments in infrastructure are crucial to achieving sustainable development.','https://www.un.org/sustainabledevelopment/infrastructure-industrialization/',0),(10,'ca','Reducció de la desigualtat','Reduir la desigualtat en i entre els països','',0),(10,'en','Reduced Inequalities','To reduce inequalities, policies should be universal in principle, paying attention to the needs of disadvantaged and marginalized populations.','https://www.un.org/sustainabledevelopment/inequality/',0),(11,'ca','Ciutats i comunitats sostenibles','Aconseguir que les ciutats i els assentaments humans siguin inclusius, segurs, resilients i sostenibles','',0),(11,'en','Sustainable Cities and Communities','There needs to be a future in which cities provide opportunities for all, with access to basic services, energy, housing, transportation and more.','https://www.un.org/sustainabledevelopment/cities/',0),(12,'ca','Producció i consum responsables','Garantir modalitats de consum i producció sostenibles','',0),(12,'en','Responsible Production and Consumption','Responsible Production and Consumption','https://www.un.org/sustainabledevelopment/sustainable-consumption-production/',0),(13,'ca','Acció pel clima','Adoptar mesures urgents per combatre el canvi climàtic i els seus efectes','',0),(13,'en','Climate Action','Climate change is a global challenge that affects everyone, everywhere.','https://www.un.org/sustainabledevelopment/climate-change-2/',0),(14,'ca','Vida submarina','Conservar i utilitzar en forma sostenible els oceans, els mars i els recursos marins per al desenvolupament sostenible','',0),(14,'en','Life Below Water','Careful management of this essential global resource is a key feature of a sustainable future.','https://www.un.org/sustainabledevelopment/oceans/',0),(15,'ca','Vida d\'ecosistemes terrestres','Gestionar sosteniblement els boscos, lluitar contra la desertificació, aturar i invertir la degradació de les terres i aturar la pèrdua de biodiversitat','',0),(15,'en','Life On Land','Sustainably manage forests, combat desertification, halt and reverse land degradation, halt biodiversity loss','https://www.un.org/sustainabledevelopment/biodiversity/',0),(16,'ca','Pau, justícia i institucions sòlides','Promoure societats, justes, pacífiques i inclusives','',0),(16,'en','Peace, Justice and Strong Institutions','Access to justice for all, and building effective, accountable institutions at all levels.','https://www.un.org/sustainabledevelopment/peace-justice/',0),(17,'ca','Aliances per assolir els objectius','Revitalitzar l\'Aliança Mundial per al Desenvolupament Sostenible','',0),(17,'en','Partnerships for the Goals','Revitalize the global partnership for sustainable development','https://www.un.org/sustainabledevelopment/globalpartnerships/',0);

/*Table structure for table `sdg_project` */

DROP TABLE IF EXISTS `sdg_project`;

CREATE TABLE `sdg_project` (
  `sdg_id` int(10) unsigned NOT NULL,
  `project_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`sdg_id`,`project_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `sdg_project_ibfk_1` FOREIGN KEY (`sdg_id`) REFERENCES `sdg` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sdg_project_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `sdg_project` */

/*Table structure for table `sdg_social_commitment` */

DROP TABLE IF EXISTS `sdg_social_commitment`;

CREATE TABLE `sdg_social_commitment` (
  `sdg_id` int(10) unsigned NOT NULL,
  `social_commitment_id` int(10) unsigned NOT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`sdg_id`,`social_commitment_id`),
  KEY `social_commitment_id` (`social_commitment_id`),
  CONSTRAINT `sdg_social_commitment_ibfk_1` FOREIGN KEY (`sdg_id`) REFERENCES `sdg` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sdg_social_commitment_ibfk_2` FOREIGN KEY (`social_commitment_id`) REFERENCES `social_commitment` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `sdg_social_commitment` */

insert  into `sdg_social_commitment`(`sdg_id`,`social_commitment_id`,`order`) values (2,1,1),(2,2,1),(2,3,1),(2,6,1),(2,7,1),(2,14,1),(3,1,1),(3,3,1),(3,6,1),(3,7,1),(3,14,1),(4,1,1),(4,2,1),(4,3,1),(4,6,1),(4,7,1),(5,3,1),(5,5,1),(5,7,1),(5,10,1),(5,11,1),(5,12,1),(5,13,1),(6,14,1),(7,8,1),(7,15,1),(8,1,1),(8,2,1),(8,3,1),(8,6,1),(8,7,1),(9,1,1),(9,2,1),(9,3,1),(9,6,1),(9,7,1),(11,1,1),(11,2,1),(11,3,1),(11,5,1),(11,6,1),(11,7,1),(11,10,1),(11,11,1),(11,12,1),(11,13,1),(11,15,1),(12,8,1),(12,15,1),(12,16,1),(14,8,1),(15,8,1),(15,16,1),(16,2,1),(16,5,1),(16,7,1),(16,10,1),(16,11,1),(16,12,1),(16,13,1);

/*Table structure for table `sdg_sphere` */

DROP TABLE IF EXISTS `sdg_sphere`;

CREATE TABLE `sdg_sphere` (
  `sdg_id` int(10) unsigned NOT NULL,
  `sphere_id` bigint(20) unsigned NOT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`sdg_id`,`sphere_id`),
  KEY `sphere_id` (`sphere_id`),
  CONSTRAINT `sdg_sphere_ibfk_1` FOREIGN KEY (`sdg_id`) REFERENCES `sdg` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sdg_sphere_ibfk_2` FOREIGN KEY (`sphere_id`) REFERENCES `sphere` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `sdg_sphere` */

insert  into `sdg_sphere`(`sdg_id`,`sphere_id`,`order`) values (2,6,1),(3,14,1),(4,7,1),(5,1,1),(6,10,1),(7,16,1),(8,12,1),(9,19,1),(10,17,1),(11,4,1),(12,18,1),(13,8,1),(14,13,1),(15,2,1),(16,9,1),(17,15,1);

/*Table structure for table `social_commitment` */

DROP TABLE IF EXISTS `social_commitment`;

CREATE TABLE `social_commitment` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(255) CHARACTER SET utf8 NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `icon` char(255) CHARACTER SET utf8 DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Compromiso social';

/*Data for the table `social_commitment` */

insert  into `social_commitment`(`id`,`name`,`description`,`icon`,`modified`) values (1,'Solidario','Solidario','1-solidario-1.png','2017-01-31 14:40:20'),(2,'Software libre','Software libre','2-software-libre-1.png','2017-01-31 14:40:30'),(3,'Generar empleo','Generar empleo','4b-empleo.png','2019-08-23 12:11:11'),(5,'Periodismo independiente','Periodismo independiente','5-periodismo-1.png','2017-01-31 14:41:03'),(6,'Educativo','Educativo','6-educativo-1.png','2017-01-31 14:41:12'),(7,'Crear cultura','Crear cultura','7--crear-cultura-1.png','2017-01-31 14:41:22'),(8,'Acción por el clima','Acción por el clima','8-ecologico-1.png','2019-08-23 12:31:40'),(10,'Datos abiertos','Datos abiertos','10-datos-abiertos-1.png','2017-01-31 14:41:56'),(11,'Reforzar valores democráticos','Reforzar valores democráticos','11--reforzar-valores-democra-ticos.png','2017-01-31 14:42:09'),(12,'Participación ciudadana','Participación ciudadana','12-participacion-ciudadana-1.png','2017-01-31 14:42:18'),(13,'Igualdad de Género',NULL,'iconos-transgenero-26-60x60.png','2019-04-08 15:56:19'),(14,'Salud y Cuidados',NULL,'5b-cuidados.png','2019-08-23 12:10:54'),(15,'Energía y sostenibilidad',NULL,'1b-energia.png','2019-08-23 12:04:13'),(16,'Desarrollo agrorural',NULL,'3b-rural.png','2019-08-23 12:10:24');

/*Table structure for table `social_commitment_footprint` */

DROP TABLE IF EXISTS `social_commitment_footprint`;

CREATE TABLE `social_commitment_footprint` (
  `footprint_id` int(10) unsigned NOT NULL,
  `social_commitment_id` int(10) unsigned NOT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`footprint_id`,`social_commitment_id`),
  KEY `social_commitment_id` (`social_commitment_id`),
  CONSTRAINT `social_commitment_footprint_ibfk_1` FOREIGN KEY (`footprint_id`) REFERENCES `footprint` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `social_commitment_footprint_ibfk_2` FOREIGN KEY (`social_commitment_id`) REFERENCES `social_commitment` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `social_commitment_footprint` */

insert  into `social_commitment_footprint`(`footprint_id`,`social_commitment_id`,`order`) values (1,8,1),(1,15,1),(1,16,1),(2,1,1),(2,2,1),(2,3,1),(2,6,1),(2,7,1),(2,14,1),(3,2,1),(3,5,1),(3,7,1),(3,10,1),(3,11,1),(3,12,1),(3,13,1);

/*Table structure for table `social_commitment_lang` */

DROP TABLE IF EXISTS `social_commitment_lang`;

CREATE TABLE `social_commitment_lang` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` char(255) CHARACTER SET utf8 NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'To be reviewed',
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `social_commitment_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `social_commitment` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `social_commitment_lang` */

insert  into `social_commitment_lang`(`id`,`lang`,`name`,`description`,`pending`) values (1,'ca','Solidari','Solidari',0),(1,'en','Solidary','Solidary',0),(1,'eu','Solidarioa','Solidarioa\r\n',0),(1,'fr','Solidaire','Solidaire',0),(1,'it','Solidale','Solidale',0),(1,'pt','Solidário','Solidário',0),(2,'ca','Programari lliure','Programari lliure',0),(2,'en','Free software','Free software',0),(2,'eu','Software librea','Software librea \r\n',0),(2,'it','Software libero','Software libero',0),(2,'pt','Software livre','Software livre',0),(3,'ca','Generar ocupació','Generar ocupació',0),(3,'en','Creating employment','Creating employment',0),(3,'eu','Enplegua sortzea','Enplegua sortzea\r\n',0),(3,'it','Creare posti di lavoro','Creare posti di lavoro',0),(3,'pt','Gerar emprego','Gerar emprego',0),(5,'ca','Periodisme independent','Periodisme independent',0),(5,'en','Independent journalism','Independent journalism',0),(5,'eu','Kazetaritza independientea','Kazetaritza independientea\r\n',0),(5,'it','Giornalismo indipendente','Giornalismo indipendente',0),(5,'pt','Jornalismo independente','Jornalismo independente ',0),(6,'ca','Educatiu','Educatiu',0),(6,'en','Educational','Educational',0),(6,'eu','Hezigarria','Hezigarria\r\n',0),(6,'it','Educativo','Educativo',0),(6,'pt','Educativo','Educativo',0),(7,'ca','Crear cultura','Crear cultura',0),(7,'en','Creating culture','Creating culture',0),(7,'eu','Kultura sortzea','Kultura sortzea\r\n',0),(7,'it','Creare cultura','Creare cultura',0),(7,'pt','Criar cultura','Criar cultura',0),(8,'ca','Acció pel clima','Acció pel clima',0),(8,'en','Climate action','Ecological',0),(8,'eu','Ekologikoa','Ekologikoa\r\n',0),(8,'it','Ecologico','Ecologico',0),(8,'pt','Ecológico','Ecológico',0),(10,'ca','Dades obertes','Dades obertes',0),(10,'en','Open data','Open data',0),(10,'eu','Datu irekiak','Datu irekiak\r\n',0),(10,'it','Open data','Open data',0),(10,'pt','Dados abertos','Dados abertos',0),(11,'ca','Reforçar valors democràtics','Reforçar valors democràtics',0),(11,'en','To strengthen democratic values','To strengthen democratic values',0),(11,'eu','Balore demokratikoak indartzea','Balore demokratikoak indartzea\r\n',0),(11,'it','Rafforzare i valori democratici','Rafforzare i valori democratici',0),(11,'pt','Reforçar os valores democráticos','Reforçar os valores democráticos ',0),(12,'ca','Participació ciudadana','Participació ciudadana',0),(12,'en','Citizen participation','Citizen participation',0),(12,'eu','Herritarren partaidetza','Herritarren partaidetza\r\n',0),(12,'it','Partecipazione dei cittadini','Partecipazione dei cittadini',0),(12,'pt','Participação dos cidadãos','Participação dos cidadãos',0),(13,'ca','Gènere','Gènere',0),(13,'en','Genre','Genre',0),(13,'eu','Generoa','Generoa',0),(13,'it','Genero','Genero',0),(13,'pt','Gênero','Gênero ',0),(14,'ca','Salut i cures',NULL,0),(14,'en','Health and care',NULL,0),(15,'ca','Energia i sostenibilitat','Energia i sostenibilitat',0),(15,'en','Energy and sustainability',NULL,0),(16,'ca','Desenvolupament agrorural','Desenvolupament agrorural',0),(16,'en','Agrorural development',NULL,0);

/*Table structure for table `sphere` */

DROP TABLE IF EXISTS `sphere`;

CREATE TABLE `sphere` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `icon` char(255) CHARACTER SET utf8 DEFAULT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  `landing_match` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Ámbitos de convocatorias';

/*Data for the table `sphere` */

insert  into `sphere`(`id`,`name`,`icon`,`order`,`landing_match`) values (1,'Cultura','01-cultura-color.png',2,1),(2,'Innovación','02-innovacion-color.png',1,0),(3,'Salud','03-salud-color.png',1,1),(4,'Emprendimiento','04-emprendimiento-color.png',1,1),(5,'Tecnología','05-tecnologia-color.png',4,1),(6,'Ciudad','06-ciudad-color.png',1,1),(7,'Cooperación','07-cooperacion-color.png',3,0),(8,'Género','08-genero-color.png',1,0),(9,'Integración Social','09-integracion-color.png',1,0),(10,'Datos Abiertos','10-opendata-color.png',1,0),(11,'Periodismo','11-periodismo-color.png',1,0),(12,'Ecología','12-sostenibilidad-color.png',1,1),(13,'Infancia','04-emprendimiento-color-1.png',1,0),(14,'Colaboración','07-cooperacion-color-1.png',2,0),(15,'Patrimonio','14-heritage-color.png',1,0),(16,'Digital','10-opendata-color-1.png',1,0),(17,'Educación','13-education-color-1.png',1,1),(18,'Emprendimiento social','20-emprenedoria-social.png',19,0),(19,'Economías colaborativas','21-economies-colaborativas-1..png',20,0);

/*Table structure for table `sphere_lang` */

DROP TABLE IF EXISTS `sphere_lang`;

CREATE TABLE `sphere_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0',
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `sphere_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `sphere` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `sphere_lang` */

insert  into `sphere_lang`(`id`,`lang`,`name`,`pending`) values (1,'ca','Cultura',0),(1,'en','Culture',0),(1,'eu','Kultura',0),(2,'ca','Innovació',0),(2,'en','Innovation',0),(2,'eu','Berrikuntza',0),(3,'ca','Salut',0),(3,'en','Health',0),(3,'eu','Osasuna',0),(4,'ca','Emprenedoria',0),(4,'en','Entrepreneurship',0),(4,'eu','Ekintzailetasuna',0),(5,'ca','Tecnologia',0),(5,'en','Technology',0),(5,'eu','Teknologia',0),(6,'ca','Ciutat',0),(6,'en','City',0),(6,'eu','Hiria',0),(7,'ca','Cooperació',0),(7,'en','Cooperation',0),(7,'eu','Lankidetza',0),(8,'ca','Gènere',0),(8,'en','Genre',0),(8,'eu','Generoa',0),(9,'ca','Integració social',0),(9,'en','Social inclusion',0),(9,'eu','Gizarteratzea',0),(10,'ca','Dades obertes',0),(10,'en','Open Data',0),(10,'eu','Datu irekiak',0),(11,'ca','Periodisme',0),(11,'en','Journalism',0),(11,'eu','Kazetaritza',0),(12,'ca','Ecologia',0),(12,'en','Environment',0),(12,'eu','Ekologia',0),(13,'ca','Infància',0),(13,'en','Childhood',0),(14,'ca','Col·laboració',0),(14,'en','Collaboration',0),(15,'ca','Patrimoni',0),(15,'en','Heritage',0),(16,'ca','Digital',0),(16,'en','Digital',0),(17,'ca','Educació',0),(17,'en','Education',0),(18,'ca','Emprenedoria social',0),(18,'en','Social entrepreneurship',0),(19,'ca','Economies colaborativas',0),(19,'en','Collaborative economies',0);

/*Table structure for table `sponsor` */

DROP TABLE IF EXISTS `sponsor`;

CREATE TABLE `sponsor` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `url` tinytext CHARACTER SET utf8,
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Contiene nombre de archivo',
  `order` int(11) NOT NULL DEFAULT '1',
  `node` varchar(50) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`),
  KEY `node` (`node`),
  CONSTRAINT `sponsor_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Patrocinadores';

/*Data for the table `sponsor` */

/*Table structure for table `stories` */

DROP TABLE IF EXISTS `stories`;

CREATE TABLE `stories` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `node` varchar(50) CHARACTER SET utf8 NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `lang` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order` smallint(5) unsigned NOT NULL DEFAULT '1',
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Contiene nombre de archivo',
  `active` int(1) NOT NULL DEFAULT '0',
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `review` text COLLATE utf8mb4_unicode_ci,
  `url` tinytext CHARACTER SET utf8,
  `post` bigint(20) unsigned DEFAULT NULL,
  `pool_image` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `pool` int(1) NOT NULL DEFAULT '0',
  `text_position` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `type` tinytext COLLATE utf8mb4_unicode_ci,
  `landing_match` tinyint(1) NOT NULL DEFAULT '0',
  `landing_pitch` tinyint(1) NOT NULL DEFAULT '0',
  `sphere` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `node` (`node`),
  KEY `project` (`project`),
  KEY `sphere` (`sphere`),
  CONSTRAINT `sphere` FOREIGN KEY (`sphere`) REFERENCES `sphere` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `stories_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `stories_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Historias existosas';

/*Data for the table `stories` */

/*Table structure for table `stories_lang` */

DROP TABLE IF EXISTS `stories_lang`;

CREATE TABLE `stories_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `review` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `stories_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `stories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `stories_lang` */

/*Table structure for table `support` */

DROP TABLE IF EXISTS `support`;

CREATE TABLE `support` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `support` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `type` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `thread` bigint(20) unsigned DEFAULT NULL COMMENT 'De la tabla message',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `hilo` (`thread`),
  KEY `proyecto` (`project`),
  CONSTRAINT `support_ibfk_1` FOREIGN KEY (`thread`) REFERENCES `message` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `support_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Colaboraciones';

/*Data for the table `support` */

insert  into `support`(`id`,`project`,`support`,`description`,`type`,`thread`) values (1,'project-passing-today','test support','Test description','task',1),(2,'project-passed','test support','Test description','task',1);

/*Table structure for table `support_lang` */

DROP TABLE IF EXISTS `support_lang`;

CREATE TABLE `support_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `support` tinytext COLLATE utf8mb4_unicode_ci,
  `description` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`),
  KEY `project` (`project`),
  CONSTRAINT `support_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `support` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `support_lang_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `support_lang` */

/*Table structure for table `tag` */

DROP TABLE IF EXISTS `tag`;

CREATE TABLE `tag` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tags de blogs (de nodo)';

/*Data for the table `tag` */

/*Table structure for table `tag_lang` */

DROP TABLE IF EXISTS `tag_lang`;

CREATE TABLE `tag_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `tag_lang` */

/*Table structure for table `task` */

DROP TABLE IF EXISTS `task`;

CREATE TABLE `task` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `node` varchar(50) NOT NULL,
  `text` text NOT NULL,
  `url` tinytext,
  `done` varchar(50) DEFAULT NULL,
  `datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `node` (`node`),
  CONSTRAINT `task_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Tareas pendientes de admin';

/*Data for the table `task` */

/*Table structure for table `template` */

DROP TABLE IF EXISTS `template`;

CREATE TABLE `template` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `group` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT 'general' COMMENT 'Agrupación de uso',
  `purpose` tinytext CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `text` text COLLATE utf8mb4_unicode_ci,
  `type` char(20) CHARACTER SET utf8 NOT NULL DEFAULT 'html',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Plantillas emails automáticos';

/*Data for the table `template` */

/*Table structure for table `template_lang` */

DROP TABLE IF EXISTS `template_lang`;

CREATE TABLE `template_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `title` tinytext COLLATE utf8mb4_unicode_ci,
  `text` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  PRIMARY KEY (`id`,`lang`),
  CONSTRAINT `template_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `template` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `template_lang` */

/*Table structure for table `text` */

DROP TABLE IF EXISTS `text`;

CREATE TABLE `text` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(2) CHARACTER SET utf8 NOT NULL DEFAULT 'es',
  `text` text COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  PRIMARY KEY (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Textos multi-idioma';

/*Data for the table `text` */

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 NOT NULL,
  `location` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8 NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender` char(1) CHARACTER SET utf8 DEFAULT NULL,
  `birthyear` year(4) DEFAULT NULL,
  `entity_type` tinyint(1) DEFAULT NULL,
  `legal_entity` tinyint(1) DEFAULT NULL,
  `about` text COLLATE utf8mb4_unicode_ci,
  `keywords` tinytext COLLATE utf8mb4_unicode_ci,
  `active` tinyint(1) NOT NULL,
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contribution` text COLLATE utf8mb4_unicode_ci,
  `twitter` tinytext CHARACTER SET utf8,
  `facebook` tinytext CHARACTER SET utf8,
  `google` tinytext CHARACTER SET utf8,
  `instagram` tinytext CHARACTER SET utf8,
  `identica` tinytext CHARACTER SET utf8,
  `linkedin` tinytext CHARACTER SET utf8,
  `amount` int(7) DEFAULT NULL COMMENT 'Cantidad total aportada',
  `num_patron` int(10) unsigned DEFAULT NULL COMMENT 'Num. proyectos patronizados',
  `num_patron_active` int(10) unsigned DEFAULT NULL COMMENT 'Num. proyectos patronizados activos',
  `worth` int(7) DEFAULT NULL,
  `created` timestamp NULL DEFAULT NULL,
  `modified` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `token` tinytext CHARACTER SET utf8 NOT NULL,
  `rememberme` varchar(255) CHARACTER SET utf8 NOT NULL,
  `hide` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'No se ve publicamente',
  `confirmed` int(1) NOT NULL DEFAULT '0',
  `lang` varchar(2) CHARACTER SET utf8 DEFAULT 'es',
  `node` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `num_invested` int(10) unsigned DEFAULT NULL COMMENT 'Num. proyectos cofinanciados',
  `num_owned` int(10) unsigned DEFAULT NULL COMMENT 'Num. proyectos publicados',
  PRIMARY KEY (`id`),
  KEY `nodo` (`node`),
  KEY `coordenadas` (`location`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `user` */

insert  into `user`(`id`,`name`,`location`,`email`,`password`,`gender`,`birthyear`,`entity_type`,`legal_entity`,`about`,`keywords`,`active`,`avatar`,`contribution`,`twitter`,`facebook`,`google`,`instagram`,`identica`,`linkedin`,`amount`,`num_patron`,`num_patron_active`,`worth`,`created`,`modified`,`token`,`rememberme`,`hide`,`confirmed`,`lang`,`node`,`num_invested`,`num_owned`) values ('backer-1-finishing-project','Backer 1 finishing project',NULL,'backer-1-finishing-project@goteo.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Backer 1 finishing project',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2020-02-19 16:50:25','2020-02-19 16:50:25','','',0,0,'es',NULL,NULL,NULL),('backer-1-passed','Backer 1 passed project',NULL,'backer-1-passed@goteo.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Backer 1 passed project',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2019-11-11 16:50:25','2019-11-11 16:50:25','','',0,0,'es',NULL,NULL,NULL),('backer-1-passing-project','Backer 1 passing project',NULL,'backer-1-passing-project@example.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Backer 1 passing project',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2020-02-19 16:50:25','2020-02-19 16:50:25','','',0,0,'es',NULL,NULL,NULL),('backer-2-finishing-project','Backer 2 finishing project',NULL,'backer-2-finishing-project@goteo.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Backer 2 finishing project',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2020-02-19 16:50:25','2020-02-19 16:50:25','','',0,0,'es',NULL,NULL,NULL),('backer-2-passed','Backer 2 passed project',NULL,'backer-2-passed@goteo.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Backer 2 passed project',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2019-11-11 16:50:25','2019-11-11 16:50:25','','',0,0,'es',NULL,NULL,NULL),('backer-2-passing-project','Backer 2 passing project',NULL,'backer-2-passing-project@example.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Backer 2 passing project',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2020-02-19 16:50:25','2020-02-19 16:50:25','','',0,0,'es',NULL,NULL,NULL),('backer-3-finishing-project','Backer 3 finishing project',NULL,'backer-3-finishing-project@goteo.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Backer 3 finishing project',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2020-02-19 16:50:25','2020-02-19 16:50:25','','',0,0,'es',NULL,NULL,NULL),('backer-3-passed','Backer 3 passed project',NULL,'backer-3-passed@goteo.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Backer 3 finishing project',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2019-11-11 16:50:25','2019-11-11 16:50:25','','',0,0,'es',NULL,NULL,NULL),('backer-3-passing-project','Backer 3 passing project',NULL,'backer-3-passing-project@example.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Backer 3 passing project',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2020-02-19 16:50:25','2020-02-19 16:50:25','','',0,0,'es',NULL,NULL,NULL),('backer-4-finishing-project','Backer 4 finishing project',NULL,'backer-4-finishing-project@goteo.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Backer 4 finishing project',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2020-02-19 16:50:25','2020-02-19 16:50:25','','',0,0,'es',NULL,NULL,NULL),('backer-4-passing-project','Backer 4 passing project',NULL,'backer-4-passing-project@example.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Backer 4 passing project',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2020-02-19 16:50:25','2020-02-19 16:50:25','','',0,0,'es',NULL,NULL,NULL),('owner-project-finishing','Owner project finishing',NULL,'owner-project-finishing@goteo.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Owner project finishing',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2020-02-19 16:50:25','2020-02-19 16:50:25','','',0,0,'es',NULL,NULL,NULL),('owner-project-passed','Owner project passed',NULL,'owner-project-passed@example.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Owner project passed',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2019-11-11 16:50:25','2019-11-11 16:50:25','','',0,0,'es','goteo',NULL,NULL),('owner-project-passing','Owner project passing',NULL,'owner-project-passing@example.org','a94a8fe5ccb19ba61c4c0873d391e987982fbbd3',NULL,NULL,NULL,NULL,'Owner project passing',NULL,1,'0','mucho arte','@owner','feisbuc.com',NULL,NULL,NULL,'ein?',NULL,NULL,NULL,NULL,'2020-02-19 16:50:25','2020-02-19 16:50:25','','',0,0,'es','goteo',NULL,NULL),('root','Sysadmin',NULL,'','dc76e9f0c0006e8f919e0c515c66dbba3982f785',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2020-04-09 16:50:25','2020-04-09 16:50:25','','',1,1,'en','goteo',NULL,NULL);

/*Table structure for table `user_api` */

DROP TABLE IF EXISTS `user_api`;

CREATE TABLE `user_api` (
  `user_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `key` varchar(50) CHARACTER SET utf8 NOT NULL,
  `expiration_date` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `user_api_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `user_api` */

/*Table structure for table `user_call` */

DROP TABLE IF EXISTS `user_call`;

CREATE TABLE `user_call` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `call` varchar(50) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`user`,`call`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Asignacion de convocatorias a admines';

/*Data for the table `user_call` */

/*Table structure for table `user_donation` */

DROP TABLE IF EXISTS `user_donation`;

CREATE TABLE `user_donation` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `amount` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `surname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nif` varchar(12) CHARACTER SET utf8 DEFAULT NULL,
  `address` tinytext COLLATE utf8mb4_unicode_ci,
  `zipcode` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `location` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `region` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `country` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `countryname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numproj` int(2) DEFAULT '1',
  `year` varchar(4) CHARACTER SET utf8 NOT NULL,
  `edited` int(1) DEFAULT '0' COMMENT 'Revisados por el usuario',
  `confirmed` int(1) DEFAULT '0' COMMENT 'Certificado generado',
  `pdf` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'nombre del archivo de certificado',
  PRIMARY KEY (`user`,`year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Datos fiscales donativo';

/*Data for the table `user_donation` */

/*Table structure for table `user_favourite_project` */

DROP TABLE IF EXISTS `user_favourite_project`;

CREATE TABLE `user_favourite_project` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  `date_send` date DEFAULT NULL,
  `date_marked` date DEFAULT NULL,
  UNIQUE KEY `user_favourite_project` (`user`,`project`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='User favourites projects';

/*Data for the table `user_favourite_project` */

/*Table structure for table `user_interest` */

DROP TABLE IF EXISTS `user_interest`;

CREATE TABLE `user_interest` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `interest` int(10) unsigned NOT NULL,
  UNIQUE KEY `user_interest` (`user`,`interest`),
  KEY `usuario` (`user`),
  KEY `interes` (`interest`),
  CONSTRAINT `user_interest_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_interest_ibfk_2` FOREIGN KEY (`interest`) REFERENCES `category` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Intereses de los usuarios';

/*Data for the table `user_interest` */

insert  into `user_interest`(`user`,`interest`) values ('owner-project-passed',2),('owner-project-passing',2);

/*Table structure for table `user_lang` */

DROP TABLE IF EXISTS `user_lang`;

CREATE TABLE `user_lang` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `about` text COLLATE utf8mb4_unicode_ci,
  `name` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `keywords` tinytext COLLATE utf8mb4_unicode_ci,
  `contribution` text COLLATE utf8mb4_unicode_ci,
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `user_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `user_lang` */

/*Table structure for table `user_location` */

DROP TABLE IF EXISTS `user_location`;

CREATE TABLE `user_location` (
  `id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `latitude` decimal(16,14) NOT NULL,
  `longitude` decimal(16,14) NOT NULL,
  `radius` smallint(6) unsigned NOT NULL DEFAULT '0',
  `method` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT 'ip',
  `locable` tinyint(1) NOT NULL DEFAULT '0',
  `city` varchar(255) CHARACTER SET utf8 NOT NULL,
  `region` varchar(255) CHARACTER SET utf8 NOT NULL,
  `country` varchar(150) CHARACTER SET utf8 NOT NULL,
  `country_code` varchar(2) CHARACTER SET utf8 NOT NULL,
  `info` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `locable` (`locable`),
  CONSTRAINT `user_location_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `user_location` */

/*Table structure for table `user_login` */

DROP TABLE IF EXISTS `user_login`;

CREATE TABLE `user_login` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `provider` varchar(50) CHARACTER SET utf8 NOT NULL,
  `oauth_token` text CHARACTER SET utf8 NOT NULL,
  `oauth_token_secret` text CHARACTER SET utf8 NOT NULL,
  `datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user`,`oauth_token`(255)),
  CONSTRAINT `user_login_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `user_login` */

/*Table structure for table `user_node` */

DROP TABLE IF EXISTS `user_node`;

CREATE TABLE `user_node` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `node` varchar(50) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`user`,`node`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `user_node` */

/*Table structure for table `user_personal` */

DROP TABLE IF EXISTS `user_personal`;

CREATE TABLE `user_personal` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `contract_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contract_surname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contract_nif` varchar(15) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Guardar sin espacios ni puntos ni guiones',
  `contract_email` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `phone` varchar(9) CHARACTER SET utf8 DEFAULT NULL COMMENT 'guardar sin espacios ni puntos',
  `address` tinytext COLLATE utf8mb4_unicode_ci,
  `zipcode` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `location` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `country` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Datos personales de usuario';

/*Data for the table `user_personal` */

/*Table structure for table `user_pool` */

DROP TABLE IF EXISTS `user_pool`;

CREATE TABLE `user_pool` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `amount` int(7) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`user`),
  CONSTRAINT `user_pool_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `user_pool` */

/*Table structure for table `user_prefer` */

DROP TABLE IF EXISTS `user_prefer`;

CREATE TABLE `user_prefer` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `updates` int(1) NOT NULL DEFAULT '0',
  `threads` int(1) NOT NULL DEFAULT '0',
  `rounds` int(1) NOT NULL DEFAULT '0',
  `mailing` int(1) NOT NULL DEFAULT '0',
  `email` int(1) NOT NULL DEFAULT '0',
  `tips` int(1) NOT NULL DEFAULT '0',
  `comlang` varchar(2) CHARACTER SET utf8 DEFAULT NULL,
  `currency` varchar(3) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`user`),
  CONSTRAINT `user_prefer_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Preferencias de notificacion de usuario';

/*Data for the table `user_prefer` */

/*Table structure for table `user_project` */

DROP TABLE IF EXISTS `user_project`;

CREATE TABLE `user_project` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `project` varchar(50) CHARACTER SET utf8 NOT NULL,
  UNIQUE KEY `user` (`user`,`project`),
  KEY `project` (`project`),
  CONSTRAINT `user_project_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_project_ibfk_2` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `user_project` */

/*Table structure for table `user_review` */

DROP TABLE IF EXISTS `user_review`;

CREATE TABLE `user_review` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `review` bigint(20) unsigned NOT NULL,
  `ready` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Ha terminado con la revision',
  PRIMARY KEY (`user`,`review`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Asignacion de revision a usuario';

/*Data for the table `user_review` */

/*Table structure for table `user_role` */

DROP TABLE IF EXISTS `user_role`;

CREATE TABLE `user_role` (
  `user_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `role_id` varchar(50) CHARACTER SET utf8 NOT NULL,
  `node_id` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `datetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `user_FK` (`user_id`),
  KEY `role_FK` (`role_id`),
  KEY `node_FK` (`node_id`),
  CONSTRAINT `user_role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_role_ibfk_3` FOREIGN KEY (`node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `user_role` */

insert  into `user_role`(`user_id`,`role_id`,`node_id`,`datetime`) values ('root','checker',NULL,NULL),('root','manager',NULL,NULL),('root','root',NULL,NULL),('root','superadmin',NULL,NULL),('root','translator',NULL,NULL);

/*Table structure for table `user_translang` */

DROP TABLE IF EXISTS `user_translang`;

CREATE TABLE `user_translang` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `lang` varchar(2) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`user`,`lang`),
  CONSTRAINT `user_translang_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Idiomas de traductores';

/*Data for the table `user_translang` */

insert  into `user_translang`(`user`,`lang`) values ('root','ca'),('root','de'),('root','el'),('root','en'),('root','es'),('root','eu'),('root','fr'),('root','gl'),('root','it'),('root','nl'),('root','pt');

/*Table structure for table `user_translate` */

DROP TABLE IF EXISTS `user_translate`;

CREATE TABLE `user_translate` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `type` varchar(10) CHARACTER SET utf8 NOT NULL COMMENT 'Tipo de contenido',
  `item` varchar(50) CHARACTER SET utf8 NOT NULL COMMENT 'id del contenido',
  `ready` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Ha terminado con la traduccion',
  PRIMARY KEY (`user`,`type`,`item`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Asignacion de traduccion a usuario';

/*Data for the table `user_translate` */

/*Table structure for table `user_vip` */

DROP TABLE IF EXISTS `user_vip`;

CREATE TABLE `user_vip` (
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `image` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT 'Contiene nombre de archivo',
  PRIMARY KEY (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Datos usuario colaborador';

/*Data for the table `user_vip` */

/*Table structure for table `user_web` */

DROP TABLE IF EXISTS `user_web`;

CREATE TABLE `user_web` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(50) CHARACTER SET utf8 NOT NULL,
  `url` tinytext CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `user` (`user`),
  CONSTRAINT `user_web_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Webs de los usuarios';

/*Data for the table `user_web` */

/*Table structure for table `workshop` */

DROP TABLE IF EXISTS `workshop`;

CREATE TABLE `workshop` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `title` char(255) NOT NULL,
  `subtitle` tinytext,
  `online` tinyint(1) NOT NULL,
  `blockquote` tinytext,
  `workshop_location` varchar(255) DEFAULT NULL,
  `event_type` tinytext,
  `lang` varchar(2) DEFAULT NULL,
  `description` text NOT NULL,
  `date_in` date NOT NULL,
  `date_out` date NOT NULL,
  `schedule` char(255) NOT NULL,
  `url` char(255) DEFAULT NULL,
  `header_image` varchar(255) DEFAULT NULL,
  `venue` tinytext,
  `city` tinytext,
  `venue_address` text,
  `how_to_get` text,
  `map_iframe` text,
  `schedule_file_url` tinytext,
  `terms_file_url` tinytext,
  `call_id` varchar(50) DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `type` varchar(10) DEFAULT 'md',
  PRIMARY KEY (`id`),
  KEY `call_id` (`call_id`),
  CONSTRAINT `workshop_ibfk_1` FOREIGN KEY (`call_id`) REFERENCES `call` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Talleres';

/*Data for the table `workshop` */

/*Table structure for table `workshop_lang` */

DROP TABLE IF EXISTS `workshop_lang`;

CREATE TABLE `workshop_lang` (
  `id` bigint(20) unsigned NOT NULL,
  `lang` varchar(2) NOT NULL,
  `title` char(255) NOT NULL,
  `subtitle` tinytext,
  `blockquote` tinytext,
  `how_to_get` text,
  `description` text NOT NULL,
  `schedule` char(255) NOT NULL,
  `pending` int(1) DEFAULT '0' COMMENT 'To be reviewed',
  UNIQUE KEY `id_lang` (`id`,`lang`),
  CONSTRAINT `workshop_lang_ibfk_1` FOREIGN KEY (`id`) REFERENCES `workshop` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `workshop_lang` */

/*Table structure for table `workshop_location` */

DROP TABLE IF EXISTS `workshop_location`;

CREATE TABLE `workshop_location` (
  `id` bigint(20) unsigned NOT NULL,
  `latitude` decimal(16,14) NOT NULL,
  `longitude` decimal(16,14) NOT NULL,
  `radius` smallint(6) unsigned NOT NULL DEFAULT '0',
  `method` varchar(50) NOT NULL DEFAULT 'ip',
  `locable` tinyint(1) NOT NULL DEFAULT '0',
  `city` varchar(255) NOT NULL,
  `region` varchar(255) NOT NULL,
  `country` varchar(150) NOT NULL,
  `country_code` varchar(2) NOT NULL,
  `info` varchar(255) DEFAULT NULL,
  `modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `latitude` (`latitude`),
  KEY `longitude` (`longitude`),
  KEY `locable` (`locable`),
  CONSTRAINT `workshop_location_ibfk_1` FOREIGN KEY (`id`) REFERENCES `workshop` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `workshop_location` */

/*Table structure for table `workshop_post` */

DROP TABLE IF EXISTS `workshop_post`;

CREATE TABLE `workshop_post` (
  `workshop_id` bigint(20) unsigned NOT NULL,
  `post_id` bigint(20) unsigned NOT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`workshop_id`,`post_id`),
  KEY `post_id` (`post_id`),
  CONSTRAINT `workshop_post_ibfk_1` FOREIGN KEY (`workshop_id`) REFERENCES `workshop` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `workshop_post_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `workshop_post` */

/*Table structure for table `workshop_sphere` */

DROP TABLE IF EXISTS `workshop_sphere`;

CREATE TABLE `workshop_sphere` (
  `workshop_id` bigint(20) unsigned NOT NULL,
  `sphere_id` bigint(20) unsigned NOT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`workshop_id`,`sphere_id`),
  KEY `sphere_id` (`sphere_id`),
  CONSTRAINT `workshop_sphere_ibfk_1` FOREIGN KEY (`workshop_id`) REFERENCES `workshop` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `workshop_sphere_ibfk_2` FOREIGN KEY (`sphere_id`) REFERENCES `sphere` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `workshop_sphere` */

/*Table structure for table `workshop_sponsor` */

DROP TABLE IF EXISTS `workshop_sponsor`;

CREATE TABLE `workshop_sponsor` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `workshop` bigint(20) unsigned NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `url` char(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `workshop_sponsor_ibfk_1` (`workshop`),
  CONSTRAINT `workshop_sponsor_ibfk_1` FOREIGN KEY (`workshop`) REFERENCES `workshop` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `workshop_sponsor` */

/*Table structure for table `workshop_stories` */

DROP TABLE IF EXISTS `workshop_stories`;

CREATE TABLE `workshop_stories` (
  `workshop_id` bigint(20) unsigned NOT NULL,
  `stories_id` bigint(20) unsigned NOT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`workshop_id`,`stories_id`),
  KEY `stories_id` (`stories_id`),
  CONSTRAINT `workshop_stories_ibfk_1` FOREIGN KEY (`workshop_id`) REFERENCES `workshop` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `workshop_stories_ibfk_2` FOREIGN KEY (`stories_id`) REFERENCES `stories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `workshop_stories` */

/*Table structure for table `worthcracy` */

DROP TABLE IF EXISTS `worthcracy`;

CREATE TABLE `worthcracy` (
  `id` int(2) NOT NULL AUTO_INCREMENT,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `amount` int(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Niveles de meritocracia';

/*Data for the table `worthcracy` */

insert  into `worthcracy`(`id`,`name`,`amount`) values (1,'Fan',25),(2,'Patrocinador/a',100),(3,'Apostador/a',500),(4,'Abonado/a',1000),(5,'Visionario/a',3000);

/*Table structure for table `worthcracy_lang` */

DROP TABLE IF EXISTS `worthcracy_lang`;

CREATE TABLE `worthcracy_lang` (
  `id` int(2) unsigned NOT NULL,
  `lang` varchar(3) CHARACTER SET utf8 NOT NULL,
  `name` tinytext COLLATE utf8mb4_unicode_ci,
  `pending` int(1) DEFAULT '0' COMMENT 'Debe revisarse la traducción',
  UNIQUE KEY `id_lang` (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `worthcracy_lang` */

insert  into `worthcracy_lang`(`id`,`lang`,`name`,`pending`) values (1,'ca','Fan',0),(1,'en','Fan',0),(1,'eu','Zalea',0),(1,'fr','Fan',0),(1,'gl','Fan',0),(2,'ca','Patrocinador/a',0),(2,'en','Member',0),(2,'eu','Babeslea',0),(2,'fr','Sponsor',0),(2,'gl','Patrocinador/a',0),(3,'ca','Apostador/a',0),(3,'en','Supporter',0),(3,'eu','Apostularia',0),(3,'fr','Contributeurs',0),(3,'gl','Xogador/a',0),(4,'ca','Abonat/da',0),(4,'en','Patron',0),(4,'eu','Abonatua',0),(4,'fr','Abonné/e',0),(4,'gl','Abonado/a',0),(5,'ca','Visionari/a',0),(5,'en','Visionary',0),(5,'eu','Irudikorra',0),(5,'fr','Pionner',0),(5,'gl','Visionario/a',0);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
