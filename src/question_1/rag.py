from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.constants import ASSISTANT_PROMPT, KEVIT_WEBSITE, KEVIT_DATA_DB_PATH, PDF_PATH
from src.question_1.utils import load_pdf, crawl_website
from src.common import llm, embeddings
load_dotenv()

system_prompt_template = ASSISTANT_PROMPT


def create_documents_from_data():
    """
    Get the data from PDF file and create the documents by splitting their content
    :return: Documents with the split content
    """
    documents = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

    pdf_data = load_pdf(PDF_PATH)
    pdf_text_splitter = text_splitter.split_documents(pdf_data)

    documents.extend(pdf_text_splitter)

    data_dict = crawl_website(KEVIT_WEBSITE)
    for url, data in data_dict.items():
        website_text_splitter = text_splitter.create_documents([data], metadatas=[{"source": url}])
        documents.extend(website_text_splitter)
    return documents


def generate_results(question):
    """
    Initialize/load the Chroma VectorStore.
    Create the retriever from the VectorStore.
    Create the Prompt to be passed to LLM.
    Create Documents Chain to stuff the Prompt with LLM
    Create Retrieval Chain to retrieve the documents from retriever and pass them to Documents Chain
    Return the result obtained by invoking the chain
    :param question: The question to be asked to RAG.
    :return: The response received by invoking the chain.
    """

    """Only required for the 1st time."""
    # documents = create_documents_from_data()
    # chroma_vector_store = Chroma.from_documents(documents, embedding=embeddings, persist_directory="/home/kevit/PycharmProjects/prac_proj/src/question_1")

    """Now the embeddings are already created and stored, so directly use them."""
    chroma_vector_store = Chroma(embedding_function=embeddings, persist_directory=KEVIT_DATA_DB_PATH)
    retriever = chroma_vector_store.as_retriever(search_kwargs={"k":1})

    chatbot_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt_template),
            ("human", "{input}")
        ]
    )
    stuff_documents_chain = create_stuff_documents_chain(llm, chatbot_prompt)

    retrieve_documents_chain = create_retrieval_chain(retriever, stuff_documents_chain)

    return retrieve_documents_chain.invoke({"input": question})

