import scrapy
from datetime import datetime
import re
from urllib.parse import urljoin


class EppenMusicSpider(scrapy.Spider):
    name = "eppen_music"
    start_urls = ["https://www.ecodibergamo.it/eventi/eppen"]

    custom_settings = {
        "DOWNLOAD_DELAY": 3.0,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 3.0,
        "AUTOTHROTTLE_MAX_DELAY": 10.0,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 0.3,
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT": "Laiive/0.0.1 (+https://laiive.com/contact)",
        "COOKIES_ENABLED": False,
        "HTTPCACHE_ENABLED": False,
        "DOWNLOAD_TIMEOUT": 30,
        "RETRY_TIMES": 2,
        "RETRY_HTTP_CODES": [500, 502, 503, 504, 408, 429],
        "LOG_LEVEL": "DEBUG",  # Changed to DEBUG for more info
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_count = 0
        self.start_time = datetime.now()
        self.logger.info("=== EPPEN MUSIC EVENTS SCRAPING SESSION STARTED ===")

    def parse(self, response):
        """Parse the main music category page"""
        self.request_count += 1
        self.log_metrics()

        self.logger.info(f"Parsing music category page: {response.url}")
        self.logger.info(f"Response status: {response.status}")
        self.logger.info(f"Response body length: {len(response.body)}")

        # Save the HTML for debugging
        with open("debug_response.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        self.logger.info("Saved debug_response.html for inspection")

        # Extract event listings from the main page
        yield from self.extract_event_listings(response)

        # Look for pagination or "load more" functionality
        yield from self.follow_pagination(response)

    def extract_event_listings(self, response):
        """Extract event listings from the main music page"""
        # Look for event containers - try multiple selectors
        selectors_to_try = [
            'div[class*="event"]',
            'div[class*="card"]',
            "article",
            ".event-item",
            ".card",
            '[class*="event"]',
            "div",
            "section",
        ]

        event_containers = []
        for selector in selectors_to_try:
            containers = response.css(selector)
            self.logger.info(f"Selector '{selector}' found {len(containers)} elements")
            if containers:
                event_containers = containers
                self.logger.info(f"Using selector: {selector}")
                break

        self.logger.info(f"Found {len(event_containers)} potential event containers")

        # If no containers found, try to find any content
        if not event_containers:
            self.logger.warning("No event containers found, checking page content...")
            all_text = response.css("::text").getall()
            self.logger.info(f"Total text elements found: {len(all_text)}")
            if all_text:
                self.logger.info(f"First few text elements: {all_text[:5]}")

            # Try to find any links
            all_links = response.css("a::attr(href)").getall()
            self.logger.info(f"Total links found: {len(all_links)}")
            if all_links:
                self.logger.info(f"First few links: {all_links[:5]}")

            # Create a dummy event to see if output works
            yield {
                "title": "DEBUG: No events found",
                "url": response.url,
                "status": "No event containers detected",
                "text_elements": len(all_text),
                "links": len(all_links),
                "timestamp": datetime.now().isoformat(),
            }
            return

        for i, container in enumerate(
            event_containers[:10]
        ):  # Limit to first 10 for debugging
            self.logger.info(f"Processing container {i+1}")

            # Extract basic event info from listing
            event_data = self.extract_basic_event_info(container, response.url)
            if event_data:
                self.logger.info(
                    f"Extracted event: {event_data.get('title', 'No title')}"
                )
                # Follow the detail page link to get full event information
                detail_link = self.extract_detail_link(container)
                if detail_link:
                    full_url = urljoin(response.url, detail_link)
                    self.logger.info(f"Following detail link: {full_url}")
                    yield scrapy.Request(
                        url=full_url,
                        callback=self.parse_event_detail,
                        meta={"basic_event_data": event_data},
                    )
                else:
                    # If no detail link, yield what we have
                    self.logger.info("No detail link found, yielding basic data")
                    yield event_data
            else:
                self.logger.warning(
                    f"Could not extract event data from container {i+1}"
                )

    def extract_basic_event_info(self, container, page_url):
        """Extract basic event information from listing container"""
        try:
            # Title - try multiple selectors
            title_selectors = [
                "h1",
                "h2",
                "h3",
                "h4",
                ".title",
                ".event-title",
                "strong",
                "b",
            ]
            title = None
            for selector in title_selectors:
                title_elem = container.css(f"{selector}::text").get()
                if title_elem and title_elem.strip():
                    title = title_elem.strip()
                    break

            # Date and time
            date_elem = container.css('.date, .event-date, [class*="date"]::text').get()
            time_elem = container.css('.time, .event-time, [class*="time"]::text').get()

            # Location
            location = container.css(
                '.location, .venue, .place, [class*="location"]::text'
            ).get()
            location = location.strip() if location else None

            # Category/tags
            category = container.css('.category, .tag, [class*="category"]::text').get()
            category = category.strip() if category else "Musica"

            # Description/summary
            description = container.css(
                ".description, .summary, .excerpt, p::text"
            ).get()
            description = description.strip() if description else None

            # Image
            image = container.css("img::attr(src)").get()
            if image:
                image = urljoin(page_url, image)

            # Get all text content for debugging
            all_text = container.css("::text").getall()
            all_text = [text.strip() for text in all_text if text.strip()]

            if title or all_text:  # Create event if we have any content
                return {
                    "title": title,
                    "date": date_elem.strip() if date_elem else None,
                    "time": time_elem.strip() if time_elem else None,
                    "location": location,
                    "category": category,
                    "description": description,
                    "image": image,
                    "source": "ecodibergamo",
                    "extraction_method": "music_listing",
                    "page_url": page_url,
                    "scraped_at": datetime.now().isoformat(),
                    "debug_text": all_text[:5],  # First 5 text elements for debugging
                    "debug_container_class": container.attrib.get("class", "no-class"),
                }

        except Exception as e:
            self.logger.error(f"Error extracting basic event info: {e}")

        return None

    def extract_detail_link(self, container):
        """Extract the link to the event detail page"""
        # Look for links that contain 'dettaglio' or similar
        detail_links = container.css('a[href*="dettaglio"]::attr(href)').getall()
        if detail_links:
            return detail_links[0]

        # Fallback: look for any link that might be the event link
        all_links = container.css("a::attr(href)").getall()
        for link in all_links:
            if "eventi" in link and not link.startswith("#"):
                return link

        return None

    def parse_event_detail(self, response):
        """Parse individual event detail page"""
        self.request_count += 1
        self.log_metrics()

        basic_data = response.meta.get("basic_event_data", {})

        self.logger.info(f"Parsing event detail: {response.url}")

        # Extract detailed event information
        detailed_data = self.extract_detailed_event_info(response)

        # Merge basic and detailed data
        complete_event = {**basic_data, **detailed_data}
        complete_event["detail_url"] = response.url
        complete_event["extraction_method"] = "music_detail_page"

        yield complete_event

    def extract_detailed_event_info(self, response):
        """Extract detailed information from event detail page"""
        detailed_data = {}

        try:
            # Full title (might be more detailed than listing)
            full_title = response.css("h1, .event-title, .title::text").get()
            if full_title:
                detailed_data["full_title"] = full_title.strip()

            # Full description
            description_elements = response.css(
                ".description, .content, .event-content, article p::text"
            ).getall()
            if description_elements:
                full_description = " ".join(
                    [elem.strip() for elem in description_elements if elem.strip()]
                )
                detailed_data["full_description"] = full_description

            # Event details
            details = response.css(".event-details, .details, .info::text").getall()
            if details:
                detailed_data["event_details"] = [
                    detail.strip() for detail in details if detail.strip()
                ]

            # Additional images
            images = response.css("img::attr(src)").getall()
            if images:
                detailed_data["all_images"] = [
                    urljoin(response.url, img) for img in images
                ]

            # Event metadata
            metadata = response.css(".metadata, .meta, .event-meta::text").getall()
            if metadata:
                detailed_data["metadata"] = [
                    meta.strip() for meta in metadata if meta.strip()
                ]

            # Price information
            price = response.css('.price, .cost, [class*="price"]::text').get()
            if price:
                detailed_data["price"] = price.strip()

            # Contact information
            contact = response.css(
                '.contact, .info-contact, [class*="contact"]::text'
            ).getall()
            if contact:
                detailed_data["contact_info"] = [
                    c.strip() for c in contact if c.strip()
                ]

            # Event URL (if different from current page)
            event_url = response.css(
                'a[href*="event"], a[href*="ticket"]::attr(href)'
            ).get()
            if event_url:
                detailed_data["event_url"] = urljoin(response.url, event_url)

        except Exception as e:
            self.logger.error(f"Error extracting detailed event info: {e}")

        return detailed_data

    def follow_pagination(self, response):
        """Follow pagination links if they exist"""
        # Look for pagination links
        next_page = response.css(
            ".pagination .next a::attr(href), .next-page::attr(href)"
        ).get()
        if next_page:
            next_url = urljoin(response.url, next_page)
            self.logger.info(f"Following pagination to: {next_url}")
            yield scrapy.Request(url=next_url, callback=self.parse)

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

        self.logger.info("=== EPPEN MUSIC EVENTS SCRAPING SESSION ENDED ===")
        self.logger.info(f"Total requests: {self.request_count}")
        self.logger.info(f"Total time: {total_time:.1f} seconds")
        self.logger.info(
            f"Average rate: {(self.request_count / total_time) * 60:.2f} requests/min"
        )
