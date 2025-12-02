from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "Hello FastAPI!"}

@app.post("/query")
def query(message:str):
    # pip install openai
    from openai import OpenAI  # openai==1.52.2

    client = OpenAI(
        api_key="up_CQlRUTuZcA4l3YwnD7g9dAdT74hXw",
        base_url="https://api.upstage.ai/v1"
    )
    response = client.embeddings.create(
        input=message,
        model="embedding-query"
    )

    print(response.data[0].embedding)