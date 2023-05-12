BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `word` (
	`word1`	TEXT,
	`word2`	TEXT
);
INSERT INTO `word` VALUES ('calamity','cataclysm');
INSERT INTO `word` VALUES ('cataclysm','calamity');
INSERT INTO `word` VALUES ('calamity','catastrophe');
INSERT INTO `word` VALUES ('catastrophe','calamity');
INSERT INTO `word` VALUES ('catastrophe','cataclysm');
INSERT INTO `word` VALUES ('cataclysm','catastrophe');
COMMIT;
