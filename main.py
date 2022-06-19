from fastapi import FastAPI, HTTPException
import uvicorn  # type: ignore
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {}

app = FastAPI()


@app.post('/reg')
async def reg(username: str, password: str):
    if username not in users:
        users[username] = pwd_context.hash(password)
        return {'token': pwd_context.hash(username)+users[username]}
    else:
        return HTTPException(status_code=400, detail="username is occupied")


@app.post('/auth')
async def auth(username: str, password: str):
    if username not in users:
        return HTTPException(status_code=404, detail='user is not registered')

    if username in users:
        if pwd_context.verify(password, users[username]):
            return {'token': pwd_context.hash(username)+users[username]}
        else:
            return HTTPException(status_code=404, detail='wrong password')


@app.get('/users')
async def all_users():
    return {'users': users}