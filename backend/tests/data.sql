INSERT INTO user (username, password, email, is_admin)
VALUES
  ('usertest', 'pbkdf2:sha256:150000$6tjsUGUN$fff35601e39010f1ed7b8dc3b07bac32a8d5af57b2f14cce1d4d953445549a1f', 'user@test.com', 0),
  ('admintest', 'pbkdf2:sha256:150000$7MoD21iF$49d13a6e893e4f18cdfddd82e9240a1207de3df20de38284790c9e91a6bfbbf0', 'admin@test.com', 1),
  ('othertest', 'pbkdf2:sha256:150000$Bph3Imma$63ce0940b378c1bb717eb19dced40a4ef7850cf79963d5019e475cdfd04c3fe9', 'other@test.com', 0);

INSERT INTO location (name, maximum_capacity, author_id, latitude, longitude)
VALUES
  ('test location', 10, 1, 100.0, 50.0);