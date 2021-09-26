# src/app/main.py
from fastapi import FastAPI
from typing import List


app = FastAPI()


@app.get('/ping')
async def pong() -> dict:
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong"}
