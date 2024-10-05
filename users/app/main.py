from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class User(BaseModel):
    username: str = Field(
        ..., pattern=r'^[a-zA-Z][a-zA-Z0-9_]{4,31}$'
    )

    def __hash__(self):
        return hash(self.username)


users: set[User] = set()


@app.post('/register')
async def register(user: User):
    if any(user.username == u.username for u in users):
        raise HTTPException(
            status_code=400,
            detail=f'User with username {user.username} already exists'
        )

    users.add(user)


@app.get('/users/{username}', response_model=User)
async def get_user(username: str):
    try:
        return next(
            u for u in users
            if username == u.username
        )
    except StopIteration:
        raise HTTPException(
            status_code=404,
            detail=f'User with username {username} does not exists'
        )
