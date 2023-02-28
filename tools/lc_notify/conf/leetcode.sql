CREATE TABLE `user_lc_daily_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(128) NOT NULL DEFAULT '',
  `total_solve` int NOT NULL DEFAULT '0',
  `code_submit` int NOT NULL DEFAULT '0',
  `problem_submit` int NOT NULL DEFAULT '0',
  `rating_score` int NOT NULL DEFAULT '0',
  `continue_days` int NOT NULL DEFAULT '0',
  `new_solve` int NOT NULL DEFAULT '0',
  `date_time` datetime NOT NULL,
  `lazy_days` int NOT NULL DEFAULT '0',
  `total_days` int NOT NULL DEFAULT '0',
  `hard_num` int NOT NULL DEFAULT '0',
  `mid_num` int NOT NULL DEFAULT '0',
  `easy_num` int NOT NULL DEFAULT '0',
  `hard_total` int NOT NULL DEFAULT '0',
  `mid_total` int NOT NULL DEFAULT '0',
  `easy_total` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_date_time` (`date_time`),
  KEY `idx_user` (`user`)
) ENGINE=InnoDB AUTO_INCREMENT=8809 DEFAULT CHARSET=utf8mb3

CREATE TABLE `account_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(128) NOT NULL DEFAULT '',
  `git_account` varchar(128) NOT NULL DEFAULT '',
  `medal` int NOT NULL DEFAULT '0',
  `award` int NOT NULL DEFAULT '0',
  `email` varchar(128) NOT NULL DEFAULT '',
  `date_time` datetime DEFAULT NULL,
  `coins` int NOT NULL DEFAULT '100',
  `status` int NOT NULL DEFAULT '0',
  `token` varchar(20) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user` (`user`)
) ENGINE=InnoDB AUTO_INCREMENT=194 DEFAULT CHARSET=utf8mb3

CREATE TABLE `feedback_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` varchar(2048) NOT NULL DEFAULT '',
  `date_time` datetime NOT NULL,
  `status` int NOT NULL DEFAULT '0',
  `answer` varchar(1024) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb3

CREATE TABLE `user_target_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(128) NOT NULL DEFAULT '',
  `target_type` int NOT NULL DEFAULT '0',
  `target_value` int NOT NULL DEFAULT '0',
  `opponent` varchar(128) NOT NULL DEFAULT '',
  `status` int NOT NULL DEFAULT '0',
  `create_date` datetime NOT NULL,
  `dead_line` datetime NOT NULL,
  `level` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=185 DEFAULT CHARSET=utf8mb3

CREATE TABLE `rand_problem_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(128) NOT NULL DEFAULT '',
  `lc_number` int NOT NULL DEFAULT '0',
  `status` int NOT NULL DEFAULT '0',
  `coins` int NOT NULL DEFAULT '0',
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=205 DEFAULT CHARSET=utf8mb3

-- type: Java, C++, 操作系统，计算机网络，mysql，redis，mq，并发编程，分布式系统，算法编程
-- company: 出题公司
CREATE TABLE `interview_problem_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` varchar(1024) NOT NULL DEFAULT '',
  `answer` varchar(2048) NOT NULL DEFAULT '',
  `type` varchar(128) NOT NULL DEFAULT '',
  `company` varchar(128) NOT NULL DEFAULT '',
  `jd` varchar(128) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `idx_type` (`type`),
  KEY `idx_company` (`company`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb3 