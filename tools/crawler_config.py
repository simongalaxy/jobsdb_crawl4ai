"""Crawler configuration and initialization."""

from crawl4ai import CrawlerRunConfig, LLMConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import URLPatternFilter, FilterChain


def create_url_filter() -> FilterChain:
    """Create URL filter to match job advertisement pages."""
    url_filter = URLPatternFilter(patterns=[r"type=standard$"])
    return FilterChain(filters=[url_filter])


def create_crawler_config(filter_chain: FilterChain) -> CrawlerRunConfig:
    """Create crawler configuration with deep crawling strategy."""
    return CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=3,
            include_external=False,
            filter_chain=filter_chain,
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True,
        exclude_all_images=True,
        # exclude_external_links=True,
        exclude_social_media_domains=True,
        # Use valid CSS attribute selectors for better compatibility
        target_elements=['h1[data-automation="job-detail-title"]', 'div[data-automation="jobAdDetails"]'],
        # extraction_strategy=create_llm_strategy(),
    )
