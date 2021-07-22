/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 50645
 Source Host           : 127.0.0.1:3306
 Source Schema         : test

 Target Server Type    : MySQL
 Target Server Version : 50645
 File Encoding         : 65001

 Date: 22/07/2021 16:43:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dnf_buylog
-- ----------------------------
DROP TABLE IF EXISTS `dnf_buylog`;
CREATE TABLE `dnf_buylog` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ids_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '角色id',
  `object_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '购买物品id',
  `is_succ` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '是否成功0否1是',
  `buy_snum` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '购买成功数量',
  `buy_scost` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '购买总花费',
  `act_price` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '实际单价',
  `seting_price` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '配置单价',
  `create_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of dnf_buylog
-- ----------------------------
BEGIN;
INSERT INTO `dnf_buylog` VALUES (1, 1, 1, 1, 1, 3, 4, 5, '2021-07-22 08:31:26');
COMMIT;

-- ----------------------------
-- Table structure for dnf_gzone
-- ----------------------------
DROP TABLE IF EXISTS `dnf_gzone`;
CREATE TABLE `dnf_gzone` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `gzone_name` varchar(255) NOT NULL DEFAULT '' COMMENT '区服名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COMMENT='区服表';

-- ----------------------------
-- Records of dnf_gzone
-- ----------------------------
BEGIN;
INSERT INTO `dnf_gzone` VALUES (1, '西南一区');
INSERT INTO `dnf_gzone` VALUES (2, '广东一区');
COMMIT;

-- ----------------------------
-- Table structure for dnf_ids
-- ----------------------------
DROP TABLE IF EXISTS `dnf_ids`;
CREATE TABLE `dnf_ids` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `gzone_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '区服id',
  `idimg` varchar(255) NOT NULL DEFAULT '' COMMENT '角色图片',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='账号表';

-- ----------------------------
-- Records of dnf_ids
-- ----------------------------
BEGIN;
INSERT INTO `dnf_ids` VALUES (1, 1, './dnfimg/屠夫.bmp');
INSERT INTO `dnf_ids` VALUES (2, 1, './dnfimg/神的.bmp');
INSERT INTO `dnf_ids` VALUES (3, 2, './dnfimg/百思不得.bmp');
COMMIT;

-- ----------------------------
-- Table structure for dnf_object
-- ----------------------------
DROP TABLE IF EXISTS `dnf_object`;
CREATE TABLE `dnf_object` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `gzone_id` int(10) unsigned NOT NULL COMMENT '区服id',
  `object_name` varchar(255) NOT NULL DEFAULT '' COMMENT '物品名称',
  `sell_price` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '销售价',
  `buy_price` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '购买价',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COMMENT='物品表';

-- ----------------------------
-- Records of dnf_object
-- ----------------------------
BEGIN;
INSERT INTO `dnf_object` VALUES (1, 1, '无色小晶体', 52, 50);
INSERT INTO `dnf_object` VALUES (2, 2, '无色小晶体', 55, 53);
COMMIT;

-- ----------------------------
-- Table structure for dnf_pricetrend
-- ----------------------------
DROP TABLE IF EXISTS `dnf_pricetrend`;
CREATE TABLE `dnf_pricetrend` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `object_id` int(10) NOT NULL DEFAULT '0' COMMENT '物品id',
  `gzone_id` int(10) NOT NULL DEFAULT '0' COMMENT '游戏区服id',
  `price1` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '销售价1',
  `count1` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '数量1',
  `price2` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '销售价2',
  `count2` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '数量2',
  `price3` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '销售价3',
  `count3` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '数量3',
  `price4` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '销售价4',
  `count4` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '数量4',
  `create_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '统计时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='拍卖行行情表';

-- ----------------------------
-- Records of dnf_pricetrend
-- ----------------------------
BEGIN;
INSERT INTO `dnf_pricetrend` VALUES (1, 1, 1, 1, 1, 3, 4, 5, 4, 5, 6, '2021-07-22 08:34:00');
COMMIT;

-- ----------------------------
-- Table structure for dnf_syslog
-- ----------------------------
DROP TABLE IF EXISTS `dnf_syslog`;
CREATE TABLE `dnf_syslog` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ids_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '角色id',
  `msg` text NOT NULL,
  `create_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of dnf_syslog
-- ----------------------------
BEGIN;
INSERT INTO `dnf_syslog` VALUES (1, 1, '测试', '2021-07-22 07:24:01');
INSERT INTO `dnf_syslog` VALUES (3, 1, '测试', '2021-07-22 07:26:05');
INSERT INTO `dnf_syslog` VALUES (7, 1, '测试', '2021-07-22 07:32:21');
INSERT INTO `dnf_syslog` VALUES (8, 1, '测试', '2021-07-22 07:33:26');
INSERT INTO `dnf_syslog` VALUES (9, 1, '测试', '2021-07-22 07:37:30');
INSERT INTO `dnf_syslog` VALUES (10, 1, '测试', '2021-07-22 08:00:26');
INSERT INTO `dnf_syslog` VALUES (11, 1, '测试3', '2021-07-22 08:00:54');
INSERT INTO `dnf_syslog` VALUES (12, 1, '测试', '2021-07-22 08:06:42');
INSERT INTO `dnf_syslog` VALUES (13, 1, '测试', '2021-07-22 08:06:56');
INSERT INTO `dnf_syslog` VALUES (14, 4294967295, '测试4', '0000-00-00 00:00:00');
INSERT INTO `dnf_syslog` VALUES (15, 4294967295, '1', '0000-00-00 00:00:00');
INSERT INTO `dnf_syslog` VALUES (16, 4294967295, '1', '0000-00-00 00:00:00');
INSERT INTO `dnf_syslog` VALUES (17, 4294967295, '1', '0000-00-00 00:00:00');
INSERT INTO `dnf_syslog` VALUES (18, 1, '测试4', '2021-07-22 08:29:11');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
