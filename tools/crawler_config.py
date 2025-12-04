"""Crawler configuration and initialization."""

from crawl4ai import CrawlerRunConfig, LLMConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import URLPatternFilter, FilterChain


def create_url_filter() -> FilterChain:
    """Create URL filter to match job advertisement pages."""
    url_filter = URLPatternFilter(patterns=[r"type=standard$"])
    return FilterChain(filters=[url_filter])


<<<<<<< HEAD
=======
def create_llm_strategy() -> LLMExtractionStrategy:
    """Create LLM extraction strategy for job ad parsing."""
    return LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="ollama/tinyllama",
            temperature=0.1,  # Lower temperature for faster, more deterministic output
        ),
        schema=JobAd.model_json_schema(),
        extraction_type="schema",
        instruction="Extract post title, company name, url, responsibilities, qualifications, salary and experience from the content of job advertisement.",
        chunk_token_threshold=500,  # Reduced chunk size for faster processing
        overlap_rate=0.0,
        apply_chunking=True,
        input_format="markdown",
    )


>>>>>>> 9e68eb14c87c7d57090c5257498bc6694ad3dd9e
def create_crawler_config(filter_chain: FilterChain) -> CrawlerRunConfig:
    """Create crawler configuration with deep crawling strategy."""
    return CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2,  # Reduced depth for faster crawling
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
