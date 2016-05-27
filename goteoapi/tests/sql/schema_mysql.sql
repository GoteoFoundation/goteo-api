/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;

DROP TABLE IF EXISTS `banner`;
DROP TABLE IF EXISTS `banner_lang`;
DROP TABLE IF EXISTS `blog`;
DROP TABLE IF EXISTS `call`;
DROP TABLE IF EXISTS `call_banner`;
DROP TABLE IF EXISTS `call_banner_lang`;
DROP TABLE IF EXISTS `call_category`;
DROP TABLE IF EXISTS `call_conf`;
DROP TABLE IF EXISTS `call_icon`;
DROP TABLE IF EXISTS `call_lang`;
DROP TABLE IF EXISTS `call_location`;
DROP TABLE IF EXISTS `call_post`;
DROP TABLE IF EXISTS `call_project`;
DROP TABLE IF EXISTS `call_sponsor`;
DROP TABLE IF EXISTS `campaign`;
DROP TABLE IF EXISTS `category`;
DROP TABLE IF EXISTS `category_lang`;
DROP TABLE IF EXISTS `comment`;
DROP TABLE IF EXISTS `conf`;
DROP TABLE IF EXISTS `contract`;
DROP TABLE IF EXISTS `contract_status`;
DROP TABLE IF EXISTS `cost`;
DROP TABLE IF EXISTS `cost_lang`;
DROP TABLE IF EXISTS `criteria`;
DROP TABLE IF EXISTS `criteria_lang`;
DROP TABLE IF EXISTS `document`;
DROP TABLE IF EXISTS `donor`;
DROP TABLE IF EXISTS `donor_invest`;
DROP TABLE IF EXISTS `info_image`;
DROP TABLE IF EXISTS `donor_location`;
DROP TABLE IF EXISTS `event`;
DROP TABLE IF EXISTS `faq`;
DROP TABLE IF EXISTS `faq_lang`;
DROP TABLE IF EXISTS `feed`;
DROP TABLE IF EXISTS `glossary`;
DROP TABLE IF EXISTS `glossary_image`;
DROP TABLE IF EXISTS `glossary_lang`;
DROP TABLE IF EXISTS `home`;
DROP TABLE IF EXISTS `icon`;
DROP TABLE IF EXISTS `icon_lang`;
DROP TABLE IF EXISTS `icon_license`;
DROP TABLE IF EXISTS `image`;
DROP TABLE IF EXISTS `info`;
DROP TABLE IF EXISTS `info_lang`;
DROP TABLE IF EXISTS `invest`;
DROP TABLE IF EXISTS `invest_address`;
DROP TABLE IF EXISTS `invest_detail`;
DROP TABLE IF EXISTS `invest_location`;
DROP TABLE IF EXISTS `invest_msg`;
DROP TABLE IF EXISTS `invest_node`;
DROP TABLE IF EXISTS `invest_reward`;
DROP TABLE IF EXISTS `license`;
DROP TABLE IF EXISTS `license_lang`;
DROP TABLE IF EXISTS `log`;
DROP TABLE IF EXISTS `mail`;
DROP TABLE IF EXISTS `mail_stats`;
DROP TABLE IF EXISTS `mail_stats_location`;
DROP TABLE IF EXISTS `mailer_content`;
DROP TABLE IF EXISTS `mailer_control`;
DROP TABLE IF EXISTS `mailer_limit`;
DROP TABLE IF EXISTS `mailer_send`;
DROP TABLE IF EXISTS `message`;
DROP TABLE IF EXISTS `message_lang`;
DROP TABLE IF EXISTS `metric`;
DROP TABLE IF EXISTS `milestone`;
DROP TABLE IF EXISTS `milestone_lang`;
DROP TABLE IF EXISTS `news`;
DROP TABLE IF EXISTS `news_lang`;
DROP TABLE IF EXISTS `node`;
DROP TABLE IF EXISTS `node_data`;
DROP TABLE IF EXISTS `node_lang`;
DROP TABLE IF EXISTS `open_tag`;
DROP TABLE IF EXISTS `open_tag_lang`;
DROP TABLE IF EXISTS `page`;
DROP TABLE IF EXISTS `page_lang`;
DROP TABLE IF EXISTS `page_node`;
DROP TABLE IF EXISTS `patron`;
DROP TABLE IF EXISTS `patron_lang`;
DROP TABLE IF EXISTS `patron_order`;
DROP TABLE IF EXISTS `post`;
DROP TABLE IF EXISTS `post_image`;
DROP TABLE IF EXISTS `post_lang`;
DROP TABLE IF EXISTS `post_node`;
DROP TABLE IF EXISTS `post_tag`;
DROP TABLE IF EXISTS `project`;
DROP TABLE IF EXISTS `project_account`;
DROP TABLE IF EXISTS `project_category`;
DROP TABLE IF EXISTS `project_conf`;
DROP TABLE IF EXISTS `project_data`;
DROP TABLE IF EXISTS `project_image`;
DROP TABLE IF EXISTS `project_lang`;
DROP TABLE IF EXISTS `project_location`;
DROP TABLE IF EXISTS `project_milestone`;
DROP TABLE IF EXISTS `project_open_tag`;
DROP TABLE IF EXISTS `promote`;
DROP TABLE IF EXISTS `promote_lang`;
DROP TABLE IF EXISTS `purpose`;
DROP TABLE IF EXISTS `purpose_copy`;
DROP TABLE IF EXISTS `relief`;
DROP TABLE IF EXISTS `review`;
DROP TABLE IF EXISTS `review_comment`;
DROP TABLE IF EXISTS `review_score`;
DROP TABLE IF EXISTS `reward`;
DROP TABLE IF EXISTS `reward_lang`;
DROP TABLE IF EXISTS `role`;
DROP TABLE IF EXISTS `sponsor`;
DROP TABLE IF EXISTS `stories`;
DROP TABLE IF EXISTS `stories_lang`;
DROP TABLE IF EXISTS `support`;
DROP TABLE IF EXISTS `support_lang`;
DROP TABLE IF EXISTS `tag`;
DROP TABLE IF EXISTS `tag_lang`;
DROP TABLE IF EXISTS `task`;
DROP TABLE IF EXISTS `template`;
DROP TABLE IF EXISTS `template_lang`;
DROP TABLE IF EXISTS `text`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `user_api`;
DROP TABLE IF EXISTS `user_call`;
DROP TABLE IF EXISTS `user_donation`;
DROP TABLE IF EXISTS `user_favourite_project`;
DROP TABLE IF EXISTS `user_interest`;
DROP TABLE IF EXISTS `user_lang`;
DROP TABLE IF EXISTS `user_location`;
DROP TABLE IF EXISTS `user_login`;
DROP TABLE IF EXISTS `user_node`;
DROP TABLE IF EXISTS `user_personal`;
DROP TABLE IF EXISTS `user_pool`;
DROP TABLE IF EXISTS `user_prefer`;
DROP TABLE IF EXISTS `user_project`;
DROP TABLE IF EXISTS `user_review`;
DROP TABLE IF EXISTS `user_role`;
DROP TABLE IF EXISTS `user_translang`;
DROP TABLE IF EXISTS `user_translate`;
DROP TABLE IF EXISTS `user_vip`;
DROP TABLE IF EXISTS `user_web`;
DROP TABLE IF EXISTS `worthcracy`;
DROP TABLE IF EXISTS `worthcracy_lang`;

/* Create table in target */
CREATE TABLE `banner`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `project` varchar(50) COLLATE utf8_general_ci NULL  ,
    `order` smallint(5) unsigned NOT NULL  DEFAULT 1 ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Contiene nombre de archivo' ,
    `active` int(1) NOT NULL  DEFAULT 0 ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `url` tinytext COLLATE utf8_general_ci NULL  ,
    PRIMARY KEY (`id`) ,
    KEY `banner_ibfk_1`(`node`) ,
    KEY `banner_ibfk_2`(`project`) ,
    CONSTRAINT `banner_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE ,
    CONSTRAINT `banner_ibfk_2`
    FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Proyectos en banner superior';


/* Create table in target */
CREATE TABLE `banner_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `blog`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `type` varchar(10) COLLATE utf8_general_ci NOT NULL  ,
    `owner` varchar(50) COLLATE utf8_general_ci NOT NULL  COMMENT 'la id del proyecto o nodo' ,
    `active` tinyint(1) NOT NULL  DEFAULT 1 ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Blogs de nodo o proyecto';


/* Create table in target */
CREATE TABLE `call`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NULL  ,
    `subtitle` tinytext COLLATE utf8_general_ci NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  DEFAULT 'es' ,
    `status` int(1) NOT NULL  ,
    `translate` int(1) NOT NULL  DEFAULT 0 ,
    `owner` varchar(50) COLLATE utf8_general_ci NOT NULL  COMMENT 'entidad que convoca' ,
    `amount` int(6) NOT NULL  COMMENT 'presupuesto' ,
    `created` date NULL  ,
    `updated` date NULL  ,
    `opened` date NULL  ,
    `published` date NULL  ,
    `success` date NULL  ,
    `closed` date NULL  ,
    `contract_name` varchar(255) COLLATE utf8_general_ci NULL  ,
    `contract_nif` varchar(10) COLLATE utf8_general_ci NULL  COMMENT 'Guardar sin espacios ni puntos ni guiones' ,
    `phone` varchar(20) COLLATE utf8_general_ci NULL  COMMENT 'guardar sin espacios ni puntos' ,
    `contract_email` varchar(255) COLLATE utf8_general_ci NULL  ,
    `address` tinytext COLLATE utf8_general_ci NULL  ,
    `zipcode` varchar(10) COLLATE utf8_general_ci NULL  ,
    `location` varchar(255) COLLATE utf8_general_ci NULL  ,
    `country` varchar(50) COLLATE utf8_general_ci NULL  ,
    `logo` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Logo. Contiene nombre de archivo' ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Imagen widget. Contiene nombre de archivo' ,
    `backimage` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Imagen background. Contiene nombre de archivo' ,
    `description` longtext COLLATE utf8_general_ci NULL  ,
    `whom` text COLLATE utf8_general_ci NULL  ,
    `apply` text COLLATE utf8_general_ci NULL  ,
    `legal` longtext COLLATE utf8_general_ci NULL  ,
    `dossier` tinytext COLLATE utf8_general_ci NULL  ,
    `tweet` tinytext COLLATE utf8_general_ci NULL  ,
    `fbappid` tinytext COLLATE utf8_general_ci NULL  ,
    `call_location` varchar(256) COLLATE utf8_general_ci NULL  ,
    `resources` text COLLATE utf8_general_ci NULL  COMMENT 'Recursos de capital riego' ,
    `scope` int(1) NOT NULL  ,
    `contract_entity` int(1) NOT NULL  DEFAULT 0 ,
    `contract_birthdate` date NULL  ,
    `entity_office` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Cargo del responsable' ,
    `entity_name` varchar(255) COLLATE utf8_general_ci NULL  ,
    `entity_cif` varchar(10) COLLATE utf8_general_ci NULL  COMMENT 'Guardar sin espacios ni puntos ni guiones' ,
    `post_address` tinytext COLLATE utf8_general_ci NULL  ,
    `secondary_address` int(11) NOT NULL  DEFAULT 0 ,
    `post_zipcode` varchar(10) COLLATE utf8_general_ci NULL  ,
    `post_location` varchar(255) COLLATE utf8_general_ci NULL  ,
    `post_country` varchar(50) COLLATE utf8_general_ci NULL  ,
    `days` int(2) NULL  ,
    `maxdrop` int(6) NULL  COMMENT 'Riego maximo por aporte' ,
    `modemaxp` varchar(3) COLLATE utf8_general_ci NULL  DEFAULT 'imp' COMMENT 'Modalidad del máximo por proyecto: imp = importe, per = porcentaje' ,
    `maxproj` int(6) NOT NULL  COMMENT 'Riego maximo por proyecto' ,
    `num_projects` int(10) unsigned NOT NULL  COMMENT 'Número de proyectos publicados' ,
    `rest` int(10) unsigned NOT NULL  COMMENT 'Importe riego disponible' ,
    `used` int(10) unsigned NOT NULL  COMMENT 'Importe riego comprometido' ,
    `applied` int(10) unsigned NOT NULL  COMMENT 'Número de proyectos aplicados' ,
    `running_projects` int(10) unsigned NOT NULL  COMMENT 'Número de proyectos en campaña' ,
    `success_projects` int(10) unsigned NOT NULL  COMMENT 'Número de proyectos exitosos' ,
    PRIMARY KEY (`id`) ,
    KEY `owner`(`owner`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Convocatorias';


/* Create table in target */
CREATE TABLE `call_banner`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `call` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `url` tinytext COLLATE utf8_general_ci NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Contiene nombre de archivo' ,
    `order` int(11) NOT NULL  DEFAULT 1 ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Banners de convocatorias';


/* Create table in target */
CREATE TABLE `call_banner_lang`(
    `id` int(20) NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `call_category`(
    `call` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `category` int(12) NOT NULL  ,
    UNIQUE KEY `call_category`(`call`,`category`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Categorias de las convocatorias';


/* Create table in target */
CREATE TABLE `call_conf`(
    `call` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `applied` int(4) NULL  COMMENT 'Para fijar numero de proyectos recibidos' ,
    `limit1` set('normal','minimum','unlimited','none') COLLATE utf8_general_ci NOT NULL  DEFAULT 'normal' COMMENT 'tipo limite riego primera ronda' ,
    `limit2` set('normal','minimum','unlimited','none') COLLATE utf8_general_ci NOT NULL  DEFAULT 'none' COMMENT 'tipo limite riego segunda ronda' ,
    `buzz_first` int(1) NOT NULL  DEFAULT 0 COMMENT 'Solo primer hashtag en el buzz' ,
    `buzz_own` int(1) NOT NULL  DEFAULT 1 COMMENT 'Tweets  propios en el buzz' ,
    `buzz_mention` int(1) NOT NULL  DEFAULT 1 COMMENT 'Menciones en el buzz' ,
    PRIMARY KEY (`call`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Configuración de convocatoria';


/* Create table in target */
CREATE TABLE `call_icon`(
    `call` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `icon` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    UNIQUE KEY `call_icon`(`call`,`icon`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Tipos de retorno de las convocatorias';


/* Create table in target */
CREATE TABLE `call_lang`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NULL  ,
    `description` longtext COLLATE utf8_general_ci NULL  ,
    `whom` text COLLATE utf8_general_ci NULL  ,
    `apply` text COLLATE utf8_general_ci NULL  ,
    `legal` longtext COLLATE utf8_general_ci NULL  ,
    `subtitle` text COLLATE utf8_general_ci NULL  ,
    `dossier` tinytext COLLATE utf8_general_ci NULL  ,
    `tweet` tinytext COLLATE utf8_general_ci NULL  ,
    `resources` text COLLATE utf8_general_ci NULL  COMMENT 'Recursos de capital riego' ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `call_location`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `latitude` decimal(16,14) NOT NULL  ,
    `longitude` decimal(16,14) NOT NULL  ,
    `method` varchar(50) COLLATE utf8_general_ci NOT NULL  DEFAULT 'ip' ,
    `locable` tinyint(1) NOT NULL  DEFAULT 0 ,
    `city` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `region` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `country` varchar(150) COLLATE utf8_general_ci NOT NULL  ,
    `country_code` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `info` varchar(255) COLLATE utf8_general_ci NULL  ,
    `modified` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    PRIMARY KEY (`id`) ,
    KEY `latitude`(`latitude`) ,
    KEY `longitude`(`longitude`) ,
    CONSTRAINT `call_location_ibfk_1`
    FOREIGN KEY (`id`) REFERENCES `call` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `call_post`(
    `call` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `post` int(20) NOT NULL  ,
    UNIQUE KEY `call_post`(`call`,`post`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Entradas de blog asignadas a convocatorias';


/* Create table in target */
CREATE TABLE `call_project`(
    `call` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    UNIQUE KEY `call_project`(`call`,`project`) ,
    KEY `call_project_ibfk_2`(`project`) ,
    CONSTRAINT `call_project_ibfk_1`
    FOREIGN KEY (`call`) REFERENCES `call` (`id`) ON UPDATE CASCADE ,
    CONSTRAINT `call_project_ibfk_2`
    FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Proyectos asignados a convocatorias';


/* Create table in target */
CREATE TABLE `call_sponsor`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `call` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `url` tinytext COLLATE utf8_general_ci NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Contiene nombre de archivo' ,
    `order` int(11) NOT NULL  DEFAULT 1 ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Patrocinadores de convocatorias';


/* Create table in target */
CREATE TABLE `campaign`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `call` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `active` int(1) NOT NULL  DEFAULT 0 ,
    `order` smallint(5) unsigned NOT NULL  DEFAULT 1 ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`) ,
    UNIQUE KEY `call_node`(`node`,`call`) ,
    CONSTRAINT `campaign_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Convocatorias en portada';


/* Create table in target */
CREATE TABLE `category`(
    `id` int(10) unsigned NOT NULL  auto_increment ,
    `name` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `order` tinyint(3) unsigned NOT NULL  DEFAULT 1 ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Categorias de los proyectos';


/* Create table in target */
CREATE TABLE `category_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    PRIMARY KEY (`id`,`lang`) ,
    KEY `lang`(`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `comment`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `post` bigint(20) unsigned NOT NULL  ,
    `date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP ,
    `text` text COLLATE utf8_general_ci NOT NULL  ,
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Comentarios';


/* Create table in target */
CREATE TABLE `conf`(
    `key` varchar(255) COLLATE utf8_general_ci NOT NULL  COMMENT 'Clave' ,
    `value` varchar(255) COLLATE utf8_general_ci NOT NULL  COMMENT 'Valor'
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Para guardar pares para configuraciones, bloqueos etc';


/* Create table in target */
CREATE TABLE `contract`(
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `number` int(11) NOT NULL  auto_increment ,
    `date` date NOT NULL  COMMENT 'dia anterior a la publicacion' ,
    `enddate` date NOT NULL  COMMENT 'finalización, un año despues de la fecha de contrato' ,
    `pdf` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Archivo pdf contrato' ,
    `type` varchar(1) COLLATE utf8_general_ci NOT NULL  DEFAULT '0' COMMENT '0 = persona física; 1 = representante asociacion; 2 = apoderado entidad mercantil' ,
    `name` tinytext COLLATE utf8_general_ci NULL  ,
    `nif` varchar(14) COLLATE utf8_general_ci NULL  ,
    `office` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Cargo en la asociación o empresa' ,
    `address` tinytext COLLATE utf8_general_ci NULL  ,
    `location` varchar(255) COLLATE utf8_general_ci NULL  ,
    `region` varchar(255) COLLATE utf8_general_ci NULL  ,
    `zipcode` varchar(8) COLLATE utf8_general_ci NULL  ,
    `country` varchar(50) COLLATE utf8_general_ci NULL  ,
    `entity_name` tinytext COLLATE utf8_general_ci NULL  ,
    `entity_cif` varchar(10) COLLATE utf8_general_ci NULL  ,
    `entity_address` tinytext COLLATE utf8_general_ci NULL  ,
    `entity_location` varchar(255) COLLATE utf8_general_ci NULL  ,
    `entity_region` varchar(255) COLLATE utf8_general_ci NULL  ,
    `entity_zipcode` varchar(8) COLLATE utf8_general_ci NULL  ,
    `entity_country` varchar(50) COLLATE utf8_general_ci NULL  ,
    `reg_name` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Nombre y ciudad del registro en el que esta inscrita la entidad' ,
    `reg_date` date NULL  ,
    `reg_number` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Número de registro' ,
    `reg_loc` tinytext COLLATE utf8_general_ci NULL  COMMENT 'NO SE USA (borrar)' ,
    `reg_id` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Número de protocolo del notario' ,
    `reg_idname` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Nombre del notario' ,
    `reg_idloc` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Ciudad de actuación del notario' ,
    `project_name` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Nombre del proyecto' ,
    `project_url` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'URL del proyecto' ,
    `project_owner` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Nombre del impulsor' ,
    `project_user` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Nombre del usuario autor del proyecto' ,
    `project_profile` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'URL del perfil del autor del proyecto' ,
    `project_description` text COLLATE utf8_general_ci NULL  COMMENT 'Breve descripción del proyecto' ,
    `project_invest` text COLLATE utf8_general_ci NULL  COMMENT 'objetivo del crowdfunding' ,
    `project_return` text COLLATE utf8_general_ci NULL  COMMENT 'retornos' ,
    `bank` tinytext COLLATE utf8_general_ci NULL  ,
    `bank_owner` tinytext COLLATE utf8_general_ci NULL  ,
    `paypal` tinytext COLLATE utf8_general_ci NULL  ,
    `paypal_owner` tinytext COLLATE utf8_general_ci NULL  ,
    `birthdate` date NULL  ,
    PRIMARY KEY (`project`) ,
    UNIQUE KEY `numero`(`number`) ,
    CONSTRAINT `contract_ibfk_1`
    FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Contratos';


/* Create table in target */
CREATE TABLE `contract_status`(
    `contract` varchar(50) COLLATE utf8_general_ci NOT NULL  COMMENT 'Id del proyecto' ,
    `owner` int(1) NOT NULL  DEFAULT 0 COMMENT 'El impulsor ha dado por rellenados los datos' ,
    `owner_date` date NULL  COMMENT 'Fecha que se cambia el flag' ,
    `owner_user` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'Usuario que cambia el flag' ,
    `admin` int(1) NOT NULL  DEFAULT 0 COMMENT 'El admin ha comenzado a revisar los datos' ,
    `admin_date` date NULL  COMMENT 'Fecha que se cambia el flag' ,
    `admin_user` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'Usuario que cambia el flag' ,
    `ready` int(1) NOT NULL  DEFAULT 0 COMMENT 'Datos verificados y correctos' ,
    `ready_date` date NULL  COMMENT 'Fecha que se cambia el flag' ,
    `ready_user` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'Usuario que cambia el flag' ,
    `pdf` int(1) NOT NULL  COMMENT 'El impulsor ha descargado el pdf' ,
    `pdf_date` date NULL  COMMENT 'Fecha que se cambia el flag' ,
    `pdf_user` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'Usuario que cambia el flag' ,
    `recieved` int(1) NOT NULL  DEFAULT 0 COMMENT 'Se ha recibido el contrato firmado' ,
    `recieved_date` date NULL  COMMENT 'Fecha que se cambia el flag' ,
    `recieved_user` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'Usuario que cambia el flag' ,
    `payed` int(1) NOT NULL  DEFAULT 0 COMMENT 'Se ha realizado el pago al proyecto' ,
    `payed_date` date NULL  COMMENT 'Fecha que se cambia el flag' ,
    `payed_user` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'Usuario que cambia el flag' ,
    `prepay` int(1) NOT NULL  DEFAULT 0 COMMENT 'Ha habido pago avanzado' ,
    `prepay_date` date NULL  COMMENT 'Fecha que se cambia el flag' ,
    `prepay_user` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'Usuario que cambia el flag' ,
    `closed` int(1) NOT NULL  DEFAULT 0 COMMENT 'Contrato finiquitado' ,
    `closed_date` date NULL  COMMENT 'Fecha que se cambia el flag' ,
    `closed_user` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'Usuario que cambia el flag' ,
    PRIMARY KEY (`contract`) ,
    CONSTRAINT `contract_status_ibfk_1`
    FOREIGN KEY (`contract`) REFERENCES `contract` (`project`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Seguimiento de estado de contrato';


/* Create table in target */
CREATE TABLE `cost`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `cost` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `type` varchar(50) COLLATE utf8_general_ci NULL  ,
    `amount` int(5) NULL  DEFAULT 0 ,
    `required` tinyint(1) NULL  DEFAULT 0 ,
    `from` date NULL  ,
    `until` date NULL  ,
    `order` int(10) unsigned NOT NULL  DEFAULT 1 ,
    PRIMARY KEY (`id`) ,
    KEY `order`(`order`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Desglose de costes de proyectos';


/* Create table in target */
CREATE TABLE `cost_lang`(
    `id` int(20) NOT NULL  ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `cost` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`) ,
    KEY `project`(`project`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `criteria`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `section` varchar(50) COLLATE utf8_general_ci NOT NULL  DEFAULT 'node' ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `order` tinyint(4) NOT NULL  DEFAULT 1 ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Criterios de puntuación';


/* Create table in target */
CREATE TABLE `criteria_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `document`(
    `id` int(10) unsigned NOT NULL  auto_increment ,
    `contract` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `name` varchar(255) COLLATE utf8_general_ci NULL  ,
    `type` varchar(20) COLLATE utf8_general_ci NULL  ,
    `size` int(10) unsigned NULL  ,
    PRIMARY KEY (`id`) ,
    KEY `contract`(`contract`) ,
    CONSTRAINT `document_ibfk_1`
    FOREIGN KEY (`contract`) REFERENCES `contract` (`project`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `event`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `type` char(20) COLLATE utf8_general_ci NOT NULL  DEFAULT 'communication' ,
    `action` char(100) COLLATE utf8_general_ci NOT NULL  ,
    `hash` char(32) COLLATE utf8_general_ci NOT NULL  ,
    `result` char(255) COLLATE utf8_general_ci NULL  ,
    `created` datetime NOT NULL  ,
    `finalized` datetime NULL  ,
    `succeeded` tinyint(1) NULL  DEFAULT 0 ,
    `error` char(255) COLLATE utf8_general_ci NULL  ,
    `modified` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    PRIMARY KEY (`id`) ,
    KEY `hash`(`hash`) ,
    KEY `succeeded`(`succeeded`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `faq`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `section` varchar(50) COLLATE utf8_general_ci NOT NULL  DEFAULT 'node' ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `order` tinyint(4) NOT NULL  DEFAULT 1 ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`) ,
    KEY `node`(`node`) ,
    CONSTRAINT `faq_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Preguntas frecuentes';


/* Create table in target */
CREATE TABLE `faq_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `feed`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `title` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `url` tinytext COLLATE utf8_general_ci NULL  ,
    `datetime` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP ,
    `scope` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `type` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `html` text COLLATE utf8_general_ci NOT NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Contiene nombre de archivo' ,
    `target_type` varchar(10) COLLATE utf8_general_ci NULL  COMMENT 'tipo de objetivo' ,
    `target_id` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'registro objetivo' ,
    `post` int(20) unsigned NULL  COMMENT 'Entrada de blog' ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`) ,
    KEY `scope`(`scope`) ,
    KEY `type`(`type`) ,
    KEY `target_type`(`target_type`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Log de eventos';


/* Create table in target */
CREATE TABLE `glossary`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `text` longtext COLLATE utf8_general_ci NULL  COMMENT 'texto de la entrada' ,
    `media` tinytext COLLATE utf8_general_ci NULL  ,
    `legend` text COLLATE utf8_general_ci NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Imagen principal' ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Entradas para el glosario';


/* Create table in target */
CREATE TABLE `glossary_image`(
    `glossary` bigint(20) unsigned NOT NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NOT NULL  DEFAULT '' COMMENT 'Contiene nombre de archivo' ,
    PRIMARY KEY (`glossary`,`image`) ,
    CONSTRAINT `glossary_image_ibfk_1`
    FOREIGN KEY (`glossary`) REFERENCES `glossary` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `glossary_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `text` longtext COLLATE utf8_general_ci NULL  ,
    `legend` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `home`(
    `item` varchar(10) COLLATE utf8_general_ci NOT NULL  ,
    `type` varchar(5) COLLATE utf8_general_ci NOT NULL  DEFAULT 'main' COMMENT 'lateral o central' ,
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `order` smallint(5) unsigned NOT NULL  DEFAULT 1 ,
    UNIQUE KEY `item_node`(`item`,`node`) ,
    KEY `node`(`node`) ,
    CONSTRAINT `home_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Elementos en portada';


/* Create table in target */
CREATE TABLE `icon`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `name` varchar(100) COLLATE utf8_general_ci NOT NULL  ,
    `description` tinytext COLLATE utf8_general_ci NULL  ,
    `group` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'exclusivo para grupo' ,
    `order` int(11) NOT NULL  DEFAULT 0 ,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Iconos para retorno/recompensa';


/* Create table in target */
CREATE TABLE `icon_lang`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `name` varchar(100) COLLATE utf8_general_ci NULL  ,
    `description` tinytext COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `icon_license`(
    `icon` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `license` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    UNIQUE KEY `icon`(`icon`,`license`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Licencias para cada icono, solo social';


/* Create table in target */
CREATE TABLE `image`(
    `id` int(20) unsigned NOT NULL  auto_increment ,
    `name` varchar(50) COLLATE utf8_general_ci NULL  ,
    `type` varchar(20) COLLATE utf8_general_ci NULL  ,
    `size` int(10) unsigned NULL  ,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `info`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `text` longtext COLLATE utf8_general_ci NULL  COMMENT 'texto de la entrada' ,
    `media` tinytext COLLATE utf8_general_ci NULL  ,
    `publish` tinyint(1) NOT NULL  DEFAULT 0 ,
    `order` int(11) NULL  DEFAULT 1 ,
    `legend` text COLLATE utf8_general_ci NULL  ,
    `gallery` varchar(2000) COLLATE utf8_general_ci NULL  COMMENT 'Galería de imagenes' ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Imagen principal' ,
    `share_facebook` tinytext COLLATE utf8_general_ci NULL  ,
    `share_twitter` tinytext COLLATE utf8_general_ci NULL  ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`) ,
    KEY `node`(`node`) ,
    CONSTRAINT `info_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Entradas about';


/* Create table in target */
CREATE TABLE `info_image`(
    `info` bigint(20) unsigned NOT NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NOT NULL  DEFAULT '' COMMENT 'Contiene nombre de archivo' ,
    PRIMARY KEY (`info`,`image`) ,
    CONSTRAINT `info_image_ibfk_1`
    FOREIGN KEY (`info`) REFERENCES `info` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `info_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `text` longtext COLLATE utf8_general_ci NULL  ,
    `legend` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    `share_facebook` tinytext COLLATE utf8_general_ci NULL  ,
    `share_twitter` tinytext COLLATE utf8_general_ci NULL  ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `invest`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `project` varchar(50) COLLATE utf8_general_ci NULL  ,
    `account` varchar(256) COLLATE utf8_general_ci NOT NULL  COMMENT 'Solo para aportes de cash' ,
    `amount` int(6) NOT NULL  ,
    `amount_original` int(6) NULL  COMMENT 'Importe introducido por el usuario' ,
    `currency` varchar(4) COLLATE utf8_general_ci NOT NULL  DEFAULT 'EUR' COMMENT 'Divisa al aportar' ,
    `currency_rate` decimal(9,5) NOT NULL  DEFAULT 1.00000 COMMENT 'Ratio de conversión a eurio al aportar' ,
    `status` int(1) NOT NULL  COMMENT '-1 en proceso, 0 pendiente, 1 cobrado, 2 devuelto, 3 pagado al proyecto' ,
    `anonymous` tinyint(1) NULL  ,
    `resign` tinyint(1) NULL  ,
    `invested` date NULL  ,
    `charged` date NULL  ,
    `returned` date NULL  ,
    `preapproval` varchar(256) COLLATE utf8_general_ci NULL  COMMENT 'PreapprovalKey' ,
    `payment` varchar(256) COLLATE utf8_general_ci NULL  COMMENT 'PayKey' ,
    `transaction` varchar(256) COLLATE utf8_general_ci NULL  COMMENT 'PaypalId' ,
    `method` varchar(20) COLLATE utf8_general_ci NOT NULL  COMMENT 'Metodo de pago' ,
    `admin` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'Admin que creó el aporte manual' ,
    `campaign` int(1) unsigned NULL  COMMENT 'si es un aporte de capital riego' ,
    `datetime` timestamp NULL  DEFAULT CURRENT_TIMESTAMP ,
    `drops` bigint(20) unsigned NULL  COMMENT 'id del aporte que provoca este riego' ,
    `droped` bigint(20) unsigned NULL  COMMENT 'id del riego generado por este aporte' ,
    `call` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'campaña dedonde sale el dinero' ,
    `issue` int(1) NULL  COMMENT 'Problemas con el cobro del aporte' ,
    `pool` int(1) NULL  COMMENT 'A reservar si el proyecto falla' ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`) ,
    KEY `usuario`(`user`) ,
    KEY `proyecto`(`project`) ,
    KEY `convocatoria`(`call`) ,
    CONSTRAINT `invest_ibfk_1`
    FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON UPDATE CASCADE ,
    CONSTRAINT `invest_ibfk_2`
    FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Aportes monetarios a proyectos';


/* Create table in target */
CREATE TABLE `invest_address`(
    `invest` bigint(20) unsigned NOT NULL  ,
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `address` tinytext COLLATE utf8_general_ci NULL  ,
    `zipcode` varchar(10) COLLATE utf8_general_ci NULL  ,
    `location` varchar(255) COLLATE utf8_general_ci NULL  ,
    `country` varchar(50) COLLATE utf8_general_ci NULL  ,
    `name` varchar(255) COLLATE utf8_general_ci NULL  ,
    `nif` varchar(10) COLLATE utf8_general_ci NULL  ,
    `namedest` tinytext COLLATE utf8_general_ci NULL  ,
    `emaildest` tinytext COLLATE utf8_general_ci NULL  ,
    `regalo` int(1) NULL  DEFAULT 0 ,
    `message` text COLLATE utf8_general_ci NULL  ,
    PRIMARY KEY (`invest`) ,
    KEY `user`(`user`) ,
    CONSTRAINT `invest_address_ibfk_1`
    FOREIGN KEY (`invest`) REFERENCES `invest` (`id`) ON UPDATE CASCADE ,
    CONSTRAINT `invest_address_ibfk_2`
    FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Dirección de entrega de recompensa';


/* Create table in target */
CREATE TABLE `invest_detail`(
    `invest` bigint(20) unsigned NOT NULL  ,
    `type` varchar(30) COLLATE utf8_general_ci NOT NULL  ,
    `log` text COLLATE utf8_general_ci NOT NULL  ,
    `date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    UNIQUE KEY `invest_type`(`invest`,`type`) ,
    KEY `invest`(`invest`) ,
    CONSTRAINT `invest_detail_ibfk_1`
    FOREIGN KEY (`invest`) REFERENCES `invest` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Detalles de los aportes';


/* Create table in target */
CREATE TABLE `invest_location`(
    `id` bigint(20) unsigned NOT NULL  ,
    `latitude` decimal(16,14) NOT NULL  ,
    `longitude` decimal(16,14) NOT NULL  ,
    `method` varchar(50) COLLATE utf8_general_ci NOT NULL  DEFAULT 'ip' ,
    `locable` tinyint(1) NOT NULL  DEFAULT 0 ,
    `city` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `region` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `country` varchar(150) COLLATE utf8_general_ci NOT NULL  ,
    `country_code` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `info` varchar(255) COLLATE utf8_general_ci NULL  ,
    `modified` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    PRIMARY KEY (`id`) ,
    KEY `latitude`(`latitude`) ,
    KEY `longitude`(`longitude`) ,
    KEY `locable`(`locable`) ,
    CONSTRAINT `invest_location_ibfk_1`
    FOREIGN KEY (`id`) REFERENCES `invest` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `invest_msg`(
    `invest` bigint(20) unsigned NOT NULL  ,
    `msg` text COLLATE utf8_general_ci NULL  ,
    PRIMARY KEY (`invest`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Mensaje de apoyo al proyecto tras aportar';


/* Create table in target */
CREATE TABLE `invest_node`(
    `user_id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `user_node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `project_id` varchar(50) COLLATE utf8_general_ci NULL  ,
    `project_node` varchar(50) COLLATE utf8_general_ci NULL  ,
    `invest_id` bigint(20) unsigned NOT NULL  ,
    `invest_node` varchar(50) COLLATE utf8_general_ci NOT NULL  COMMENT 'Nodo en el que se hace el aporte' ,
    UNIQUE KEY `invest`(`invest_id`) ,
    KEY `invest_id`(`invest_id`) ,
    KEY `invest_node`(`invest_node`) ,
    KEY `project_id`(`project_id`) ,
    KEY `project_node`(`project_node`) ,
    KEY `user_id`(`user_id`) ,
    KEY `user_node`(`user_node`) ,
    CONSTRAINT `invest_node_ibfk_1`
    FOREIGN KEY (`user_node`) REFERENCES `node` (`id`) ON UPDATE CASCADE ,
    CONSTRAINT `invest_node_ibfk_2`
    FOREIGN KEY (`project_node`) REFERENCES `node` (`id`) ON UPDATE CASCADE ,
    CONSTRAINT `invest_node_ibfk_3`
    FOREIGN KEY (`invest_node`) REFERENCES `node` (`id`) ON UPDATE CASCADE ,
    CONSTRAINT `invest_node_ibfk_4`
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE ,
    CONSTRAINT `invest_node_ibfk_5`
    FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE ,
    CONSTRAINT `invest_node_ibfk_6`
    FOREIGN KEY (`invest_id`) REFERENCES `invest` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Aportes por usuario/nodo a proyecto/nodo';


/* Create table in target */
CREATE TABLE `invest_reward`(
    `invest` bigint(20) unsigned NOT NULL  ,
    `reward` bigint(20) unsigned NOT NULL  ,
    `fulfilled` tinyint(1) NOT NULL  DEFAULT 0 ,
    UNIQUE KEY `invest`(`invest`,`reward`) ,
    KEY `reward`(`reward`) ,
    CONSTRAINT `invest_reward_ibfk_1`
    FOREIGN KEY (`invest`) REFERENCES `invest` (`id`) ON DELETE CASCADE ON UPDATE CASCADE ,
    CONSTRAINT `invest_reward_ibfk_2`
    FOREIGN KEY (`reward`) REFERENCES `reward` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Recompensas elegidas al aportar';


/* Create table in target */
CREATE TABLE `license`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `name` varchar(100) COLLATE utf8_general_ci NOT NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `group` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'grupo de restriccion de menor a mayor' ,
    `url` varchar(256) COLLATE utf8_general_ci NULL  ,
    `order` tinyint(4) NULL  DEFAULT 1 ,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Licencias de distribucion';


/* Create table in target */
CREATE TABLE `license_lang`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `name` varchar(100) COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `url` varchar(256) COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `log`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `scope` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `target_type` varchar(10) COLLATE utf8_general_ci NULL  COMMENT 'tipo de objetivo' ,
    `target_id` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'registro objetivo' ,
    `text` text COLLATE utf8_general_ci NULL  ,
    `url` tinytext COLLATE utf8_general_ci NULL  ,
    `datetime` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP ,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Log de cosas';


/* Create table in target */
CREATE TABLE `mail`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `email` char(255) COLLATE utf8_general_ci NOT NULL  ,
    `subject` char(255) COLLATE utf8_general_ci NULL  ,
    `content` longtext COLLATE utf8_general_ci NOT NULL  ,
    `template` bigint(20) unsigned NULL  ,
    `node` varchar(50) COLLATE utf8_general_ci NULL  ,
    `date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP ,
    `lang` varchar(2) COLLATE utf8_general_ci NULL  COMMENT 'Idioma en el que se solicitó la plantilla' ,
    `sent` tinyint(4) NULL  ,
    `error` tinytext COLLATE utf8_general_ci NULL  ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`,`email`) ,
    KEY `email`(`email`) ,
    KEY `node`(`node`) ,
    KEY `template`(`template`) ,
    CONSTRAINT `mail_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE ,
    CONSTRAINT `mail_ibfk_2`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE ,
    CONSTRAINT `mail_ibfk_3`
    FOREIGN KEY (`template`) REFERENCES `template` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Contenido enviado por email para el -si no ves-';


/* Create table in target */
CREATE TABLE `mail_stats`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `mail_id` bigint(20) unsigned NOT NULL  ,
    `email` char(150) COLLATE utf8_general_ci NOT NULL  ,
    `metric_id` bigint(20) unsigned NOT NULL  ,
    `counter` int(10) unsigned NOT NULL  DEFAULT 0 ,
    `created_at` datetime NOT NULL  ,
    `modified_at` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    PRIMARY KEY (`id`,`mail_id`,`email`,`metric_id`) ,
    KEY `email`(`email`) ,
    KEY `metric`(`metric_id`) ,
    KEY `mail_id`(`mail_id`) ,
    CONSTRAINT `mail_stats_ibfk_1`
    FOREIGN KEY (`metric_id`) REFERENCES `metric` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `mail_stats_location`(
    `id` bigint(20) unsigned NOT NULL  ,
    `latitude` decimal(16,14) NOT NULL  ,
    `longitude` decimal(16,14) NOT NULL  ,
    `method` varchar(50) COLLATE utf8_general_ci NOT NULL  DEFAULT 'ip' ,
    `locable` tinyint(1) NOT NULL  DEFAULT 0 ,
    `city` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `region` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `country` varchar(150) COLLATE utf8_general_ci NOT NULL  ,
    `country_code` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `info` varchar(255) COLLATE utf8_general_ci NULL  ,
    `modified` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    PRIMARY KEY (`id`) ,
    KEY `latitude`(`latitude`) ,
    KEY `longitude`(`longitude`) ,
    KEY `locable`(`locable`) ,
    CONSTRAINT `mail_stats_location_ibfk_1`
    FOREIGN KEY (`id`) REFERENCES `mail_stats` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `mailer_content`(
    `id` int(20) unsigned NOT NULL  auto_increment ,
    `active` int(1) NOT NULL  DEFAULT 1 ,
    `mail` bigint(20) unsigned NOT NULL  ,
    `datetime` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP ,
    `blocked` int(1) NULL  ,
    `reply` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Email remitente' ,
    `reply_name` text COLLATE utf8_general_ci NULL  COMMENT 'Nombre remitente' ,
    PRIMARY KEY (`id`) ,
    KEY `mail`(`mail`) ,
    CONSTRAINT `mailer_content_ibfk_1`
    FOREIGN KEY (`mail`) REFERENCES `mail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Contenido a enviar';


/* Create table in target */
CREATE TABLE `mailer_control`(
    `email` char(150) COLLATE utf8_general_ci NOT NULL  ,
    `bounces` int(10) unsigned NOT NULL  ,
    `complaints` int(10) unsigned NOT NULL  ,
    `action` enum('allow','deny') COLLATE utf8_general_ci NULL  DEFAULT 'allow' ,
    `last_reason` char(255) COLLATE utf8_general_ci NULL  ,
    `modified` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Lista negra para bounces y complaints';


/* Create table in target */
CREATE TABLE `mailer_limit`(
    `hora` time NOT NULL  COMMENT 'Hora envio' ,
    `num` int(5) unsigned NOT NULL  DEFAULT 0 COMMENT 'Cuantos' ,
    `modified` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    PRIMARY KEY (`hora`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Para limitar el número de envios diarios';


/* Create table in target */
CREATE TABLE `mailer_send`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `mailing` int(20) unsigned NOT NULL  COMMENT 'Id de mailer_content' ,
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `email` varchar(256) COLLATE utf8_general_ci NOT NULL  ,
    `name` varchar(100) COLLATE utf8_general_ci NOT NULL  ,
    `datetime` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP ,
    `sent` int(1) NULL  ,
    `error` text COLLATE utf8_general_ci NULL  ,
    `blocked` int(1) NULL  ,
    UNIQUE KEY `id`(`id`) ,
    KEY `mailing`(`mailing`) ,
    CONSTRAINT `mailer_send_ibfk_1`
    FOREIGN KEY (`mailing`) REFERENCES `mailer_content` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Destinatarios pendientes y realizados';


/* Create table in target */
CREATE TABLE `message`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `thread` bigint(20) unsigned NULL  ,
    `date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    `message` text COLLATE utf8_general_ci NOT NULL  ,
    `blocked` tinyint(1) NOT NULL  DEFAULT 0 COMMENT 'No se puede modificar ni borrar' ,
    `closed` tinyint(1) NOT NULL  DEFAULT 0 COMMENT 'No se puede responder' ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Mensajes de usuarios en proyecto';


/* Create table in target */
CREATE TABLE `message_lang`(
    `id` int(20) NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `message` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `metric`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `metric` char(255) COLLATE utf8_general_ci NOT NULL  ,
    `desc` char(255) COLLATE utf8_general_ci NULL  ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `metric`(`metric`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `milestone`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `type` varchar(255) COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  ,
    `image_emoji` varchar(255) COLLATE utf8_general_ci NULL  ,
    `twitter_msg` text COLLATE utf8_general_ci NULL  ,
    `facebook_msg` text COLLATE utf8_general_ci NULL  ,
    `twitter_msg_owner` text COLLATE utf8_general_ci NULL  ,
    `facebook_msg_owner` text COLLATE utf8_general_ci NULL  ,
    `link` varchar(255) COLLATE utf8_general_ci NULL  ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Milestones';


/* Create table in target */
CREATE TABLE `milestone_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `name` varchar(255) COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `twitter_msg` text COLLATE utf8_general_ci NULL  ,
    `facebook_msg` text COLLATE utf8_general_ci NULL  ,
    `twitter_msg_owner` text COLLATE utf8_general_ci NULL  ,
    `facebook_msg_owner` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `news`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `title` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `description` text COLLATE utf8_general_ci NULL  COMMENT 'Entradilla' ,
    `url` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `order` int(11) NOT NULL  DEFAULT 1 ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Contiene nombre de archivo' ,
    `press_banner` tinyint(1) NULL  DEFAULT 0 COMMENT 'Para aparecer en banner prensa' ,
    `media_name` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Medio de prensa en que se publica' ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Noticias en la cabecera';


/* Create table in target */
CREATE TABLE `news_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `url` tinytext COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `node`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `name` varchar(256) COLLATE utf8_general_ci NOT NULL  ,
    `email` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `active` tinyint(1) NOT NULL  ,
    `url` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `subtitle` text COLLATE utf8_general_ci NULL  ,
    `logo` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Contiene nombre de archivo' ,
    `location` varchar(100) COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `twitter` tinytext COLLATE utf8_general_ci NULL  ,
    `facebook` tinytext COLLATE utf8_general_ci NULL  ,
    `google` tinytext COLLATE utf8_general_ci NULL  ,
    `linkedin` tinytext COLLATE utf8_general_ci NULL  ,
    `label` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Sello en proyectos' ,
    `owner_background` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Color de background módulo owner' ,
    `default_consultant` varchar(50) COLLATE utf8_general_ci NULL  COMMENT 'Asesor por defecto para el proyecto' ,
    `sponsors_limit` int(2) NULL  COMMENT 'Número de sponsors permitidos para el canal' ,
    `home_img` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Imagen para módulo canales en home' ,
    PRIMARY KEY (`id`) ,
    KEY `default_consultant`(`default_consultant`) ,
    CONSTRAINT `node_ibfk_1`
    FOREIGN KEY (`default_consultant`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Nodos';


/* Create table in target */
CREATE TABLE `node_data`(
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `projects` smallint(5) unsigned NULL  DEFAULT 0 ,
    `active` tinyint(3) unsigned NULL  DEFAULT 0 ,
    `success` smallint(5) unsigned NULL  DEFAULT 0 ,
    `investors` smallint(5) unsigned NULL  DEFAULT 0 ,
    `supporters` smallint(5) unsigned NULL  DEFAULT 0 ,
    `amount` mediumint(8) unsigned NULL  DEFAULT 0 ,
    `budget` mediumint(8) unsigned NULL  DEFAULT 0 ,
    `rest` mediumint(8) unsigned NULL  DEFAULT 0 ,
    `calls` tinyint(3) unsigned NULL  DEFAULT 0 ,
    `campaigns` tinyint(3) unsigned NULL  DEFAULT 0 ,
    `updated` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    PRIMARY KEY (`node`) ,
    CONSTRAINT `node_data_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Datos resumen nodo';


/* Create table in target */
CREATE TABLE `node_lang`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `subtitle` text COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`) ,
    CONSTRAINT `node_lang_ibfk_1`
    FOREIGN KEY (`id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `open_tag`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `name` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `order` tinyint(3) unsigned NOT NULL  DEFAULT 1 ,
    `post` bigint(20) unsigned NULL  ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Agrupacion de los proyectos';


/* Create table in target */
CREATE TABLE `open_tag_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `page`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `url` tinytext COLLATE utf8_general_ci NULL  ,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Páginas institucionales';


/* Create table in target */
CREATE TABLE `page_lang`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `page_node`(
    `page` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `content` longtext COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `page`(`page`,`node`,`lang`) ,
    KEY `node`(`node`) ,
    CONSTRAINT `page_node_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Contenidos de las paginas';


/* Create table in target */
CREATE TABLE `post`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `blog` bigint(20) unsigned NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `text` longtext COLLATE utf8_general_ci NULL  COMMENT 'texto de la entrada' ,
    `media` tinytext COLLATE utf8_general_ci NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Contiene nombre de archivo' ,
    `date` date NOT NULL  COMMENT 'fehca de publicacion' ,
    `order` int(11) NULL  DEFAULT 1 ,
    `allow` tinyint(1) NOT NULL  DEFAULT 1 COMMENT 'Permite comentarios' ,
    `home` tinyint(1) NULL  DEFAULT 0 COMMENT 'para los de portada' ,
    `footer` tinyint(1) NULL  DEFAULT 0 COMMENT 'Para los del footer' ,
    `publish` tinyint(1) NOT NULL  DEFAULT 0 COMMENT 'Publicado' ,
    `legend` text COLLATE utf8_general_ci NULL  ,
    `author` varchar(50) COLLATE utf8_general_ci NULL  ,
    `num_comments` int(10) unsigned NULL  COMMENT 'Número de comentarios que recibe el post' ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`) ,
    KEY `portada`(`home`) ,
    KEY `pie`(`footer`) ,
    KEY `publicadas`(`publish`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Entradas para la portada';


/* Create table in target */
CREATE TABLE `post_image`(
    `post` bigint(20) unsigned NOT NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NOT NULL  DEFAULT '' COMMENT 'Contiene nombre de archivo' ,
    PRIMARY KEY (`post`,`image`) ,
    CONSTRAINT `post_image_ibfk_1`
    FOREIGN KEY (`post`) REFERENCES `post` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `post_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `blog` int(20) NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `text` longtext COLLATE utf8_general_ci NULL  ,
    `legend` text COLLATE utf8_general_ci NULL  ,
    `media` tinytext COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`) ,
    KEY `blog`(`blog`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `post_node`(
    `post` bigint(20) unsigned NOT NULL  ,
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `order` int(11) NULL  DEFAULT 1 ,
    PRIMARY KEY (`post`,`node`) ,
    KEY `node`(`node`) ,
    CONSTRAINT `post_node_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Entradas para la portada de nodos';


/* Create table in target */
CREATE TABLE `post_tag`(
    `post` bigint(20) unsigned NOT NULL  ,
    `tag` bigint(20) unsigned NOT NULL  ,
    PRIMARY KEY (`post`,`tag`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Tags de las entradas';


/* Create table in target */
CREATE TABLE `project`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NULL  ,
    `subtitle` tinytext COLLATE utf8_general_ci NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NULL  DEFAULT 'es' ,
    `currency` varchar(4) COLLATE utf8_general_ci NOT NULL  DEFAULT 'EUR' COMMENT 'Divisa del proyecto' ,
    `currency_rate` decimal(9,5) NOT NULL  DEFAULT 1.00000 COMMENT 'Ratio al crear el proyecto' ,
    `status` int(1) NOT NULL  ,
    `translate` int(1) NOT NULL  DEFAULT 0 ,
    `progress` int(3) NOT NULL  ,
    `owner` varchar(50) COLLATE utf8_general_ci NOT NULL  COMMENT 'usuario que lo ha creado' ,
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  COMMENT 'nodo en el que se ha creado' ,
    `amount` int(6) NULL  COMMENT 'acumulado actualmente' ,
    `mincost` int(5) NULL  COMMENT 'minimo coste' ,
    `maxcost` int(5) NULL  COMMENT 'optimo' ,
    `days` int(3) NOT NULL  DEFAULT 0 COMMENT 'Dias restantes' ,
    `num_investors` int(10) unsigned NULL  COMMENT 'Numero inversores' ,
    `popularity` int(10) unsigned NULL  COMMENT 'Popularidad del proyecto' ,
    `num_messengers` int(10) unsigned NULL  COMMENT 'Número de personas que envían mensajes' ,
    `num_posts` int(10) unsigned NULL  COMMENT 'Número de post' ,
    `created` date NULL  ,
    `updated` date NULL  ,
    `published` date NULL  ,
    `success` date NULL  ,
    `closed` date NULL  ,
    `passed` date NULL  ,
    `contract_name` varchar(255) COLLATE utf8_general_ci NULL  ,
    `contract_nif` varchar(15) COLLATE utf8_general_ci NULL  COMMENT 'Guardar sin espacios ni puntos ni guiones' ,
    `phone` varchar(20) COLLATE utf8_general_ci NULL  COMMENT 'guardar talcual' ,
    `contract_email` varchar(255) COLLATE utf8_general_ci NULL  ,
    `address` tinytext COLLATE utf8_general_ci NULL  ,
    `zipcode` varchar(10) COLLATE utf8_general_ci NULL  ,
    `location` varchar(255) COLLATE utf8_general_ci NULL  ,
    `country` varchar(50) COLLATE utf8_general_ci NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Contiene nombre de archivo' ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `motivation` text COLLATE utf8_general_ci NULL  ,
    `video` varchar(256) COLLATE utf8_general_ci NULL  ,
    `video_usubs` int(1) NOT NULL  DEFAULT 0 ,
    `about` text COLLATE utf8_general_ci NULL  ,
    `goal` text COLLATE utf8_general_ci NULL  ,
    `related` text COLLATE utf8_general_ci NULL  ,
    `spread` text COLLATE utf8_general_ci NULL  ,
    `reward` text COLLATE utf8_general_ci NULL  ,
    `category` varchar(50) COLLATE utf8_general_ci NULL  ,
    `keywords` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Separadas por comas' ,
    `media` varchar(256) COLLATE utf8_general_ci NULL  ,
    `media_usubs` int(1) NOT NULL  DEFAULT 0 ,
    `currently` int(1) NULL  ,
    `project_location` varchar(256) COLLATE utf8_general_ci NULL  ,
    `scope` int(1) NULL  COMMENT 'Ambito de alcance' ,
    `resource` text COLLATE utf8_general_ci NULL  ,
    `comment` text COLLATE utf8_general_ci NULL  COMMENT 'Comentario para los admin' ,
    `contract_entity` int(1) NOT NULL  DEFAULT 0 ,
    `contract_birthdate` date NULL  ,
    `entity_office` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Cargo del responsable' ,
    `entity_name` varchar(255) COLLATE utf8_general_ci NULL  ,
    `entity_cif` varchar(10) COLLATE utf8_general_ci NULL  COMMENT 'Guardar sin espacios ni puntos ni guiones' ,
    `post_address` tinytext COLLATE utf8_general_ci NULL  ,
    `secondary_address` int(11) NOT NULL  DEFAULT 0 ,
    `post_zipcode` varchar(10) COLLATE utf8_general_ci NULL  ,
    `post_location` varchar(255) COLLATE utf8_general_ci NULL  ,
    `post_country` varchar(50) COLLATE utf8_general_ci NULL  ,
    `amount_users` int(10) unsigned NULL  COMMENT 'Recaudación proveniente de los usuarios' ,
    `amount_call` int(10) unsigned NULL  COMMENT 'Recaudación proveniente de la convocatoria' ,
    `maxproj` int(5) NULL  COMMENT 'Dinero que puede conseguir un proyecto de la convocatoria' ,
    PRIMARY KEY (`id`) ,
    KEY `owner`(`owner`) ,
    KEY `nodo`(`node`) ,
    KEY `estado`(`status`) ,
    CONSTRAINT `project_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE ,
    CONSTRAINT `project_ibfk_2`
    FOREIGN KEY (`owner`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Proyectos de la plataforma';


/* Create table in target */
CREATE TABLE `project_account`(
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `bank` tinytext COLLATE utf8_general_ci NULL  ,
    `bank_owner` tinytext COLLATE utf8_general_ci NULL  ,
    `paypal` tinytext COLLATE utf8_general_ci NULL  ,
    `paypal_owner` tinytext COLLATE utf8_general_ci NULL  ,
    `allowpp` int(1) NULL  ,
    `fee` int(1) NOT NULL  DEFAULT 4 COMMENT 'porcentaje de comisión goteo' ,
    PRIMARY KEY (`project`) ,
    CONSTRAINT `project_account_ibfk_1`
    FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Cuentas bancarias de proyecto';


/* Create table in target */
CREATE TABLE `project_category`(
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `category` bigint(20) unsigned NOT NULL  ,
    UNIQUE KEY `project_category`(`project`,`category`) ,
    KEY `category`(`category`) ,
    KEY `project`(`project`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Categorias de los proyectos';


/* Create table in target */
CREATE TABLE `project_conf`(
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `noinvest` int(1) NOT NULL  DEFAULT 0 COMMENT 'No se permiten más aportes' ,
    `watch` tinyint(1) NOT NULL  DEFAULT 0 COMMENT 'Vigilar el proyecto' ,
    `days_round1` int(4) NULL  DEFAULT 40 COMMENT 'Días que dura la primera ronda desde la publicación del proyecto' ,
    `days_round2` int(4) NULL  DEFAULT 40 COMMENT 'Días que dura la segunda ronda desde la publicación del proyecto' ,
    `one_round` tinyint(1) NOT NULL  DEFAULT 0 COMMENT 'Si el proyecto tiene una unica ronda' ,
    `help_license` tinyint(1) NOT NULL  DEFAULT 0 COMMENT 'Si necesita ayuda en licencias' ,
    `help_cost` tinyint(1) NOT NULL  DEFAULT 0 COMMENT 'Si necesita ayuda en costes' ,
    PRIMARY KEY (`project`) ,
    CONSTRAINT `project_conf_ibfk_1`
    FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Configuraciones para proyectos';


/* Create table in target */
CREATE TABLE `project_data`(
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `updated` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP ,
    `invested` int(6) unsigned NOT NULL  DEFAULT 0 COMMENT 'Mostrado en termometro al cerrar' ,
    `fee` int(6) unsigned NOT NULL  DEFAULT 0 COMMENT 'comisiones cobradas por bancos y paypal a goteo' ,
    `issue` int(6) unsigned NOT NULL  DEFAULT 0 COMMENT 'importe de las incidencias' ,
    `amount` int(6) unsigned NOT NULL  DEFAULT 0 COMMENT 'recaudaro realmente' ,
    `goteo` int(6) unsigned NOT NULL  DEFAULT 0 COMMENT 'comision goteo' ,
    `percent` int(1) unsigned NOT NULL  DEFAULT 8 COMMENT 'porcentaje comision goteo' ,
    `comment` text COLLATE utf8_general_ci NULL  COMMENT 'comentarios y/o listado de incidencias' ,
    PRIMARY KEY (`project`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='datos de informe financiero';


/* Create table in target */
CREATE TABLE `project_image`(
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NOT NULL  DEFAULT '' COMMENT 'Contiene nombre de archivo' ,
    `section` varchar(50) COLLATE utf8_general_ci NULL  ,
    `url` tinytext COLLATE utf8_general_ci NULL  ,
    `order` tinyint(4) NULL  ,
    PRIMARY KEY (`project`,`image`) ,
    KEY `proyecto-seccion`(`project`,`section`) ,
    CONSTRAINT `project_image_ibfk_1`
    FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `project_lang`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `motivation` text COLLATE utf8_general_ci NULL  ,
    `video` varchar(256) COLLATE utf8_general_ci NULL  ,
    `about` text COLLATE utf8_general_ci NULL  ,
    `goal` text COLLATE utf8_general_ci NULL  ,
    `related` text COLLATE utf8_general_ci NULL  ,
    `reward` text COLLATE utf8_general_ci NULL  ,
    `keywords` tinytext COLLATE utf8_general_ci NULL  ,
    `media` varchar(255) COLLATE utf8_general_ci NULL  ,
    `subtitle` tinytext COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `project_location`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `latitude` decimal(16,14) NOT NULL  ,
    `longitude` decimal(16,14) NOT NULL  ,
    `method` varchar(50) COLLATE utf8_general_ci NOT NULL  DEFAULT 'ip' ,
    `locable` tinyint(1) NOT NULL  DEFAULT 0 ,
    `city` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `region` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `country` varchar(150) COLLATE utf8_general_ci NOT NULL  ,
    `country_code` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `info` varchar(255) COLLATE utf8_general_ci NULL  ,
    `modified` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    PRIMARY KEY (`id`) ,
    KEY `latitude`(`latitude`) ,
    KEY `longitude`(`longitude`) ,
    KEY `locable`(`locable`) ,
    CONSTRAINT `project_location_ibfk_1`
    FOREIGN KEY (`id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `project_milestone`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `milestone` int(12) NULL  ,
    `date` date NULL  ,
    `post` int(12) NULL  ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Project milestones';


/* Create table in target */
CREATE TABLE `project_open_tag`(
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `open_tag` int(12) NOT NULL  ,
    UNIQUE KEY `project_open_tag`(`project`,`open_tag`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Agrupacion de los proyectos';


/* Create table in target */
CREATE TABLE `promote`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `order` smallint(5) unsigned NOT NULL  DEFAULT 1 ,
    `active` int(1) NOT NULL  DEFAULT 0 ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `project_node`(`node`,`project`) ,
    UNIQUE KEY `id`(`id`) ,
    KEY `activos`(`active`) ,
    KEY `project`(`project`) ,
    CONSTRAINT `promote_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE ,
    CONSTRAINT `promote_ibfk_2`
    FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Proyectos destacados';


/* Create table in target */
CREATE TABLE `promote_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`) ,
    CONSTRAINT `promote_lang_ibfk_1`
    FOREIGN KEY (`id`) REFERENCES `promote` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `purpose`(
    `text` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `purpose` text COLLATE utf8_general_ci NOT NULL  ,
    `html` tinyint(1) NULL  COMMENT 'Si el texto lleva formato html' ,
    `group` varchar(50) COLLATE utf8_general_ci NOT NULL  DEFAULT 'general' COMMENT 'Agrupacion de uso' ,
    PRIMARY KEY (`text`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Explicación del propósito de los textos';


/* Create table in target */
CREATE TABLE `purpose_copy`(
    `text` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `purpose` text COLLATE utf8_general_ci NOT NULL  ,
    `html` tinyint(1) NULL  COMMENT 'Si el texto lleva formato html' ,
    `group` varchar(50) COLLATE utf8_general_ci NOT NULL  DEFAULT 'general' COMMENT 'Agrupacion de uso' ,
    PRIMARY KEY (`text`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Explicación del propósito de los textos';


/* Create table in target */
CREATE TABLE `review`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `status` tinyint(1) NOT NULL  DEFAULT 1 ,
    `to_checker` text COLLATE utf8_general_ci NULL  ,
    `to_owner` text COLLATE utf8_general_ci NULL  ,
    `score` int(2) NOT NULL  DEFAULT 0 ,
    `max` int(2) NOT NULL  DEFAULT 0 ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Revision para evaluacion de proyecto';


/* Create table in target */
CREATE TABLE `review_comment`(
    `review` bigint(20) unsigned NOT NULL  ,
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `section` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `evaluation` text COLLATE utf8_general_ci NULL  ,
    `recommendation` text COLLATE utf8_general_ci NULL  ,
    `date` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP ,
    PRIMARY KEY (`review`,`user`,`section`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Comentarios de revision';


/* Create table in target */
CREATE TABLE `review_score`(
    `review` bigint(20) unsigned NOT NULL  ,
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `criteria` bigint(20) unsigned NOT NULL  ,
    `score` tinyint(1) NULL  ,
    PRIMARY KEY (`review`,`user`,`criteria`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Puntuacion por citerio';


/* Create table in target */
CREATE TABLE `reward`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `reward` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `type` varchar(50) COLLATE utf8_general_ci NULL  ,
    `icon` varchar(50) COLLATE utf8_general_ci NULL  ,
    `other` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Otro tipo de recompensa' ,
    `license` varchar(50) COLLATE utf8_general_ci NULL  ,
    `amount` int(5) NULL  ,
    `units` int(5) NULL  ,
    `fulsocial` tinyint(1) NOT NULL  DEFAULT 0 COMMENT 'Retorno colectivo cumplido' ,
    `url` tinytext COLLATE utf8_general_ci NULL  COMMENT 'Localización del Retorno cumplido' ,
    `order` tinyint(4) NOT NULL  DEFAULT 1 COMMENT 'Orden para retornos colectivos' ,
    `bonus` tinyint(1) NOT NULL  DEFAULT 0 COMMENT 'Retorno colectivo adicional' ,
    PRIMARY KEY (`id`) ,
    KEY `project`(`project`) ,
    KEY `icon`(`icon`) ,
    KEY `type`(`type`) ,
    KEY `order`(`order`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Retornos colectivos e individuales';


/* Create table in target */
CREATE TABLE `reward_lang`(
    `id` int(20) NOT NULL  ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `reward` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `other` tinytext COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`) ,
    KEY `project`(`project`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `role`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `name` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `sponsor`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `name` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `url` tinytext COLLATE utf8_general_ci NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Contiene nombre de archivo' ,
    `order` int(11) NOT NULL  DEFAULT 1 ,
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    PRIMARY KEY (`id`) ,
    KEY `node`(`node`) ,
    CONSTRAINT `sponsor_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Patrocinadores';


/* Create table in target */
CREATE TABLE `stories`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `project` varchar(50) COLLATE utf8_general_ci NULL  ,
    `order` smallint(5) unsigned NOT NULL  DEFAULT 1 ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Contiene nombre de archivo' ,
    `active` int(1) NOT NULL  DEFAULT 0 ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `review` text COLLATE utf8_general_ci NULL  ,
    `url` tinytext COLLATE utf8_general_ci NULL  ,
    `post` bigint(20) unsigned NULL  ,
    `pool_image` varchar(255) COLLATE utf8_general_ci NULL  ,
    `pool` int(1) NOT NULL  DEFAULT 0 ,
    `text_position` varchar(50) COLLATE utf8_general_ci NULL  ,
    PRIMARY KEY (`id`) ,
    KEY `node`(`node`) ,
    CONSTRAINT `stories_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Historias existosas';


/* Create table in target */
CREATE TABLE `stories_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `review` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `support`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `support` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `type` varchar(50) COLLATE utf8_general_ci NULL  ,
    `thread` bigint(20) unsigned NULL  COMMENT 'De la tabla message' ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`) ,
    KEY `hilo`(`thread`) ,
    KEY `proyecto`(`project`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Colaboraciones';


/* Create table in target */
CREATE TABLE `support_lang`(
    `id` int(20) NOT NULL  ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `support` tinytext COLLATE utf8_general_ci NULL  ,
    `description` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`) ,
    KEY `project`(`project`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `tag`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `name` tinytext COLLATE utf8_general_ci NOT NULL  ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Tags de blogs (de nodo)';


/* Create table in target */
CREATE TABLE `tag_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `template`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `name` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `group` varchar(50) COLLATE utf8_general_ci NOT NULL  DEFAULT 'general' COMMENT 'Agrupación de uso' ,
    `purpose` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `text` text COLLATE utf8_general_ci NOT NULL  ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Plantillas emails automáticos';


/* Create table in target */
CREATE TABLE `template_lang`(
    `id` bigint(20) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `title` tinytext COLLATE utf8_general_ci NULL  ,
    `text` text COLLATE utf8_general_ci NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    PRIMARY KEY (`id`,`lang`) ,
    CONSTRAINT `template_lang_ibfk_1`
    FOREIGN KEY (`id`) REFERENCES `template` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `text`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  DEFAULT 'es' ,
    `text` text COLLATE utf8_general_ci NOT NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    PRIMARY KEY (`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Textos multi-idioma';


/* Create table in target */
CREATE TABLE `user`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `name` varchar(100) COLLATE utf8_general_ci NOT NULL  ,
    `location` varchar(255) COLLATE utf8_general_ci NULL  ,
    `email` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `password` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `gender` char(1) COLLATE utf8_general_ci NULL  ,
    `birthyear` year(4) NULL  ,
    `entity_type` tinyint(1) NULL  ,
    `legal_entity` tinyint(1) NULL  ,
    `about` text COLLATE utf8_general_ci NULL  ,
    `keywords` tinytext COLLATE utf8_general_ci NULL  ,
    `active` tinyint(1) NOT NULL  ,
    `avatar` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Contiene nombre de archivo' ,
    `contribution` text COLLATE utf8_general_ci NULL  ,
    `twitter` tinytext COLLATE utf8_general_ci NULL  ,
    `facebook` tinytext COLLATE utf8_general_ci NULL  ,
    `google` tinytext COLLATE utf8_general_ci NULL  ,
    `identica` tinytext COLLATE utf8_general_ci NULL  ,
    `linkedin` tinytext COLLATE utf8_general_ci NULL  ,
    `amount` int(7) NULL  COMMENT 'Cantidad total aportada' ,
    `num_patron` int(10) unsigned NULL  COMMENT 'Num. proyectos patronizados' ,
    `num_patron_active` int(10) unsigned NULL  COMMENT 'Num. proyectos patronizados activos' ,
    `worth` int(7) NULL  ,
    `created` timestamp NULL  ,
    `modified` timestamp NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    `token` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `hide` tinyint(1) NOT NULL  DEFAULT 0 COMMENT 'No se ve publicamente' ,
    `confirmed` int(1) NOT NULL  DEFAULT 0 ,
    `lang` varchar(2) COLLATE utf8_general_ci NULL  DEFAULT 'es' ,
    `node` varchar(50) COLLATE utf8_general_ci NULL  ,
    `num_invested` int(10) unsigned NULL  COMMENT 'Num. proyectos cofinanciados' ,
    `num_owned` int(10) unsigned NULL  COMMENT 'Num. proyectos publicados' ,
    PRIMARY KEY (`id`) ,
    KEY `nodo`(`node`) ,
    KEY `coordenadas`(`location`) ,
    CONSTRAINT `user_ibfk_1`
    FOREIGN KEY (`node`) REFERENCES `node` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `user_api`(
    `user_id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `key` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `expiration_date` datetime NULL  ,
    PRIMARY KEY (`user_id`) ,
    CONSTRAINT `user_api_ibfk_1`
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `user_call`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `call` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    PRIMARY KEY (`user`,`call`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Asignacion de convocatorias a admines';


/* Create table in target */
CREATE TABLE `user_donation`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `amount` int(11) NOT NULL  ,
    `name` varchar(255) COLLATE utf8_general_ci NULL  ,
    `surname` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Apellido' ,
    `nif` varchar(12) COLLATE utf8_general_ci NULL  ,
    `address` tinytext COLLATE utf8_general_ci NULL  ,
    `zipcode` varchar(10) COLLATE utf8_general_ci NULL  ,
    `location` varchar(255) COLLATE utf8_general_ci NULL  ,
    `region` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Provincia' ,
    `country` varchar(50) COLLATE utf8_general_ci NULL  ,
    `countryname` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Nombre del pais' ,
    `numproj` int(2) NULL  DEFAULT 1 ,
    `year` varchar(4) COLLATE utf8_general_ci NOT NULL  ,
    `edited` int(1) NULL  DEFAULT 0 COMMENT 'Revisados por el usuario' ,
    `confirmed` int(1) NULL  DEFAULT 0 COMMENT 'Certificado generado' ,
    `pdf` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'nombre del archivo de certificado' ,
    PRIMARY KEY (`user`,`year`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Datos fiscales donativo';


/* Create table in target */
CREATE TABLE `user_favourite_project`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `date_send` date NULL  ,
    `date_marked` date NULL  ,
    UNIQUE KEY `user_favourite_project`(`user`,`project`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='User favourites projects';


/* Create table in target */
CREATE TABLE `user_interest`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `interest` int(12) NOT NULL  ,
    UNIQUE KEY `user_interest`(`user`,`interest`) ,
    KEY `usuario`(`user`) ,
    KEY `interes`(`interest`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Intereses de los usuarios';


/* Create table in target */
CREATE TABLE `user_lang`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `about` text COLLATE utf8_general_ci NULL  ,
    `name` varchar(100) COLLATE utf8_general_ci NULL  ,
    `keywords` tinytext COLLATE utf8_general_ci NULL  ,
    `contribution` text COLLATE utf8_general_ci NULL  ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `user_location`(
    `id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `latitude` decimal(16,14) NOT NULL  ,
    `longitude` decimal(16,14) NOT NULL  ,
    `method` varchar(50) COLLATE utf8_general_ci NOT NULL  DEFAULT 'ip' ,
    `locable` tinyint(1) NOT NULL  DEFAULT 0 ,
    `city` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `region` varchar(255) COLLATE utf8_general_ci NOT NULL  ,
    `country` varchar(150) COLLATE utf8_general_ci NOT NULL  ,
    `country_code` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `info` varchar(255) COLLATE utf8_general_ci NULL  ,
    `modified` timestamp NOT NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP ,
    PRIMARY KEY (`id`) ,
    KEY `latitude`(`latitude`) ,
    KEY `longitude`(`longitude`) ,
    KEY `locable`(`locable`) ,
    CONSTRAINT `user_location_ibfk_1`
    FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `user_login`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `provider` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `oauth_token` text COLLATE utf8_general_ci NOT NULL  ,
    `oauth_token_secret` text COLLATE utf8_general_ci NOT NULL  ,
    `datetime` timestamp NULL  DEFAULT CURRENT_TIMESTAMP ,
    PRIMARY KEY (`user`,`oauth_token`(255)) ,
    CONSTRAINT `user_login_ibfk_1`
    FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `user_node`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `node` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    PRIMARY KEY (`user`,`node`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `user_personal`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `contract_name` varchar(255) COLLATE utf8_general_ci NULL  ,
    `contract_surname` varchar(255) COLLATE utf8_general_ci NULL  ,
    `contract_nif` varchar(15) COLLATE utf8_general_ci NULL  COMMENT 'Guardar sin espacios ni puntos ni guiones' ,
    `contract_email` varchar(256) COLLATE utf8_general_ci NULL  ,
    `phone` varchar(9) COLLATE utf8_general_ci NULL  COMMENT 'guardar sin espacios ni puntos' ,
    `address` tinytext COLLATE utf8_general_ci NULL  ,
    `zipcode` varchar(10) COLLATE utf8_general_ci NULL  ,
    `location` varchar(255) COLLATE utf8_general_ci NULL  ,
    `country` varchar(50) COLLATE utf8_general_ci NULL  ,
    PRIMARY KEY (`user`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Datos personales de usuario';


/* Create table in target */
CREATE TABLE `user_pool`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `amount` int(7) unsigned NOT NULL  DEFAULT 0 ,
    PRIMARY KEY (`user`) ,
    CONSTRAINT `user_pool_ibfk_1`
    FOREIGN KEY (`user`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `user_prefer`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `updates` int(1) NOT NULL  DEFAULT 0 ,
    `threads` int(1) NOT NULL  DEFAULT 0 ,
    `rounds` int(1) NOT NULL  DEFAULT 0 ,
    `mailing` int(1) NOT NULL  DEFAULT 0 ,
    `email` int(1) NOT NULL  DEFAULT 0 ,
    `tips` int(1) NOT NULL  DEFAULT 0 ,
    `comlang` varchar(2) COLLATE utf8_general_ci NULL  ,
    `currency` varchar(3) COLLATE utf8_general_ci NULL  ,
    PRIMARY KEY (`user`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Preferencias de notificacion de usuario';


/* Create table in target */
CREATE TABLE `user_project`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `project` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    UNIQUE KEY `user`(`user`,`project`) ,
    KEY `project`(`project`) ,
    CONSTRAINT `user_project_ibfk_1`
    FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE ,
    CONSTRAINT `user_project_ibfk_2`
    FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `user_review`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `review` bigint(20) unsigned NOT NULL  ,
    `ready` tinyint(1) NOT NULL  DEFAULT 0 COMMENT 'Ha terminado con la revision' ,
    PRIMARY KEY (`user`,`review`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Asignacion de revision a usuario';


/* Create table in target */
CREATE TABLE `user_role`(
    `user_id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `role_id` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `node_id` varchar(50) COLLATE utf8_general_ci NULL  ,
    `datetime` timestamp NULL  DEFAULT CURRENT_TIMESTAMP ,
    KEY `user_FK`(`user_id`) ,
    KEY `role_FK`(`role_id`) ,
    KEY `node_FK`(`node_id`) ,
    CONSTRAINT `user_role_ibfk_1`
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE ,
    CONSTRAINT `user_role_ibfk_2`
    FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE ,
    CONSTRAINT `user_role_ibfk_3`
    FOREIGN KEY (`node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Create table in target */
CREATE TABLE `user_translang`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    PRIMARY KEY (`user`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Idiomas de traductores';


/* Create table in target */
CREATE TABLE `user_translate`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `type` varchar(10) COLLATE utf8_general_ci NOT NULL  COMMENT 'Tipo de contenido' ,
    `item` varchar(50) COLLATE utf8_general_ci NOT NULL  COMMENT 'id del contenido' ,
    `ready` tinyint(1) NOT NULL  DEFAULT 0 COMMENT 'Ha terminado con la traduccion' ,
    PRIMARY KEY (`user`,`type`,`item`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Asignacion de traduccion a usuario';


/* Create table in target */
CREATE TABLE `user_vip`(
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `image` varchar(255) COLLATE utf8_general_ci NULL  COMMENT 'Contiene nombre de archivo' ,
    PRIMARY KEY (`user`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Datos usuario colaborador';


/* Create table in target */
CREATE TABLE `user_web`(
    `id` bigint(20) unsigned NOT NULL  auto_increment ,
    `user` varchar(50) COLLATE utf8_general_ci NOT NULL  ,
    `url` tinytext COLLATE utf8_general_ci NOT NULL  ,
    PRIMARY KEY (`id`) ,
    UNIQUE KEY `id`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Webs de los usuarios';


/* Create table in target */
CREATE TABLE `worthcracy`(
    `id` int(2) NOT NULL  auto_increment ,
    `name` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `amount` int(6) NOT NULL  ,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci' COMMENT='Niveles de meritocracia';


/* Create table in target */
CREATE TABLE `worthcracy_lang`(
    `id` int(2) unsigned NOT NULL  ,
    `lang` varchar(2) COLLATE utf8_general_ci NOT NULL  ,
    `name` tinytext COLLATE utf8_general_ci NOT NULL  ,
    `pending` int(1) NULL  DEFAULT 0 COMMENT 'Debe revisarse la traducción' ,
    UNIQUE KEY `id_lang`(`id`,`lang`)
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';

/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
