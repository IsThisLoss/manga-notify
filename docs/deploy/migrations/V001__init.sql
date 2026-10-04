CREATE TABLE feeds (
  id SERIAL PRIMARY KEY,
  driver TEXT NOT NULL,
  url TEXT NOT NULL,
  cursor TEXT NOT NULL DEFAULT ''
);

CREATE TABLE users (
  id TEXT PRIMARY KEY,
  login TEXT NOT NULL
);

CREATE TABLE subscriptions (
  user_id TEXT REFERENCES users(id),
  feed_id INTEGER REFERENCES feeds(id),
  UNIQUE(user_id, feed_id)
);
