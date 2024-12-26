PRAGMA foreign_keys = ON;

CREATE TABLE users(
	userid INTEGER NOT NULL,
	email VARCHAR(50) NOT NULL,
	completed VARCHAR(5) NOT NULL,
	currentq INTEGER NOT NULL,
	password CHARACTER (256) NOT NULL,
	age INTEGER NOT NULL,
  gender VARCHAR(50),
  orientation VARCHAR(50),
  aclevel VARCHAR(50),
  acfield VARCHAR(50),
  isLGBT VARCHAR(50),
  tutorial VARCHAR(50),
  type VARCHAR(50),
  PRIMARY KEY (userid)
);

CREATE TABLE response(
	userid INTEGER NOT NULL,
	q_id INTEGER NOT NULL,
  local_id VARCHAR(50),
	starttime DOUBLE NOT NULL,
	endtime DOUBLE,
	answer VARCHAR(50),
  lines VARCHAR(250),
	PRIMARY KEY (q_id, userid)
);
