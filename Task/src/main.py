from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from .agent.titanic_agent import TitanicAgent

load_dotenv()

app = FastAPI()
agent = TitanicAgent(os.getenv('GOOGLE_API_KEY'))

class Query(BaseModel):
    text: str

@app.post("/query")
async def process_query(query: Query):
    try:
        response = agent.process_query(query.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 