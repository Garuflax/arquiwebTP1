-- SQLite
INSERT INTO user (username, password, email, is_admin)
VALUES
  ('usertest', 'pbkdf2:sha256:150000$6tjsUGUN$fff35601e39010f1ed7b8dc3b07bac32a8d5af57b2f14cce1d4d953445549a1f', 'user@test.com', 0),
  ('admintest', 'pbkdf2:sha256:150000$7MoD21iF$49d13a6e893e4f18cdfddd82e9240a1207de3df20de38284790c9e91a6bfbbf0', 'admin@test.com', 1),
  ('othertest', 'pbkdf2:sha256:150000$Bph3Imma$63ce0940b378c1bb717eb19dced40a4ef7850cf79963d5019e475cdfd04c3fe9', 'other@test.com', 0),
  ('anothertest', 'pbkdf2:sha256:150000$IAB9BmP4$f4c70e3fe36b6639b0810f037e3da0d0397b65c0c079e02765787fde0317e2b8', 'another@test.com', 0);

INSERT INTO location (name, maximum_capacity, author_id, latitude, longitude)
VALUES
  ('test location 1', 10, 1, 31.0, 61.0),
  ('test location 2', 10, 1, 32.0, 66.0),
  ('test location 3', 10, 1, 33.0, 65.0),
  ('test location 4', 10, 1, 34.0, 64.0),
  ('test location 5', 10, 1, 35.0, 63.0),
  ('test location 6', 10, 1, 36.0, 62.0),
  ('test location 7', 1, 1, 37.0, 61.0);