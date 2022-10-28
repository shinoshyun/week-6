USE member_data;
SHOW TABLES;
DROP TABLE membership;

CREATE TABLE membership(
	id bigint PRIMARY KEY AUTO_INCREMENT,
	name varchar(255) NOT NULL,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL
);

SELECT * FROM membership;