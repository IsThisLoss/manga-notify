-- name: get_add
-- Fetch all feeds from database
SELECT
  id,
  driver,
  url,
  cursor,
  title,
  mal_url
FROM
  feeds;

-- name: get^
-- Fetch feed by id
SELECT
  id,
  driver,
  url,
  cursor,
  title,
  mal_url
FROM
  feeds
WHERE
  id = :id
LIMIT 1;

-- name: find^
-- Find feed by driver and url
SELECT
  id,
  driver,
  url,
  cursor,
  title,
  mal_url
FROM
  feeds
WHERE
  driver = :driver
  AND
  url = :url
LIMIT 1;

-- name: insert<!
-- Inserts new feed
INSERT INTO feeds(
  driver,
  url
) VALUES (
  :driver,
  :url
)
RETURNING id

-- name: find_without_mal_link
-- Finds feeds with mal_url IS NULL
SELECT
  id,
  driver,
  url,
  cursor,
  title,
  mal_url
FROM
  feeds
WHERE
  title IS NOT NULL
  AND
  mal_url IS NULL
LIMIT :limit;

-- name: update!
-- Updates cursor and title
UPDATE
  feeds
SET
  cursor = :cursor,
  title = :title
WHERE
  id = :id;

-- name: update_mal_url!
-- Updates mal_url
UPDATE
  feeds
SET
  mal_url = :mal_url
WHERE
  id = :id;
