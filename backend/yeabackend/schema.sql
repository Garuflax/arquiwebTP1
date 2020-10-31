CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL,
  is_infected BOOLEAN DEFAULT 0,
  being_in_risk_since DATETIME,
  is_admin BOOLEAN NOT NULL,
  current_location INTEGER,
  FOREIGN KEY (current_location) REFERENCES location (id)
);

CREATE TABLE location (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  maximum_capacity INTEGER NOT NULL,
  people_inside INTEGER DEFAULT 0,
  latitude FLOAT NOT NULL,
  longitude FLOAT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE checks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  location_id INTEGER NOT NULL,
  check_in_time DATETIME,
  check_out_time DATETIME,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (location_id) REFERENCES location (id)
);