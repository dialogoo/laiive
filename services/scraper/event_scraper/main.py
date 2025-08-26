from datetime import datetime
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from config.py import settings


def run():
    # Use the existing out directory where other JSONL files are located
    out_dir = Path("event_scraper/out")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"eppen_music_{datetime.now().strftime('%Y%m%d')}.jsonl"

    scrapy_settings  # TODO it requires a dict to continue

    process = CrawlerProcess(scrapy_settings)
    process.crawl("eppen_music")
    process.start()


if __name__ == "__main__":
    scrapy_settings = settings  # TODO tranform class into dict
    run()
