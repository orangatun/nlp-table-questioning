DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS file;
DROP TABLE IF EXISTS question;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE file (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  uploaded TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  file_name TEXT NOT NULL,
  file_path TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE question (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  req_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  question TEXT NOT NULL,
  response TEXT NOT NULL,
  file_id INTEGER NOT NULL,
  FOREIGN KEY (file_id) REFERENCES file (id)
);