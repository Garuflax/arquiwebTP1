--TODO not admin user data
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL,
  is_admin BOOLEAN NOT NULL
);

--TODO Geoposition and QR
CREATE TABLE location (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  maximum_capacity INTEGER NOT NULL,
  people_inside INTEGER DEFAULT 0,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
