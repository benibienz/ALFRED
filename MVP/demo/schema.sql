-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS history;

CREATE TABLE history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  state TEXT NOT NULL,
  action INTEGER NOT NULL
);