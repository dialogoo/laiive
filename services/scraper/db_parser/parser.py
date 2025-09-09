# services/scraper/db_parser/parser.py
import psycopg2
from typing import List, Dict, Any, Optional
from .config import settings
from difflib import SequenceMatcher
from loguru import logger
import re
import json
from datetime import datetime
import os


class DatabaseParser:
    def __init__(self, database_url: str = None):
        self.database_url = database_url
        # Simple similarity thresholds
        self.NAME_SIMILARITY_THRESHOLD = 0.80  # TODO individual thresholds

    # ============================================================================
    # PUBLIC METHODS
    # ============================================================================

    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.database_url)

    def insert_events(self, events_data, source_website="www.ecodibergamo.it"):
        """Insert events with duplicate checking"""
        # Set review file name based on source and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.review_file = (
            f"data/duplicates_to_review_{source_website}_{timestamp}.json"
        )

        conn = self.get_connection()
        cursor = conn.cursor()

        inserted_count = 0
        skipped_count = 0

        for event in events_data:
            try:
                # 1. Check for potential duplicate events
                if self._is_duplicate_event(cursor, event):
                    logger.warning(
                        f"Skipping potential duplicate event: {event.get('name')}"
                    )
                    skipped_count += 1
                    continue

                # 2. Handle venue with quality checks
                venue_id = self._handle_venue_simple(cursor, event)

                # 3. Handle artists with quality checks
                artist_ids = self._handle_artists_simple(cursor, event)

                # 4. Insert event with foreign keys
                cursor.execute(
                    """
                    INSERT INTO events (
                        name, description, genre, tags, image, link,
                        start_date, start_time, end_date, end_time,
                        language, age_restriction, age_recommended,
                        organizer, promoter, contact_name, contact_email, contact_phone,
                        ticket_link, price_regular, price_discounted, price_comments,
                        venue_id, artist1_id, artist2_id, artist3_id, artist4_id, artist5_id,
                        artist6_id, artist7_id, artist8_id, artist9_id, artist10_id,
                        extracted_text
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """,
                    (
                        event.get("name"),
                        event.get("description"),
                        event.get("genre"),
                        event.get("tags"),
                        event.get("image"),
                        event.get("link"),
                        event.get("start_date"),
                        event.get("start_time"),
                        event.get("end_date"),
                        event.get("end_time"),
                        event.get("language"),
                        event.get("age_restriction"),
                        event.get("age_recommended"),
                        event.get("organizer"),
                        event.get("promoter"),
                        event.get("contact_name"),
                        event.get("contact_email"),
                        event.get("contact_phone"),
                        event.get("ticket_link"),
                        event.get("price_regular"),
                        event.get("price_discounted"),
                        event.get("price_comments"),
                        venue_id,
                        artist_ids[0],
                        artist_ids[1],
                        artist_ids[2],
                        artist_ids[3],
                        artist_ids[4],
                        artist_ids[5],
                        artist_ids[6],
                        artist_ids[7],
                        artist_ids[8],
                        artist_ids[9],
                        event.get("extracted_text"),
                    ),
                )

                inserted_count += 1
                logger.info(f"Successfully inserted event: {event.get('name')}")

            except Exception as e:
                logger.error(
                    f"Error inserting event {event.get('name', 'Unknown')}: {e}"
                )

        conn.commit()
        conn.close()

        logger.info(
            f"Insertion complete: {inserted_count} inserted, {skipped_count} skipped"
        )
        return inserted_count

    def get_events_count(self) -> int:
        """Get total number of events in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_review_summary(
        self,
    ) -> Dict[
        str, Any
    ]:  # TODO add all the data for review and check reviews for artists and venues
        """Get summary of items pending review"""
        try:
            with open(self.review_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            pending_reviews = []
            for line in lines:
                if line.strip():
                    try:
                        entry = json.loads(line.strip())
                        if entry.get("decision") is None:  # Not yet reviewed
                            pending_reviews.append(entry)
                    except json.JSONDecodeError:
                        continue

            # Group by table
            by_table = {}
            for review in pending_reviews:
                table = review["table"]
                if table not in by_table:
                    by_table[table] = []
                by_table[table].append(review)

            return {
                "total_pending": len(pending_reviews),
                "by_table": {
                    table: len(reviews) for table, reviews in by_table.items()
                },
                "pending_reviews": pending_reviews,
            }
        except FileNotFoundError:
            return {"total_pending": 0, "by_table": {}, "pending_reviews": []}

    def clear_review_file(self):
        """Clear the review file"""
        if os.path.exists(self.review_file):
            os.remove(self.review_file)
            logger.info("Cleared review file")

    # ============================================================================
    # PRIVATE HELPER METHODS - TEXT PROCESSING
    # ============================================================================

    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        if not text:
            return ""
        normalized = re.sub(r"[^\w\s]", "", text.lower().strip())
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(
            None, self._normalize_text(text1), self._normalize_text(text2)
        ).ratio()

    def _log_for_review(
        self,
        table: str,
        new_item: dict,
        existing_item: dict,
        similarity: float,
        event_data: dict = None,
    ):
        review_entry = {
            "timestamp": datetime.now().isoformat(),
            "table": table,
            "similarity": round(similarity, 3),
            "action": "REVIEW_REQUIRED",
            "new_item": new_item,
            "existing_item": existing_item,
            "decision": None,
        }

        try:
            with open(self.review_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(review_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"Error writing to review file: {e}")

        logger.warning(
            f"REVIEW NEEDED - {table}: '{new_item.get('name')}' vs '{existing_item.get('name')}' "
            f"(similarity: {similarity:.3f})"
        )

    # ============================================================================
    # PRIVATE HELPER METHODS - DUPLICATE DETECTION
    # ============================================================================

    def _is_duplicate_event(self, cursor, event) -> bool:
        """Check if event is a duplicate - exact match first, then similarity"""
        event_name = event.get("name")
        if not event_name:
            return False

        # 1. Try exact match first (most efficient)
        cursor.execute("SELECT id, name FROM events WHERE name = %s", (event_name,))
        exact_match = cursor.fetchone()
        if exact_match:
            logger.info(
                f"Event already exists (exact match): '{event_name}' - skipping entry"
            )
            return True

        # 2. Try case-insensitive match
        cursor.execute(
            "SELECT id, name FROM events WHERE LOWER(name) = LOWER(%s)", (event_name,)
        )
        case_insensitive_match = cursor.fetchone()
        if case_insensitive_match:
            logger.info(
                f"Event already exists (case-insensitive): '{event_name}' vs '{case_insensitive_match[1]}' - skipping entry"
            )
            return True

        # 3. Check for similar events (only if no exact match found)
        cursor.execute("SELECT id, name FROM events")
        existing_events = cursor.fetchall()

        for existing_id, existing_name in existing_events:
            similarity = self._calculate_similarity(event_name, existing_name)

            if similarity >= 1.0:  # Perfect match
                logger.info(
                    f"Event already exists (perfect similarity): '{event_name}' - skipping entry"
                )
                return True
            elif similarity > self.NAME_SIMILARITY_THRESHOLD:  # Potential duplicate
                logger.warning(
                    f"REVIEW NEEDED - events: '{event_name}' vs '{existing_name}' (similarity: {similarity:.3f})"
                )
                self._log_for_review(
                    "events",
                    {"name": event_name, "id": "NEW"},
                    {"name": existing_name, "id": existing_id},
                    similarity,
                    event,
                )
                return True

        return False  # No duplicate found

    # ============================================================================
    # PRIVATE HELPER METHODS - VENUE HANDLING
    # ============================================================================

    def _handle_venue_simple(self, cursor, event) -> Optional[int]:
        """Handle venue with simple name matching - only creates venues when data exists"""
        venue_name = event.get("venue_name")
        if not venue_name or not venue_name.strip():
            return None

        # 1. Try exact match first (most efficient)
        cursor.execute("SELECT id, name FROM venues WHERE name = %s", (venue_name,))
        exact_match = cursor.fetchone()
        if exact_match:
            logger.debug(
                f"Exact venue match found: '{venue_name}' (ID: {exact_match[0]})"
            )
            return exact_match[0]

        # 2. Try case-insensitive match
        cursor.execute(
            "SELECT id, name FROM venues WHERE LOWER(name) = LOWER(%s)", (venue_name,)
        )
        case_insensitive_match = cursor.fetchone()
        if case_insensitive_match:
            logger.info(
                f"Case-insensitive venue match: '{venue_name}' vs '{case_insensitive_match[1]}' (ID: {case_insensitive_match[0]})"
            )
            return case_insensitive_match[0]

        # 3. Try trimmed match (remove extra spaces)
        trimmed_name = venue_name.strip()
        if trimmed_name != venue_name:
            cursor.execute(
                "SELECT id, name FROM venues WHERE name = %s", (trimmed_name,)
            )
            trimmed_match = cursor.fetchone()
            if trimmed_match:
                logger.info(
                    f"Trimmed venue match: '{venue_name}' vs '{trimmed_match[1]}' (ID: {trimmed_match[0]})"
                )
                return trimmed_match[0]

        # 4. Only if no exact matches, check for similar venues (expensive operation)
        if self._should_check_similarity():
            return self._check_similar_venues(cursor, venue_name)

        # 5. No match found, create new venue
        return self._insert_new_venue(cursor, event)

    def _should_check_similarity(self) -> bool:
        """Decide if we should check for similar venues (can be based on venue count)"""
        # For now, always check, but you could add logic like:
        # - Only check if venue count < 1000
        # - Only check for certain venue types
        # - Add a configuration flag
        return True

    def _check_similar_venues(self, cursor, venue_name):
        """Check for similar venues using similarity calculation"""
        cursor.execute("SELECT id, name FROM venues")
        all_venues = cursor.fetchall()

        for venue_id, existing_name in all_venues:
            similarity = self._calculate_similarity(venue_name, existing_name)
            if similarity > self.NAME_SIMILARITY_THRESHOLD:
                self._log_for_review(
                    "venues",
                    {"name": venue_name, "id": "NEW"},
                    {"name": existing_name, "id": venue_id},
                    similarity,
                )
                logger.warning(
                    f"Similar venue found: '{venue_name}' vs '{existing_name}' (similarity: {similarity:.3f}) - logged for review"
                )
                return venue_id

    def _insert_new_venue(self, cursor, event) -> int:
        """Insert a new venue"""
        cursor.execute(
            """
            INSERT INTO venues (name, description, address, city, country, capacity,
                              latitude, longitude, link, image, contact_name, contact_email,
                              contact_phone, founded_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                event.get("venue_name"),
                event.get("venue_description"),
                event.get("venue_address"),
                event.get("venue_city"),
                event.get("venue_country"),
                event.get("venue_capacity"),
                event.get("venue_latitude"),
                event.get("venue_longitude"),
                event.get("venue_link"),
                event.get("venue_image"),
                event.get("venue_contact_name"),
                event.get("venue_contact_email"),
                event.get("venue_contact_phone"),
                event.get("venue_founded_year"),
            ),
        )
        venue_id = cursor.fetchone()[0]
        logger.info(f"Inserted new venue: {event.get('venue_name')} (ID: {venue_id})")
        return venue_id

    # ============================================================================
    # PRIVATE HELPER METHODS - ARTIST HANDLING
    # ============================================================================

    def _handle_artists_simple(self, cursor, event) -> List[Optional[int]]:
        """Handle artists with simple name matching - only creates artists when data exists"""
        artist_ids = [None] * 10  # Initialize with None values

        for i in range(1, 11):
            artist_name = event.get(f"artist{i}_name")
            if (
                artist_name and artist_name.strip()
            ):  # Only process if artist name exists and is not empty
                artist_id = self._handle_single_artist_simple(cursor, event, i)
                artist_ids[i - 1] = (
                    artist_id  # Place in correct position (0-based index)
                )
            # If no artist name, leave as None (no default artist creation)

        return artist_ids

    def _handle_single_artist_simple(self, cursor, event, artist_num: int) -> int:
        """Handle a single artist with simple name matching - only called when artist data exists"""
        artist_name = event.get(f"artist{artist_num}_name")

        # First, try exact match
        cursor.execute("SELECT id, name FROM artists WHERE name = %s", (artist_name,))
        exact_match = cursor.fetchone()

        if exact_match:
            return exact_match[0]  # Return existing artist_id

        # Check for similar artists
        cursor.execute("SELECT id, name FROM artists")
        all_artists = cursor.fetchall()

        for artist_id, existing_name in all_artists:
            similarity = self._calculate_similarity(artist_name, existing_name)

            if similarity > self.NAME_SIMILARITY_THRESHOLD:
                # Log for human review
                self._log_for_review(
                    "artists",
                    {"name": artist_name, "id": "NEW"},
                    {"name": existing_name, "id": artist_id},
                    similarity,
                )
                return artist_id  # Use existing artist

        # No similar artist found, create new one
        return self._insert_new_artist(cursor, event, artist_num)

    def _insert_new_artist(self, cursor, event, artist_num: int) -> int:
        """Insert a new artist - always returns an artist ID"""
        cursor.execute(
            """
            INSERT INTO artists (name, description, summary, components, country, city,
                               genres, link, image, contact_name, contact_email,
                               contact_phone, founded_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                event.get(f"artist{artist_num}_name"),
                event.get(f"artist{artist_num}_description"),
                event.get(f"artist{artist_num}_summary"),
                event.get(f"artist{artist_num}_components"),
                event.get(f"artist{artist_num}_country"),
                event.get(f"artist{artist_num}_city"),
                event.get(f"artist{artist_num}_genres"),
                event.get(f"artist{artist_num}_link"),
                event.get(f"artist{artist_num}_image"),
                event.get(f"artist{artist_num}_contact_name"),
                event.get(f"artist{artist_num}_contact_email"),
                event.get(f"artist{artist_num}_contact_phone"),
                event.get(f"artist{artist_num}_founded_year"),
            ),
        )
        artist_id = cursor.fetchone()[0]
        logger.info(
            f"Inserted new artist: {event.get(f'artist{artist_num}_name')} (ID: {artist_id})"
        )
        return artist_id


def main():
    database_url = settings.POSTGRES_URL
    parser = DatabaseParser(database_url)

    # Show review summary
    review_summary = parser.get_review_summary()
    print("=== REVIEW SUMMARY ===")
    print(f"Total pending reviews: {review_summary['total_pending']}")
    for table, count in review_summary["by_table"].items():
        print(f"{table}: {count} pending")

    print(f"\nTotal events: {parser.get_events_count()}")

    conn = parser.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM events WHERE venue_id IS NULL")
    null_venue_count = cursor.fetchone()[0]
    logger.info(f"Events with NULL venue_id: {null_venue_count}")


if __name__ == "__main__":
    main()
