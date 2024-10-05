import os
import httpx

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

POSTS_BASE_URL = os.getenv('POSTS_BASE_URL')

app = FastAPI()


class Post(BaseModel):
    id: int = Field(...)
    username: str = Field(
        ..., pattern=r'^[a-zA-Z][a-zA-Z0-9_]{4,31}$'
    )
    content: str = Field(
        ..., min_length=1, max_length=400
    )
    liked_by: list[str] = Field([])


class Feeds(BaseModel):
    posts: list[Post] = Field(..., max_length=10)


@app.get('/feed', response_model=Feeds)
async def get_feed():
    print(POSTS_BASE_URL)
    async with httpx.AsyncClient() as client:
        r = await client.get(POSTS_BASE_URL + '/posts')
        if r.status_code not in (200, 201):
            raise HTTPException(
                status_code=500,
                detail='Cannot retrieve messages'
            )

        return Feeds(posts=[Post(**post) for post in r.json()[-10:]])
