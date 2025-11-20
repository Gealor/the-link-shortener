from fastapi import FastAPI, Query
import uvicorn

from core.config import settings
from schemas.pydantic_schemas import URLShort
from services import ShortenerService


app = FastAPI()


@app.post("/short_url")
async def make_short_url(
    url: str = Query(),
) -> URLShort:
    '''
    Make shortener version of URL.
    '''
    return await ShortenerService().generate_and_safe_shortcut_url(url)

@app.get("/{code}")
async def redirect(
    code: str,
):
    '''
    Return full version url from shortener code
    '''
    pass


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.runtime.host,
        port=settings.runtime.port,
        reload=True,
    )