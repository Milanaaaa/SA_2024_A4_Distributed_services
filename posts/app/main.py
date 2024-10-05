import os
import httpx

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

USERS_BASE_URL = os.getenv('USERS_BASE_URL')

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


class CreatePost(BaseModel):
    username: str = Field(
        ..., pattern=r'^[a-zA-Z][a-zA-Z0-9_]{4,31}$'
    )
    content: str = Field(
        ..., min_length=1, max_length=400
    )


class CreateLike(BaseModel):
    username: str


posts: list[Post] = []


async def check_user(username: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(USERS_BASE_URL + f'/users/{username}')
        if r.status_code not in (200, 201):
            raise HTTPException(
                status_code=400,
                detail=f'User with username {username} not registered'
            )


@app.get('/posts', response_model=list[Post])
def get_posts():
    return posts


@app.post("/posts", response_model=Post)
async def send_post(post: CreatePost):
    username = post.username.strip()
    content = post.content.strip()

    await check_user(username)

    new_post = Post(
        id=len(posts),
        username=username,
        content=content
    )

    posts.append(new_post)

    return new_post


@app.post('/posts/{post_id}/like')
async def like_post(post_id: int, like: CreateLike):
    username = like.username.strip()

    await check_user(username)

    try:
        post = next(p for p in posts if p.id == post_id)
    except StopIteration:
        raise HTTPException(
            status_code=404,
            detail='Post not found'
        )

    if username in post.liked_by:
        post.liked_by.remove(username)
    else:
        post.liked_by.append(username)
