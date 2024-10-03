from starlette.responses import RedirectResponse

from src import create_app


app = create_app()

@app.get("/")
async def docs_redirect():
    """
    API to route the app to Swagger Documentation.
    :return:
    """
    return RedirectResponse(url='/docs')