/* Made by Hyungsuk Yoon */
/* Last Modified 20130703 05:35 */


CREATE DATABASE IF NOT EXISTS `garagestory` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `garagestory`;

DROP TABLE IF EXISTS singlo_lesson_answer;
DROP TABLE IF EXISTS singlo_lesson_question;
DROP TABLE IF EXISTS singlo_lesson_symptom;
DROP TABLE IF EXISTS singlo_lesson_training;
DROP TABLE IF EXISTS singlo_user_teacher_like;
DROP TABLE IF EXISTS singlo_user;
DROP TABLE IF EXISTS singlo_teacher;

CREATE TABLE singlo_user ( 
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(31) NOT NULL,
	`phone` VARCHAR(31) NOT NULL,
	`email` VARCHAR(63) NOT NULL,
	`password` VARCHAR(63) NOT NULL,
	`photo` VARCHAR(63) DEFAULT NULL,
	`created_datetime` DATETIME NOT NULL,
	`lastlogin_datetime` DATETIME NOT NULL,
	`pushtoken` VARCHAR(100) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE singlo_teacher (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(31) NOT NULL,
	`phone` VARCHAR(31) NOT NULL,
	`email` VARCHAR(63) NOT NULL,
	`password` VARCHAR(63) NOT NULL,
	`photo` VARCHAR(63) DEFAULT NULL,
	`company` VARCHAR(63) NOT NULL,
	`certification` VARCHAR(63) NOT NULL,
	`lessons` VARCHAR(63) NOT NULL,
	`video_available` TINYINT(1) NOT NULL DEFAULT 0, /* Video Lesson X/O */
	`price` INT NOT NULL,
	`profile` TEXT NOT NULL,
	`url` VARCHAR(127) NOT NULL,
	`created_datetime` DATETIME NOT NULL,
	`lastlogin_datetime` DATETIME NOT NULL,
	`pushtoken` VARCHAR(100) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE singlo_user_teacher_like (
	`user_id` INT NOT NULL,
	`teacher_id` INT NOT NULL,
	`status` TINYINT(1) NOT NULL DEFAULT 0,
	`created_datetime` DATETIME NOT NULL,
	PRIMARY KEY (`user_id`, `teacher_id`),
	FOREIGN KEY (`user_id`) REFERENCES singlo_user(`id`) ON DELETE CASCADE,
	FOREIGN KEY (`teacher_id`) REFERENCES singlo_teacher(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
	

CREATE TABLE singlo_lesson_symptom (
	`id` INT NOT NULL AUTO_INCREMENT,
	`group` VARCHAR(127) NOT NULL,
	`title` VARCHAR(127) NOT NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE singlo_lesson_training (
	`id` INT NOT NULL AUTO_INCREMENT,
	`title` VARCHAR(127) NOT NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



CREATE TABLE singlo_lesson_question (
	`id` INT NOT NULL AUTO_INCREMENT,
	`user_id` INT NOT NULL,
	`teacher_id` INT DEFAULT NULL,
	`status` TINYINT(1) NOT NULL DEFAULT 0, /* Waiting or Finish */
	`lesson_type` TINYINT(1) NOT NULL, /* Video or Message */
	`video` VARCHAR(63) DEFAULT NULL,
	`club_type` TINYINT NOT NULL,
	`question` TEXT NOT NULL,
	`created_datetime` DATETIME NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`user_id`) REFERENCES singlo_user(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE singlo_lesson_answer (
	`id` INT NOT NULL AUTO_INCREMENT,
	`question_id` INT NOT NULL,
	`score_address` TINYINT NOT NULL,
	`score_backswing` TINYINT NOT NULL,
	`score_top` TINYINT NOT NULL,
	`score_downswing` TINYINT NOT NULL,
	`score_finish` TINYINT NOT NULL,
	`symptom_id` INT NOT NULL,
	`answer` TEXT NOT NULL,
	`video` VARCHAR(63) DEFAULT NULL,
	`training1` INT NOT NULL,
	`training2` INT NOT NULL,
	`created_datetime` DATETIME NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`question_id`) REFERENCES singlo_lesson_question(`id`) ON DELETE CASCADE,
	FOREIGN KEY (`symptom_id`) REFERENCES singlo_lesson_symptom(`id`) ON DELETE CASCADE,
	FOREIGN KEY (`training1`) REFERENCES singlo_lesson_training(`id`) ON DELETE CASCADE,
	FOREIGN KEY (`training2`) REFERENCES singlo_lesson_training(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
	

