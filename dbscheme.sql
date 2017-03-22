CREATE TABLE users (
  id INTEGER NOT NULL PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  middle_name TEXT,
  email TEXT,
  password TEXT,
  date_of_birth TEXT,
  diagnosis INT,
  date_of_diagnosis TEXT,
  additional_info TEXT,
  admin_role INT DEFAULT 0
);

CREATE TABLE tasks (
  id INTEGER NOT NULL PRIMARY KEY,
  name TEXT,
  alias TEXT,
  task_markup TEXT,
  subjects_list TEXT
);

CREATE TABLE sessions (
  id INTEGER NOT NULL PRIMARY KEY,
  task_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  time INTEGER,
  result REAL,
  task_type TEXT,
  FOREIGN KEY (task_id) REFERENCES tasks (id),
  FOREIGN KEY (user_id) REFERENCES users (id)
);



