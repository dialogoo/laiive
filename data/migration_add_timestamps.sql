-- Migration: Replace time fields with timestamp fields
-- Run this in your database to update the schema

-- Add new timestamp columns
ALTER TABLE events
ADD COLUMN start_time TIMESTAMP,
ADD COLUMN end_time TIMESTAMP;

-- Update existing data (if you have any)
-- Convert existing date + time combinations to timestamps
UPDATE events
SET start_time = (event_date + event_init_hour)::TIMESTAMP,
    end_time = (event_date + event_end_hour)::TIMESTAMP
WHERE event_date IS NOT NULL
  AND event_init_hour IS NOT NULL
  AND event_end_hour IS NOT NULL;

-- Drop old columns
ALTER TABLE events
DROP COLUMN event_init_hour,
DROP COLUMN event_end_hour,
DROP COLUMN event_comments_hour;

-- Make the new columns NOT NULL if you want
-- ALTER TABLE events ALTER COLUMN start_time SET NOT NULL;
-- ALTER TABLE events ALTER COLUMN end_time SET NOT NULL;
