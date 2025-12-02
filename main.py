import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import URLPatternFilter, FilterChain

from pprint import pprint
import json

async def main():
    
    # only follow urls ending with type=standard
    url_filter = URLPatternFilter(patterns=[r'type=standard$'])
    filter_chain = FilterChain(filters=[url_filter])
    
    # Configure a 2-level deep crawl
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=3, 
            include_external=False,
            filter_chain=filter_chain
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True
    )
    
    async with AsyncWebCrawler() as crawler:
        while True: 
            keyword = input("Enter job keyword to search (or type 'q' to quit):")
            if keyword.lower() == "q":
                print("Exiting the program.")
                break
            
            # get all the urls for each job ad.
            search_url = f"https://hk.jobsdb.com/{keyword}-jobs"
            results = await crawler.arun(url=search_url, config=config)
            print(f"Crawled {len(results)} pages in total")
            jobAd_urls = [result.url for result in results if result.url.endswith("type=standard")]
            jobAd_markdowns = [result.markdown for result in results if result.url.endswith("type=standard")]
            
            # scrape all the information (title, company, location, salary, etc.) from each job ad page.
            
            for url, jobAd in zip(jobAd_urls, jobAd_markdowns):
                print(f"Job Ad URL: {url}")
                print("Job Ad Content:")
                print(jobAd)
                print("-" * 80)

    return 


# main entry point.        
if __name__ == "__main__":
    asyncio.run(main())
