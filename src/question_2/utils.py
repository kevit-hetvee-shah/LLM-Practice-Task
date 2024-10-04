import os

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import YoutubeLoader
import requests
from src.constants import RECIPE_PROMPT, FORM_DATA, REQUEST_HEADERS, CHEFS_RECIPE_URL, CONTENT_FETCHING_EXCEPTION, \
    ERROR_RESPONSE_MESSAGE, LANGUAGE_TRANSCRIPTION_ERROR
from bs4 import BeautifulSoup
from langchain_core.prompts import ChatPromptTemplate
RECIPE_DB_PATH=os.path.dirname(os.path.realpath(__file__))
from src.common import llm, embeddings


def get_data():
    youtube_links = []
    try:
        response = requests.post(url=CHEFS_RECIPE_URL,
                                 data=FORM_DATA, headers=REQUEST_HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        links = {link.get('href') for link in soup.find_all("a")}
        print(f"Found {len(links)} links.")
        for link in list(links):
            try:
                link_response = requests.get(link, headers=REQUEST_HEADERS)
                soup = BeautifulSoup(link_response.content, "html.parser")
                youtube_url = [i.get('href') for i in soup.find_all("a") if "youtube.com/watch" in i.get("href")]
                youtube_links.extend(youtube_url)
            except Exception as error:
                print(CONTENT_FETCHING_EXCEPTION.format(link=link, error=error))
        return youtube_links
    except Exception as e:
        print(ERROR_RESPONSE_MESSAGE.format(error=e))
        return youtube_links


def scrape_video_data_from_url():
    links = get_data()
    videos_data = []
    for youtube_link in links:
        try:
            youtube_audio_loader = YoutubeLoader.from_youtube_url(youtube_link, add_video_info=True,
                                                                  language=["en-IN"],
                                                                  translation="en", )
            youtube_data = youtube_audio_loader.load()
            videos_data.extend(youtube_data)
        except Exception:
            print(CONTENT_FETCHING_EXCEPTION.format(link=youtube_link, error=LANGUAGE_TRANSCRIPTION_ERROR))
    return videos_data


def create_store_embeddings_and_query(question):
    """Only for the first time"""
    # video_data = scrape_video_data_from_url()
    # chroma_vector_store = Chroma.from_documents(documents=video_data, embedding=embeddings,
    #                                             persist_directory="/home/kevit/PycharmProjects/prac_proj/src/question_2")
    chroma_vector_store = Chroma(embedding_function=embeddings,
                                 persist_directory=RECIPE_DB_PATH)
    retriever = chroma_vector_store.as_retriever(search_kwargs={"k": 1})

    recipe_chatbot_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", RECIPE_PROMPT),
            ("human", "{input}")
        ]
    )
    recipe_stuff_documents_chain = create_stuff_documents_chain(llm, recipe_chatbot_prompt)
    recipe_retrieve_documents_chain = create_retrieval_chain(retriever, recipe_stuff_documents_chain)
    return recipe_retrieve_documents_chain.invoke({"input": question})


