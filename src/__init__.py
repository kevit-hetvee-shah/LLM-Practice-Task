from fastapi import FastAPI
from src.question_1.router import scrape_data_router
from src.question_2.router import youtube_data_router


def create_app():
    app = FastAPI()
    app.include_router(scrape_data_router)
    app.include_router(youtube_data_router)
    return app
