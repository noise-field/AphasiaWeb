CREATE TABLE patients (
  id INTEGER NOT NULL PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  middle_name TEXT,
  email TEXT,
  password TEXT,
  date_of_birth TEXT,
  diagnosis INT,
  date_of_diagnosis TEXT,
  additional_info TEXT
);