import os

from fastapi import FastAPI
from pydantic import BaseModel

from dotenv import load_dotenv
from openai import OpenAI  # openai==1.52.2
import os


load_dotenv()

class ChatRequest(BaseModel):
    prompt: str

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "Hello FastAPI!"}

@app.post("/query")
async def query(message: ChatRequest):
    api_key = os.getenv("UPSTAGE_API_KEY")
    if not api_key:
        raise ValueError("UPSTAGE_API_KEY environment variable is required")
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.upstage.ai/v1"
    )
    response = client.embeddings.create(
        input=message.prompt,
        model="embedding-query"
    )
    return response.data[0].embedding