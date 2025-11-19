from crawl4ai import AsyncWebCrawler
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.chains import create_retrieval_chain

# Step 1: Crawl data
async def crawl_site(url: str):
    crawler = AsyncWebCrawler()
    result = await crawler.arun(url)
    
    return result


# main program.
def main():
    
    # configuration.
    OLLAMA_MODEL = "mistral"
    OLLAMA_EMBEDDING_MODEL = "mxbai-embed-large:latest"
    PRESIST_DIRECTORY = "./chroma_job_db"
    
    # initiate Ollama LLM.
    LLM = OllamaLLM(model=OLLAMA_MODEL)
    
    # initiate Ollama embeddings
    EMBEDDINGS = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL)
    
    # initiate vectorstore
    vector_store = Chroma(
        embedding_function=EMBEDDINGS, 
        collection_name="jobs_collection",
        persist_directory=PRESIST_DIRECTORY,
    )

    # chat loop.
    while True:
        question = input("Enter the keyword for jobs u wanna search (type 'q' for quit): ")

        # type q for breaking the chat loop.
        if question.lower() == "q":
            break
        
        # Crawl the web page.
        url = f"https://hk.jobsdb.com/{question}-jobs"
        docs = [crawl_site(url=url)]
        
        # Save docs to vectorstore.
        vector_store.add_texts(texts=docs)
        
        # Query with LangChain
        retriever=vector_store.as_retriever()
        # qa = RetrievalQA.from_chain_type(
        #     llm=OllamaLLM(model=OLLAMA_MODEL),
        #     retriever=retriever
        # )
        
        qa = create_retrieval_chain(retriever=retriever, )
        
        # return the summary.
        print(qa.run(f"Summarize the latest job ads for {question} related jobs."))

    return 


# main entry point.
if __name__ == "__main__":
    main()