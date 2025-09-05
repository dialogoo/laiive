# services/scraper/db_parser/parser.py
import psycopg2
from typing import List, Dict, Any
from config import settings


class DatabaseParser:
    def __init__(self, database_url: str = None):
        # Use environment variable or default connection string
        self.database_url = database_url

    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.database_url)

    def insert_events(
        self,
        events_data: List[Dict[str, Any]],
        source_website: str = "www.ecodibergamo.it",
    ):
        """Insert events into the database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        inserted_count = 0
        for event in events_data:
            try:
                cursor.execute(
                    """
                    INSERT INTO events (
                        event_name, event_name_2, event_description, event_genre,
                        event_tags, event_image, event_link, event_date,
                        event_init_hour, event_end_hour, event_comments_hour,
                        event_language, event_age_restriction, place_name,
                        place_name_2, place_description, place_address,
                        place_city, place_coordinates, place_link,
                        artist_name, artist_description, artist_summary,
                        artist_link, artist_genres, artist2_name,
                        artist2_description, artist2_summary, artist2_link,
                        artist2_genres, artist3_name, artist3_description,
                        artist3_summary, artist3_link, artist3_genres,
                        price_regular, price_discounted1, price_discounted1_comments,
                        price_discounted2, price_discounted2_comments, entrance_link,
                        source_website
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        event.get("event_name"),
                        event.get("event_name_2"),
                        event.get("event_description"),
                        event.get("event_genre"),
                        event.get("event_tags"),
                        event.get("event_image"),
                        event.get("event_link"),
                        event.get("event_date"),
                        event.get("event_init_hour"),
                        event.get("event_end_hour"),
                        event.get("event_comments_hour"),
                        event.get("event_language"),
                        event.get("event_age_restriction"),
                        event.get("place_name"),
                        event.get("place_name_2"),
                        event.get("place_description"),
                        event.get("place_address"),
                        event.get("place_city"),
                        event.get("place_coordinates"),
                        event.get("place_link"),
                        event.get("artist_name"),
                        event.get("artist_description"),
                        event.get("artist_summary"),
                        event.get("artist_link"),
                        event.get("artist_genres"),
                        event.get("artist2_name"),
                        event.get("artist2_description"),
                        event.get("artist2_summary"),
                        event.get("artist2_link"),
                        event.get("artist2_genres"),
                        event.get("artist3_name"),
                        event.get("artist3_description"),
                        event.get("artist3_summary"),
                        event.get("artist3_link"),
                        event.get("artist3_genres"),
                        event.get("price_regular"),
                        event.get("price_discounted1"),
                        event.get("price_discounted1_comments"),
                        event.get("price_discounted2"),
                        event.get("price_discounted2_comments"),
                        event.get("entrance_link"),
                        source_website,
                    ),
                )
                inserted_count += 1
            except Exception as e:
                print(
                    f"Error inserting event {event.get('event_name', 'Unknown')}: {e}"
                )

        conn.commit()
        conn.close()
        return inserted_count

    def get_events_count(self) -> int:
        """Get total number of events in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events")
        count = cursor.fetchone()[0]
        conn.close()
        return count


def main():
    database_url = settings.POSTGRES_URL
    parser = DatabaseParser(database_url)
    print(f"Databasen actualized. Total events: {parser.get_events_count()}")


if __name__ == "__main__":
    main()
