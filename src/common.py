from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import os

load_dotenv()
llm = GoogleGenerativeAI(model="gemini-pro", api_key=os.environ.get('GOOGLE_API_KEY'))
embeddings = GoogleGenerativeAIEmbeddings(google_api_key=os.environ.get('GOOGLE_API_KEY'), model="models/embedding-001")
