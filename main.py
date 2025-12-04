"""JobsDB Crawler - Automated job advertisement extraction from JobsDB Hong Kong."""

import asyncio
import json
import logging
from typing import Optional
from pprint import pprint

from crawl4ai import AsyncWebCrawler
from tools.crawler_config import create_crawler_config, create_url_filter
from tools.data_extractor import get_metadata_from_jobAd

from dotenv import load_dotenv
import os

load_dotenv()


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="w",       # 'a' = append, 'w' = overwrite
    format="%(asctime)s - %(levelname)s - %(message)s"
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
            logger.info(f"job ad url: {result.url}")
            logger.info(f"extracted content:")
            logger.info(result.markdown)
            logger.info("-"*100)
        else:
            logger.error(f"Crawling failed for {result.url}: {result.error_message}")

    return extracted_count


async def search_jobs(crawler: AsyncWebCrawler, keyword: str):
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

    return results


async def main() -> None:
    """Main entry point for the JobsDB crawler application."""
    # logging startup message
    logger.info("Starting JobsDB Crawler")

    # load LLM model from environment variable
    OLLAMA_EXTRACTION_MODEL = os.getenv("OLLAMA_EXTRACTION_MODEL")
    
    async with AsyncWebCrawler() as crawler:
        while True:
            # Get user input for job keyword.
            keyword = input("\nEnter job keyword to search (or type 'q' to quit): ").strip()

            if keyword.lower() == "q":
                logger.info("Exiting the program.")
                break
            
            # Perform job search and extraction.
            try:
                job_contents = await search_jobs(crawler, keyword)
            except Exception as e:
                logger.error(f"An error occurred during search: {e}", exc_info=True) 

            # use LLM to extract data from unstructured content.
            metadatas = get_metadata_from_jobAd(
                job_contents=job_contents,
                keyword=keyword,
                logger=logger,
                llm_model=OLLAMA_EXTRACTION_MODEL
            )
            
             

if __name__ == "__main__":
    asyncio.run(main())
