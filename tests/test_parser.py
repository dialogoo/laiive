#!/usr/bin/env python3
import json
import sys
import os

# Add the workspace root to Python path
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, workspace_root)

# Now import from services
from services.scraper.db_parser.parser import DatabaseParser
from services.scraper.db_parser.config import settings
from loguru import logger


def test_parser_simple():
    """Simple test: parse JSON data and show results"""

    # Load the JSON data
    with open(
        "services/scraper/event_scraper/out/events_20250905.json", "r", encoding="utf-8"
    ) as f:
        data = json.load(f)

    events = data["events"]
    logger.info(f"Loaded {len(events)} events from JSON")

    # Initialize parser
    try:
        parser = DatabaseParser(settings.POSTGRES_URL)
        logger.success("Parser initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing parser: {e}")
        return

    # Test database connection
    try:
        conn = parser.get_connection()
        logger.success("Database connection successful")
        conn.close()
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return

    # Test insertion
    logger.info("Starting event insertion...")
    try:
        # DON'T clear data first - let's see if duplicates are detected
        logger.info("Testing duplicate detection with existing data...")
        inserted_count = parser.insert_events(
            events, source_website="www.ecodibergamo.it"
        )
        logger.success(f"Successfully inserted {inserted_count} events")

        # Verify results
        conn = parser.get_connection()
        cursor = conn.cursor()

        # Check counts
        cursor.execute("SELECT COUNT(*) FROM events")
        events_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM venues")
        venues_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM artists")
        artists_count = cursor.fetchone()[0]

        logger.info(f" FINAL COUNTS:")
        logger.info(f"   Events: {events_count}")
        logger.info(f"   Venues: {venues_count}")
        logger.info(f"   Artists: {artists_count}")

        # Show sample events
        cursor.execute(
            """
            SELECT id, name, start_date, start_time, extracted_text
            FROM events
            ORDER BY id
            LIMIT 5
        """
        )
        sample_events = cursor.fetchall()
        logger.info(" SAMPLE EVENTS:")
        for event in sample_events:
            logger.info(
                f"   ID: {event[0]}, Name: {event[1]}, Date: {event[2]}, Time: {event[3]}"
            )
            logger.info(f"   Text: {event[4][:100]}...")

        # Show sample venues
        cursor.execute("SELECT id, name, city, country FROM venues ORDER BY id LIMIT 5")
        sample_venues = cursor.fetchall()
        logger.info(" SAMPLE VENUES:")
        for venue in sample_venues:
            logger.info(
                f"   ID: {venue[0]}, Name: {venue[1]}, City: {venue[2]}, Country: {venue[3]}"
            )

        # Show sample artists (if any)
        if artists_count > 0:
            cursor.execute(
                "SELECT id, name, country, city FROM artists ORDER BY id LIMIT 5"
            )
            sample_artists = cursor.fetchall()
            logger.info(" SAMPLE ARTISTS:")
            for artist in sample_artists:
                logger.info(
                    f"   ID: {artist[0]}, Name: {artist[1]}, Country: {artist[2]}, City: {artist[3]}"
                )
        else:
            logger.info(" ARTISTS: None (as expected - no artist data in JSON)")

        conn.close()

        # Get review summary
        review_summary = parser.get_review_summary()
        logger.warning(f" Pending reviews: {review_summary['total_pending']}")

        logger.success(" Test completed successfully!")

    except Exception as e:
        logger.error(f"Error during insertion: {e}")
        logger.exception("Full traceback:")


if __name__ == "__main__":
    test_parser_simple()
