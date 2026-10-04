-- name: exists(id)$
-- return true if given user_id exists in database
SELECT EXISTS(SELECT id FROM users WHERE id = :id);

-- name: insert(id, login)!
-- Inserts new user in database
INSERT INTO users (
  id,
  login
) VALUES (
  :id,
  :login
)
ON CONFLICT (id) DO NOTHING;

-- name: subscribe(user_id, feed_id)!
-- Insert user_id, feed_id into subscriptions
INSERT INTO subscriptions (
  user_id,
  feed_id
) VALUES (
  :user_id,
  :feed_id
)
ON CONFLICT (user_id, feed_id) DO NOTHING;

-- name: unsubscribe(user_id, feed_id)!
-- Remove user_id, feed_id from subscriptions
DELETE FROM
  subscriptions
WHERE
  user_id = :user_id
  AND
  feed_id = :feed_id;

-- name: get_subscriptions(user_id)
-- Returns user's subscriptions
SELECT
  subscriptions.feed_id as feed_id
FROM
  users
  INNER JOIN
  subscriptions
  ON users.id = subscriptions.user_id
WHERE
  users.id = :user_id;

-- name: get_all_subscriptions()
-- Returns all subscriptions
SELECT
  users.id as user_id,
  subscriptions.feed_id as feed_id
FROM
  users
  INNER JOIN
  subscriptions
  ON users.id = subscriptions.user_id;
