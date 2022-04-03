CREATE TABLE user_pipeline (
  user_id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  state TEXT NOT NULL,
  payload TEXT
);
