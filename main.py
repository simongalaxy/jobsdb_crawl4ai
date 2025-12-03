"""JobsDB Crawler - Automated job advertisement extraction from JobsDB Hong Kong."""

import asyncio
import json
import logging
from typing import Optional

from crawl4ai import AsyncWebCrawler

from tools.crawler_config import create_crawler_config, create_url_filter
from tools.models import JobAd

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def process_search_results(crawler: AsyncWebCrawler, results) -> int:
    """
    Process and display crawled results.

    Args:
        crawler: The AsyncWebCrawler instance
        results: Crawled results from the crawler

    Returns:
        Number of successfully extracted job ads
    """
    extracted_count = 0

    for result in results:
        if result.success:
            try:
                data = json.loads(result.extracted_content)
                logger.info(f"Successfully extracted from {result.url}")
                logger.info(f"Extracted Data: {json.dumps(data, indent=2)}")
                extracted_count += 1
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from {result.url}: {e}")
        else:
            logger.error(f"Crawling failed for {result.url}: {result.error_message}")

    return extracted_count


async def search_jobs(crawler: AsyncWebCrawler, keyword: str) -> None:
    """
    Search for jobs with the given keyword and extract job advertisements.

    Args:
        crawler: The AsyncWebCrawler instance
        keyword: Job search keyword
    """
    logger.info(f"Searching for jobs with keyword: {keyword}")

    filter_chain = create_url_filter()
    crawl_config = create_crawler_config(filter_chain)

    search_url = f"https://hk.jobsdb.com/{keyword}-jobs"
    logger.info(f"Starting crawl from: {search_url}")

    results = await crawler.arun(url=search_url, config=crawl_config)
    extracted_count = await process_search_results(crawler, results)

    logger.info(f"Extraction complete. Successfully extracted {extracted_count} job ads.")


async def main() -> None:
    """Main entry point for the JobsDB crawler application."""
    logger.info("Starting JobsDB Crawler")

    async with AsyncWebCrawler() as crawler:
        while True:
            keyword = input("\nEnter job keyword to search (or type 'q' to quit): ").strip()

            if keyword.lower() == "q":
                logger.info("Exiting the program.")
                break

            if not keyword:
                logger.warning("Please enter a valid keyword.")
                continue

            try:
                await search_jobs(crawler, keyword)
            except Exception as e:
                logger.error(f"An error occurred during search: {e}", exc_info=True) 


if __name__ == "__main__":
    asyncio.run(main())
