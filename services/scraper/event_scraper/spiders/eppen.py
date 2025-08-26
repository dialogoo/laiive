import scrapy
from datetime import datetime
import re


class EppenSpider(scrapy.Spider):
    name = "eppen"
    start_urls = ["https://www.ecodibergamo.it/eventi/eppen/"]

    # Ethical scraping settings
    custom_settings = {
        "DOWNLOAD_DELAY": 5.0,  # 5 seconds between requests
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,  # Only 1 request at a time
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 5.0,
        "AUTOTHROTTLE_MAX_DELAY": 15.0,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 0.2,
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT": "LaiiveEventScraper/1.0 (+https://your-website.com/contact)",
        "COOKIES_ENABLED": False,
        "HTTPCACHE_ENABLED": False,
        "DOWNLOAD_TIMEOUT": 30,
        "RETRY_TIMES": 1,
        "RETRY_HTTP_CODES": [500, 502, 503, 504, 408, 429],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_count = 0
        self.start_time = datetime.now()
        self.logger.info("=== ETHICAL SCRAPING SESSION STARTED ===")

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.request_count += 1
        self.log_metrics()

        # Follow date links to find events
        yield from self.follow_date_links(response)

    def follow_date_links(self, response):
        """Follow date-specific links to find events"""
        date_links = response.css('a[href*="/eventi/data/"]::attr(href)').getall()
        self.logger.info(f"Found {len(date_links)} date links")

        for date_link in date_links:
            if date_link.startswith("/"):
                full_url = response.urljoin(date_link)
            else:
                full_url = date_link

            # Extract date from URL
            date_match = re.search(r"/data/(\d{4}/\d{2}/\d{2})/", date_link)
            date_str = date_match.group(1) if date_match else "unknown_date"

            yield scrapy.Request(
                url=full_url,
                callback=self.parse_date_page,
                meta={"date": date_str},
            )

    def parse_date_page(self, response):
        """Parse a specific date page to find events"""
        date = response.meta.get("date")
        self.logger.info(f"Parsing date page: {date}")

        # Extract events from this date page
        events = self.extract_events_from_date_page(response, date)

        for event in events:
            yield event

    def extract_events_from_date_page(self, response, date):
        """Extract events from a specific date page"""
        events = []
        event_containers = response.css('[class*="event"]')

        self.logger.info(f"Found {len(event_containers)} event containers for {date}")

        for container in event_containers:
            event_data = self.extract_single_event(container, date, response.url)
            if event_data:
                events.append(event_data)

        return events

    def extract_single_event(self, container, date, page_url):
        """Extract data from a single event container"""
        try:
            # Get text content
            text_content = container.css("::text").getall()
            text_content = [text.strip() for text in text_content if text.strip()]

            # Get links
            links = container.css("a::attr(href)").getall()

            # Get images
            images = container.css("img::attr(src)").getall()

            # Only create event if we have meaningful content
            if text_content and len(" ".join(text_content)) > 10:
                event_data = {
                    "date": date,
                    "page_url": page_url,
                    "text_content": text_content[:5],
                    "links": links[:3],
                    "images": images[:3],
                    "source": "ecodibergamo",
                    "extraction_method": "date_page_parsing",
                }

                # Add structured data if available
                structured_data = self.extract_structured_data(container)
                event_data.update(structured_data)

                return event_data

        except Exception as e:
            self.logger.error(f"Error extracting event: {e}")

        return None

    def extract_structured_data(self, container):
        """Extract structured event data from container"""
        structured_data = {}

        try:
            # Title
            title = container.css(
                ".event-title, .card-title, h3, h4, strong::text"
            ).get()
            if title:
                structured_data["title"] = title.strip()

            # Date/time
            date_elem = container.css(".card-day, .event-date, .date::text").get()
            if date_elem:
                structured_data["day"] = date_elem.strip()

            time_elem = container.css(".card-time, .event-time, .time::text").get()
            if time_elem:
                structured_data["time"] = time_elem.strip()

            # Location
            location = container.css(".event-location, .location, .venue::text").get()
            if location:
                structured_data["location"] = location.strip()

            # Category
            category = container.css(".event-category, .category, .tag::text").get()
            if category:
                structured_data["category"] = category.strip()

        except Exception as e:
            self.logger.error(f"Error extracting structured data: {e}")

        return structured_data

    def log_metrics(self):
        """Log basic scraping metrics"""
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        requests_per_minute = (
            (self.request_count / elapsed_time) * 60 if elapsed_time > 0 else 0
        )

        self.logger.info(
            f"Requests: {self.request_count}, Rate: {requests_per_minute:.2f}/min"
        )

    def closed(self, reason):
        """Called when spider is closed"""
        end_time = datetime.now()
        total_time = (end_time - self.start_time).total_seconds()

        self.logger.info("=== SCRAPING SESSION ENDED ===")
        self.logger.info(f"Total requests: {self.request_count}")
        self.logger.info(f"Total time: {total_time:.1f} seconds")
        self.logger.info(
            f"Average rate: {(self.request_count / total_time) * 60:.2f} requests/min"
        )
