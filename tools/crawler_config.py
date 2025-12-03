"""Crawler configuration and initialization."""

from crawl4ai import CrawlerRunConfig, LLMConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import URLPatternFilter, FilterChain
from crawl4ai import LLMExtractionStrategy

from tools.models import JobAd


def create_url_filter() -> FilterChain:
    """Create URL filter to match job advertisement pages."""
    url_filter = URLPatternFilter(patterns=[r"type=standard$"])
    return FilterChain(filters=[url_filter])


def create_llm_strategy() -> LLMExtractionStrategy:
    """Create LLM extraction strategy for job ad parsing."""
    return LLMExtractionStrategy(
        llm_config=LLMConfig(provider="ollama/phi3:3.8b"),
        schema=JobAd.model_json_schema(),
        extraction_type="schema",
        instruction="Extract post title, company name, url, responsibilities, qualifications, salary and experience from the content of job advertisement.",
        chunk_token_threshold=1000,
        overlap_rate=0.0,
        apply_chunking=True,
        input_format="markdown",
    )


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
        extraction_strategy=create_llm_strategy(),
    )
