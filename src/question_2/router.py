from fastapi import APIRouter

from src.question_2.utils import create_store_embeddings_and_query, scrape_video_data_from_url
from src.constants import SUCCESS_RESPONSE_MESSAGE, LINK_REFERENCE_IN_RESPONSE, COMPLETE_YOUTUBE_URL, \
    RECIPE_DONT_KNOW_MESSAGE_CHECK, UNABLE_TO_FETCH_DATA_RESPONSE_MESSAGE, ERROR_RESPONSE_MESSAGE

youtube_data_router = APIRouter(prefix="/youtube", tags=["YouTube"])


@youtube_data_router.get("/get_data")
def get_data_from_youtube_videos():
    """
    API to fetch the recipe data from YouTube video URLs from Chef Ranveer Brar's Website
    :return: data from the YouTube Video like title, source (URL), author, data (Data in string format)
    """
    try:
        video_data_to_return = []
        video_data = scrape_video_data_from_url()
        for data in video_data:
            source_url = data.metadata.get('source')
            video_data_to_return.append(
                {
                    "title": data.metadata.get('title'),
                    "source": COMPLETE_YOUTUBE_URL.format(source=source_url),
                    "author": data.metadata.get('author'),
                    "data": data.page_content.replace("\n", " ").replace("\t", " ").strip()
                }
            )
        return {"message": SUCCESS_RESPONSE_MESSAGE, "data": video_data_to_return}
    except Exception as error:
        return {"message": ERROR_RESPONSE_MESSAGE.format(error=error), "data": None}


@youtube_data_router.get("/get_answers")
def get_answers_from_youtube_videos(question: str):
    """
    API to question the RAG ti get the answers from LLM, and YouTube Videos
    :param question: Question to ask LLM using retriever
    :return: The response generated from the LLM.
    """
    try:
        data = create_store_embeddings_and_query(question)
        source = data.get('context')[0].metadata.get('source')
        answer = data.get('answer').strip().replace("\n", "").replace("\t", "")
        return_message = SUCCESS_RESPONSE_MESSAGE
        if answer != "" and RECIPE_DONT_KNOW_MESSAGE_CHECK not in answer:
            source_url = COMPLETE_YOUTUBE_URL.format(source=source)
            answer += LINK_REFERENCE_IN_RESPONSE.format(source=source_url)
        else:
            return_message = UNABLE_TO_FETCH_DATA_RESPONSE_MESSAGE.format(question=question)
        return {"message": return_message,
                "question": question,
                "answer": answer,
                }
    except Exception as error:
        return {"message": ERROR_RESPONSE_MESSAGE.format(error=error), "question": question, "answer": None}
