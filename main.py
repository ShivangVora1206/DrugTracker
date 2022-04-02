from typing import List
from fastapi import FastAPI

app = FastAPI()

@app.get('/thing/{thing_id}')
async def root(thing_id: int):
    return {'message':thing_id}