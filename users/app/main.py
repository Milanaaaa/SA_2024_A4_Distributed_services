from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import sys
sys.path = ['', '..'] + sys.path[1:]


from db.config import SessionLocal, engine
from db.models import User

app = FastAPI()


@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)


async def get_db():
    async with SessionLocal() as session:
        yield session


class User(BaseModel):
    username: str = Field(
        ..., pattern=r'^[a-zA-Z][a-zA-Z0-9_]{4,31}$'
    )

    def __hash__(self):
        return hash(self.username)


users: set[User] = set()


@app.post('/register')
async def register(user: User, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=f'User with username {user.username} already exists'
        )
    db.add(user)
    await db.commit()
    return user


@app.get('/users/{username}', response_model=User)
async def get_user(username: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'User with username {username} does not exist'
        )
    return user
