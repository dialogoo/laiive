import json
import re
from datetime import datetime, date, time
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class EventParser:
    """Parse scraped JSONL events into database schema format"""

    def __init__(self, jsonl_file_path: str):
        self.jsonl_file_path = Path(jsonl_file_path)
        self.parsed_events = []

    def parse_all_events(self) -> List[Dict]:
        """Parse all events from JSONL file"""
        if not self.jsonl_file_path.exists():
            raise FileNotFoundError(f"File not found: {self.jsonl_file_path}")

        print(f"Parsing events from: {self.jsonl_file_path}")

        with open(self.jsonl_file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    event_data = json.loads(line)
                    parsed_event = self.parse_single_event(event_data)
                    if parsed_event:
                        self.parsed_events.append(parsed_event)

                except json.JSONDecodeError as e:
                    print(f"Error parsing line {line_num}: {e}")
                    continue

        print(f"Successfully parsed {len(self.parsed_events)} events")
        return self.parsed_events

    def parse_single_event(self, event_data: Dict) -> Optional[Dict]:
        """Parse a single event into database schema format"""
        try:
            # Skip navigation/non-event entries
            if not self._is_valid_event(event_data):
                return None

            # Extract basic event info
            event_name = self._extract_event_name(event_data)
            if not event_name:
                return None

            # Parse date and time
            event_date, event_init_hour, event_end_hour = self._parse_date_time(
                event_data
            )

            # Extract location info
            place_name, place_city = self._extract_location(event_data)

            # Extract event details
            event_description = self._extract_description(event_data)
            event_genre = self._extract_genre(event_data)
            event_link = self._extract_event_link(event_data)

            # Build database record
            db_event = {
                # Event basic info
                "event_name": event_name,
                "event_name_2": None,  # Secondary name if available
                "event_description": event_description,
                "event_genre": event_genre,
                "event_tags": self._extract_tags(event_data),
                "event_image": None,  # No images in current data
                "event_link": event_link,
                # Date and time
                "event_date": event_date,
                "event_init_hour": event_init_hour,
                "event_end_hour": event_end_hour,
                "event_comments_hour": self._extract_time_comments(event_data),
                # Location info
                "place_name": place_name,
                "place_name_2": None,
                "place_description": None,
                "place_address": None,
                "place_city": place_city,
                "place_coordinates": None,
                "place_link": None,
                # Artist info (not available in current data)
                "artist_id": None,
                "artist_name": None,
                "artist_description": None,
                "artist_summary": None,
                "artist_link": None,
                "artist_genres": None,
                # Additional artists (not available)
                "artist2_id": None,
                "artist2_name": None,
                "artist2_description": None,
                "artist2_summary": None,
                "artist2_link": None,
                "artist2_genres": None,
                "artist3_id": None,
                "artist3_name": None,
                "artist3_description": None,
                "artist3_summary": None,
                "artist3_link": None,
                "artist3_genres": None,
                # Pricing (not available in current data)
                "price_regular": None,
                "price_discounted1": None,
                "price_discounted1_comments": None,
                "price_discounted2": None,
                "price_discounted2_comments": None,
                "entrance_link": None,
                # Additional fields
                "event_language": "Italian",  # Default for Italian site
                "event_age_restriction": None,
            }

            return db_event

        except Exception as e:
            print(f"Error parsing event: {e}")
            return None

    def _is_valid_event(self, event_data: Dict) -> bool:
        """Check if this is a valid event entry"""
        # Skip navigation entries
        if "Oggi" in event_data.get("text_content", []) or "Domani" in event_data.get(
            "text_content", []
        ):
            return False

        # Skip entries without meaningful content
        if not event_data.get("title") and not event_data.get("text_content"):
            return False

        return True

    def _extract_event_name(self, event_data: Dict) -> Optional[str]:
        """Extract event name from title or text content"""
        # Try to get from title first
        title = event_data.get("title")
        if title:
            # Clean HTML tags
            clean_title = re.sub(r"<[^>]+>", "", title)
            clean_title = re.sub(r"&[^;]+;", "", clean_title)
            clean_title = clean_title.strip()
            if clean_title and len(clean_title) > 3:
                return clean_title

        # Fallback to text content
        text_content = event_data.get("text_content", [])
        if text_content:
            # Look for meaningful text (not just dates/numbers)
            for text in text_content:
                if (
                    text
                    and len(text) > 3
                    and not text.isdigit()
                    and not text
                    in [
                        "Oggi",
                        "Domani",
                        "Agosto",
                        "Settembre",
                        "Ottobre",
                        "Novembre",
                        "Dicembre",
                    ]
                ):
                    return text.strip()

        return None

    def _parse_date_time(
        self, event_data: Dict
    ) -> Tuple[Optional[date], Optional[time], Optional[time]]:
        """Parse date and time information"""
        try:
            # Extract date from the date field
            date_str = event_data.get("date", "")
            if not date_str or date_str == "unknown_date":
                return None, None, None

            # Parse date (format: "2025/08/13")
            if "/" in date_str:
                year, month, day = map(int, date_str.split("/"))
                event_date = date(year, month, day)
            else:
                event_date = None

            # Extract time from text content
            text_content = event_data.get("text_content", [])
            event_init_hour = None
            event_end_hour = None

            for text in text_content:
                if "h." in text:
                    time_match = re.search(
                        r"h\.(\d{1,2}):(\d{2})\s*/\s*(\d{1,2}):(\d{2})", text
                    )
                    if time_match:
                        start_hour, start_min = int(time_match.group(1)), int(
                            time_match.group(2)
                        )
                        end_hour, end_min = int(time_match.group(3)), int(
                            time_match.group(4)
                        )
                        event_init_hour = time(start_hour, start_min)
                        event_end_hour = time(end_hour, end_min)
                        break

                    # Single time
                    time_match = re.search(r"h\.(\d{1,2}):(\d{2})", text)
                    if time_match:
                        hour, minute = int(time_match.group(1)), int(
                            time_match.group(2)
                        )
                        event_init_hour = time(hour, minute)
                        break

            return event_date, event_init_hour, event_end_hour

        except Exception as e:
            print(f"Error parsing date/time: {e}")
            return None, None, None

    def _extract_location(
        self, event_data: Dict
    ) -> Tuple[Optional[str], Optional[str]]:
        """Extract place name and city from text content"""
        text_content = event_data.get("text_content", [])
        place_name = None
        place_city = None

        for text in text_content:
            text = text.strip()
            if text and len(text) > 3:
                # Skip dates, times, and short text
                if (
                    not text.isdigit()
                    and not text
                    in [
                        "Oggi",
                        "Domani",
                        "Agosto",
                        "Settembre",
                        "Ottobre",
                        "Novembre",
                        "Dicembre",
                    ]
                    and not "h." in text
                ):
                    if not place_name:
                        place_name = text
                    elif not place_city and text != place_name:
                        place_city = text
                        break

        return place_name, place_city

    def _extract_description(self, event_data: Dict) -> Optional[str]:
        """Extract event description"""
        # For now, use the event name as description
        # In the future, you could scrape detail pages for full descriptions
        return event_data.get("title")

    def _extract_genre(self, event_data: Dict) -> Optional[str]:
        """Extract event genre/category from URL or text"""
        # Try to extract from URL path
        links = event_data.get("links", [])
        for link in links:
            if "/dettaglio/" in link:
                # URL format: /eventi/eppen/dettaglio/category/city/event-name/
                parts = link.split("/")
                if len(parts) > 4:
                    category = parts[4]  # e.g., "arte", "musica", "cinema"
                    return category.title()

        return None

    def _extract_tags(self, event_data: Dict) -> List[str]:
        """Extract event tags"""
        tags = []

        # Add genre as tag
        genre = self._extract_genre(event_data)
        if genre:
            tags.append(genre)

        # Add city as tag
        place_city = event_data.get("place_city")
        if place_city:
            tags.append(place_city)

        return tags

    def _extract_event_link(self, event_data: Dict) -> Optional[str]:
        """Extract the main event link"""
        links = event_data.get("links", [])
        for link in links:
            if "/dettaglio/" in link:
                return f"https://www.ecodibergamo.it{link}"
        return None

    def _extract_time_comments(self, event_data: Dict) -> Optional[str]:
        """Extract additional time-related comments"""
        text_content = event_data.get("text_content", [])
        time_comments = []

        for text in text_content:
            if "Fino a" in text or "h." in text:
                time_comments.append(text.strip())

        return " | ".join(time_comments) if time_comments else None

    def save_to_json(self, output_file: str):
        """Save parsed events to JSON file"""
        output_path = Path(output_file)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.parsed_events, f, indent=2, ensure_ascii=False, default=str)

        print(f"Saved {len(self.parsed_events)} parsed events to: {output_path}")

    def generate_sql_inserts(self, output_file: str):
        """Generate SQL INSERT statements"""
        output_path = Path(output_file)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("-- Generated SQL INSERT statements for events table\n")
            f.write("-- Generated on: " + datetime.now().isoformat() + "\n\n")

            for event in self.parsed_events:
                # Build column list
                columns = list(event.keys())
                values = []

                for col in columns:
                    value = event[col]
                    if value is None:
                        values.append("NULL")
                    elif isinstance(value, (date, time)):
                        values.append(f"'{value}'")
                    elif isinstance(value, list):
                        # Handle arrays like event_tags
                        if value:
                            array_values = [f"'{v}'" for v in value]
                            values.append(f"ARRAY[{', '.join(array_values)}]")
                        else:
                            values.append("ARRAY[]")
                    elif isinstance(value, str):
                        # Escape single quotes
                        escaped_value = value.replace("'", "''")
                        values.append(f"'{escaped_value}'")
                    else:
                        values.append(str(value))

                sql = f"INSERT INTO events ({', '.join(columns)}) VALUES ({', '.join(values)});\n"
                f.write(sql)

        print(f"Generated SQL INSERT statements: {output_path}")


def main():
    """Main function to parse events"""
    # Parse the latest JSONL file
    jsonl_file = "out/eppen_20250813.jsonl"

    parser = EventParser(jsonl_file)
    events = parser.parse_all_events()

    if events:
        # Save parsed events to JSON
        parser.save_to_json("parsed_events.json")

        # Generate SQL INSERT statements
        parser.generate_sql_inserts("events_insert.sql")

        # Print summary
        print(f"\n=== PARSING SUMMARY ===")
        print(f"Total events parsed: {len(events)}")
        print(f"Events with dates: {sum(1 for e in events if e['event_date'])}")
        print(f"Events with times: {sum(1 for e in events if e['event_init_hour'])}")
        print(f"Events with locations: {sum(1 for e in events if e['place_name'])}")
        print(f"Events with genres: {sum(1 for e in events if e['event_genre'])}")

        # Show sample event
        if events:
            print(f"\n=== SAMPLE EVENT ===")
            sample = events[0]
            for key, value in sample.items():
                if value is not None:
                    print(f"{key}: {value}")
    else:
        print("No events were parsed successfully")


if __name__ == "__main__":
    main()
