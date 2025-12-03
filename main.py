from fastapi import FastAPI
from pydantic import BaseModel

from dotenv import load_dotenv
from openai import OpenAI  # openai==1.52.2
import os

from starlette.responses import StreamingResponse

app = FastAPI()

load_dotenv()


class ChatRequest(BaseModel):
    prompt: str


@app.get("/hello")
async def hello():
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


def upstage_chat(message: ChatRequest):
    api_key = os.getenv("UPSTAGE_API_KEY")
    if not api_key:
        raise ValueError("UPSTAGE_API_KEY environment variable is required")
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.upstage.ai/v1"
    )
    stream = client.chat.completions.create(
        model="solar-pro2",
        messages=[
            {
                "role": "user",
                "content": message.prompt
            }
        ],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content

    # Use with stream=False
    # print(stream.choices[0].message.content)


@app.post("/chat")
def query(message: ChatRequest):
    return StreamingResponse(
        upstage_chat(message),
        media_type="text/plain; charset=utf-8"
    )
