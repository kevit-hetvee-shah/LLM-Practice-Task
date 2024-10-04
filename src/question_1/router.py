from src.constants import SUCCESS_RESPONSE_MESSAGE, ERROR_RESPONSE_MESSAGE, LINK_REFERENCE_IN_RESPONSE, \
    KEVIT_WEBSITE, KEVIT_DONT_KNOW_MESSAGE_CHECK, UNABLE_TO_FETCH_DATA_RESPONSE_MESSAGE, HANDBOOK_FILE_NAME
from src.question_1.rag import generate_results
from src.question_1.utils import crawl_website, load_pdf
from fastapi import APIRouter
import os
PDF_PATH = os.path.join(os.getcwd(), HANDBOOK_FILE_NAME)

scrape_data_router = APIRouter(prefix="/data", tags=["Kevit"])


@scrape_data_router.get("/get_pdf_data")
def fetch_data_from_pdf():
    """
    API to fetch the text data from Kevit Employee Handbook PDF.
    :return: Text content of the PDF.
    """
    try:
        doc_data = load_pdf(PDF_PATH)
        combined_data = [i.page_content.strip().replace("\n", "").replace("\t", "") for i in doc_data]
        data = "".join(combined_data)
        return {"message": SUCCESS_RESPONSE_MESSAGE, "data": data}
    except Exception as error:
        return {"message": ERROR_RESPONSE_MESSAGE.format(error=error), "data": None}


@scrape_data_router.get("/crawl_website")
def crawl_website_data():
    """
    API to crawl the websites of Kevit and extract the text content.
    :return: Text content from the crawled websites.
    """
    try:
        dict_data = crawl_website(KEVIT_WEBSITE)
        data = [dict_data.items()]
        return {"message": SUCCESS_RESPONSE_MESSAGE, "data": data}
    except Exception as error:
        print(error)
        return {"message": ERROR_RESPONSE_MESSAGE.format(error=error), "data": None}


@scrape_data_router.get("/get_answers")
def get_answers_from_extracted_data(question):
    """
    API to question the RAG to get answers from LLM, PDF, and Websites
    :param question: The question to ask LLM using retriever
    :return: The response generated from the LLM.
    """
    try:
        result = generate_results(question)
        source = result.get('context')[0].metadata.get('source')
        answer = result.get('answer').replace("\n", "").replace("\t", "").strip()

        return_message = SUCCESS_RESPONSE_MESSAGE

        if answer == "" or KEVIT_DONT_KNOW_MESSAGE_CHECK in answer:
            return_message = UNABLE_TO_FETCH_DATA_RESPONSE_MESSAGE.format(question=question)

        if "https" in source:
            answer += LINK_REFERENCE_IN_RESPONSE.format(source=source)

        return {"message": return_message, "question": question,
                "answer": answer}
    except Exception as error:
        return {"message": ERROR_RESPONSE_MESSAGE.format(error=error), "question": question, "answer": None}
