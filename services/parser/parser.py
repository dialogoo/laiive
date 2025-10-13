from pydantic import BaseModel, EmailStr, field_validator
import psycopg2
from typing import List, Dict, Any, Optional
from .config import settings
from rapidfuzz import fuzz
from loguru import logger
import re
import json
from datetime import datetime
import os


class DatabaseParser:
    def __init__(self, database_url: str = None):
        self.database_url = database_url
        self.NAME_SIMILARITY_THRESHOLD = 0.80
        self.PERFECT_SIMILARITY_THRESHOLD = 1.0

    def get_connection(self):
        return psycopg2.connect(self.database_url)

    def insert_events(self, events_data, source_website="www.ecodibergamo.it"):
        # TODO improve the insertion logic, check artist and date filtering by place. add pydantic for type verification

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
                if self._is_duplicate_event(cursor, event):
                    logger.warning(
                        f"Skipping potential duplicate event: {event.get('name')}"
                    )
                    skipped_count += 1
                    continue

                venue_id = self._handle_venue_simple(cursor, event)
                artist_ids = self._handle_artists_simple(cursor, event)

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
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events")
        count = cursor.fetchone()[0]
        conn.close()
        return count

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

    def get_review_summary(
        self,
    ) -> Dict[
        str, Any
    ]:  # TODO add all the data for review and check reviews for artists and venues
        try:
            with open(self.review_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            pending_reviews = []
            for line in lines:
                if line.strip():
                    try:
                        entry = json.loads(line.strip())
                        if entry.get("decision") is None:  # TODO Not yet reviewed
                            pending_reviews.append(entry)
                    except json.JSONDecodeError:
                        continue

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

    def remove_review_file(self):
        if os.path.exists(self.review_file):
            os.remove(self.review_file)
            logger.info("Cleared review file")

    def _normalize_text(self, text: str) -> str:
        if not text:
            return ""
        normalized = re.sub(r"[^\w\s]", "", text.lower().strip())
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        if not text1 or not text2:
            return 0.0
        return fuzz.ratio(
            None, self._normalize_text(text1), self._normalize_text(text2)
        )

    def _find_duplicate_entity(
        self, cursor, table_name: str, name: str, entity_type: str = "entity"
    ) -> Optional[tuple]:
        if not name or not name.strip():
            return None

        # Level 1: Exact match (case-sensitive)
        cursor.execute(f"SELECT id, name FROM {table_name} WHERE name = %s", (name,))
        exact_match = cursor.fetchone()
        if exact_match:
            logger.info(
                f"{entity_type.title()} exact match found: '{name}' (ID: {exact_match[0]})"
            )
            return (exact_match[0], "exact", exact_match[1])

        self._find_similar_entity(cursor, table_name, name, entity_type)

    def _find_similar_entity(
        self, cursor, table_name: str, name: str, entity_type: str
    ) -> Optional[tuple]:
        cursor.execute(f"SELECT id, name FROM {table_name}")
        all_entities = cursor.fetchall()

        for entity_id, existing_name in all_entities:
            similarity = self._calculate_similarity(name, existing_name)

            if similarity >= self.PERFECT_SIMILARITY_THRESHOLD:  # Perfect match
                logger.info(
                    f"{entity_type.title()} perfect similarity match: '{name}' vs '{existing_name}' (similarity: {similarity:.3f})"
                )
                return (entity_id, "perfect_similarity", existing_name)
            elif similarity > self.NAME_SIMILARITY_THRESHOLD:  # Potential duplicate
                logger.warning(
                    f"REVIEW NEEDED - for manual entry- {entity_type}: '{name}' vs '{existing_name}' (similarity: {similarity:.3f})"
                )  # TODO this step could be done by an Agent. or at least semi automated.
                self._log_for_review(
                    entity_type,
                    {"name": name, "id": "NEW"},
                    {"name": existing_name, "id": entity_id},
                    similarity,
                )
                return (entity_id, "similarity", existing_name)

        return None

    def _is_duplicate_event(self, cursor, event) -> bool:
        event_name = event.get("name")
        if not event_name:
            return False

        duplicate_result = self._find_duplicate_entity(
            cursor, "events", event_name, "event"
        )
        if duplicate_result:
            entity_id, match_type, existing_name = duplicate_result
            logger.info(
                f"Event duplicate found ({match_type}): '{event_name}' - skipping entry"
            )
            return True

        return False

    def _handle_venue_simple(self, cursor, event) -> Optional[int]:
        """Handle venue with standardized 4-level duplicate detection"""
        venue_name = event.get("venue_name")
        if not venue_name or not venue_name.strip():
            return None

        duplicate_result = self._find_duplicate_entity(
            cursor, "venues", venue_name, "venue"
        )
        if duplicate_result:
            entity_id, match_type, existing_name = duplicate_result
            logger.info(
                f"venue duplicate found ({match_type}): '{venue_name}' - skipping entry"
            )
            return entity_id

        # No duplicate found, create new venue
        return self._insert_new_venue(cursor, event)

    def _handle_single_artist_simple(self, cursor, event, artist_num: int) -> int:
        """Handle a single artist with standardized 4-level duplicate detection"""
        artist_name = event.get(f"artist{artist_num}_name")

        duplicate_result = self._find_duplicate_entity(
            cursor, "artists", artist_name, "artist"
        )
        if duplicate_result:
            entity_id, match_type, existing_name = duplicate_result
            logger.info(
                f"artist duplicate found ({match_type}): '{artist_name}' - skipping entry"
            )
            return entity_id

        # No duplicate found, create new artist
        return self._insert_new_artist(cursor, event, artist_num)

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

    review_summary = parser.get_review_summary()
    logger.info("=== REVIEW SUMMARY ===")
    logger.info(f"Total pending reviews: {review_summary['total_pending']}")
    for table, count in review_summary["by_table"].items():
        print(f"{table}: {count} pending")

    logger.info(f"\nTotal events: {parser.get_events_count()}")

    conn = parser.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM events WHERE venue_id IS NULL")
    null_venue_count = cursor.fetchone()[0]
    logger.info(f"Events with NULL venue_id: {null_venue_count}")


if __name__ == "__main__":
    main()
