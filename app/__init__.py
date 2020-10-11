
import os

from fastapi import FastAPI
from app.setup import *

app = FastAPI()


@app.get('/')
def index():
    return {"message": "Hello World"}
