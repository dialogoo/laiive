from pathlib import Path
from scrapy.crawler import CrawlerProcess
from config import settings
from spiders.eppen_music import EppenMusicSpider


def run():
    # Convert Pydantic settings to dictionary for Scrapy
    scrapy_settings = settings.model_dump()

    # Set up output directory
    out_dir = Path("out")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Add output directory to settings
    scrapy_settings["OUTPUT_DIR"] = str(out_dir)

    process = CrawlerProcess(scrapy_settings)
    process.crawl(EppenMusicSpider)
    process.start()


if __name__ == "__main__":
    run()
