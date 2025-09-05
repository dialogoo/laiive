import scrapy
from pathlib import Path
from datetime import datetime
import json


class EppenMusicSpider(scrapy.Spider):
    def __init__(self):
        self.event_data = []

    name = "eppen_music"
    custom_settings = {
        "LOG_LEVEL": "DEBUG",
    }

    def start_requests(self):

        urls = [
            "https://www.ecodibergamo.it/eventi/eppen/ricerca/?q=&page=1&start_date=&end_date=&category=musica&city=",
            "https://www.ecodibergamo.it/eventi/eppen/ricerca/?q=&page=2&start_date=&end_date=&category=musica&city=",
            "https://www.ecodibergamo.it/eventi/eppen/ricerca/?q=&page=3&start_date=&end_date=&category=musica&city=",
            "https://www.ecodibergamo.it/eventi/eppen/ricerca/?q=&page=4&start_date=&end_date=&category=musica&city=",
            "https://www.ecodibergamo.it/eventi/eppen/ricerca/?q=&page=5&start_date=&end_date=&category=musica&city=",
        ]

        for page_num, url in enumerate(urls, 1):
            yield scrapy.Request(
                url=url, callback=self.parse, meta={"page_num": page_num}
            )

    def parse(self, response):
        """Parse response and save HTML content to file."""
        page_num = response.meta["page_num"]
        # Sanitize the domain name for filename
        domain = response.url.split("/")[2].replace(".", "_")
        page = f"{domain}_page{page_num}"
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"eppenEvents-{page}-{date_str}.html"

        # Get output directory from settings
        out_dir = Path(self.settings.get("OUTPUT_DIR", "out"))
        out_file = out_dir / filename

        out_file.write_bytes(response.body)
        self.log(f"Saved file {out_file}")

        # get all the event links
        event_links = response.css("h5.card-title a::attr(href)").getall()

        for link in event_links[:5]:  # TODO apply to all links, delete index [:5]
            if link.startswith("http"):
                absolute_url = link  # Already absolute
            else:
                absolute_url = "https://www.ecodibergamo.it" + link

            yield scrapy.Request(
                url=absolute_url,
                callback=self.parse_event_details,
            )

    def parse_event_details(self, response):
        """parse each event details"""
        import json

        # Extract JSON-LD data
        json_ld = response.xpath('//script[@type="application/ld+json"]/text()').get()
        event_json = None

        if json_ld:
            try:
                event_json = json.loads(json_ld)
            except json.JSONDecodeError:
                pass

        event_data = {
            # Event basic info
            "event_name": (
                response.css(".col-12.col-lg-10 h1::text").get() or ""
            ).strip(),
            "event_name_2": None,
            "event_description": response.css(".col-12.col-lg-10 h2::text").get(),
            "event_genre": (
                response.css(".col-12.col-lg-10 .article-section-category::text")
                .getall()[-1]
                .strip()
                .split("/")[-1]
                .strip()
                if response.css(
                    ".col-12.col-lg-10 .article-section-category::text"
                ).getall()
                else None
            ),
            "event_tags": None,
            "event_image": None,
            "event_link": response.css("event-detail-sidebar-test a href::text").get(),
            # Event timing
            "event_date": (
                event_json.get("startDate")[:10]
                if event_json and event_json.get("startDate")
                else None
            ),
            "event_init_hour": (
                event_json.get("startDate")[11:16]
                if event_json and event_json.get("startDate")
                else None
            ),
            "event_end_hour": (
                event_json.get("endDate")[11:16]
                if event_json and event_json.get("endDate")
                else None
            ),
            "event_comments_hour": None,
            # Event details
            "event_language": None,
            "event_age_restriction": None,
            # Place information
            "place_name": None,
            "place_name_2": None,
            "place_description": None,
            "place_address": None,
            "place_city": None,
            "place_coordinates": None,
            "place_link": None,
            # Artist information (primary artist)
            "artist_name": None,
            "artist_description": None,
            "artist_summary": None,
            "artist_link": None,
            "artist_genres": None,
            # Secondary artist
            "artist2_name": None,
            "artist2_description": None,
            "artist2_summary": None,
            "artist2_link": None,
            "artist2_genres": None,
            # Tertiary artist
            "artist3_name": None,
            "artist3_description": None,
            "artist3_summary": None,
            "artist3_link": None,
            "artist3_genres": None,
            # Pricing information
            "price_regular": None,
            "price_discounted1": None,
            "price_discounted1_comments": None,
            "price_discounted2": None,
            "price_discounted2_comments": None,
            "entrance_link": response.css(".mb-3 a href::text").get(),
        }

        self.event_data.append(event_data)
        yield event_data

    def closed(self):
        """Called when spider finishes - save all collected data"""
        from datetime import datetime

        # Create proper JSON structure
        output_data = {
            "title": "Events Scraped from Eco di Bergamo",
            "scraped_date": datetime.now().strftime("%Y-%m-%d"),
            "website": "www.ecodibergamo.it",
            "total_events": len(self.event_data),
            "events": self.event_data,
        }

        filename = f"events_{datetime.now().strftime('%Y%m%d')}.json"
        out_dir = Path("out")
        out_dir.mkdir(exist_ok=True)

        with open(out_dir / filename, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        self.logger.info(f"Saved {len(self.event_data)} events to {out_dir / filename}")

        # Send data to database
        self.parse_to_db()

    def parse_to_db(self):
        """Parse event data and send to database"""
        from db_parser.parser import DatabaseParser

        if not self.event_data:
            self.logger.warning("No event data to parse")
            return

        # Initialize database parser
        db_parser = DatabaseParser("events.db")

        try:
            # Insert events into database
            inserted_count = db_parser.insert_events(
                events_data=self.event_data, source_website="www.ecodibergamo.it"
            )

            self.logger.info(
                f"Successfully inserted {inserted_count} events into database"
            )

            # Get total count
            total_events = db_parser.get_events_count()
            self.logger.info(f"Total events in database: {total_events}")

        except Exception as e:
            self.logger.error(f"Error inserting events into database: {e}")
