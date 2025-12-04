from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate

import json

def extract_job_data(llm_model: str, job_content: str, logger) -> dict:
    
    """Extract structured job data from unstructured job description using LLM."""
    
    prompt = PromptTemplate(
        input_variables=["job_content"],
        template=(
            "You are an information extraction assistant. "
            "Your task is to read the following job description and extract specific fields.\n\n"
            "Job Description:\n{job_content}\n\n"
            "Return ONLY valid JSON with the following structure:\n\n"
            "{{\n"
            '  "title": "",\n'
            '  "company": "",\n'
            '  "location": "",\n'
            "}}\n\n"
            "Rules:\n"
            "- Do not add explanations or text outside the JSON.\n"
            "- Use empty strings or empty arrays if information is missing.\n"
            "- Ensure the JSON is syntactically valid."
        ),
    )

    llm = OllamaLLM(model=llm_model, temperature=0)
    llm_chain = prompt | llm
    response = llm_chain.invoke({"job_content": job_content})
    logger.info(f"LLM Response: {response}")

    return response


def get_metadata_from_jobAd(job_contents: list, keyword: str, logger, llm_model:str) -> list[dict]:
    
    metadatas = []
    for content in job_contents:
        if content.success:
            metadata = extract_job_data(
                llm_model=llm_model,
                job_content=content.markdown,
                logger=logger
            )
            metadata["url"] = content.url
            metadata["keyword"] = keyword
            logger.info("Extracted Metadata:")
            logger.info(json.dumps(metadata, indent=2, ensure_ascii=False))
            metadatas.append(metadata)
    
    return metadatas