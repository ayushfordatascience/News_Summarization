from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import json

application = FastAPI()


class ArticleModel(BaseModel):
    Title: str
    Summary: str
    Sentiment: str
    Topics: List[str]

class CoverageDifferenceModel(BaseModel):
    Comparison: str
    Impact: str

class SentimentDistributionModel(BaseModel):
    Positive: int
    Neutral: int

class TopicOverlapModel(BaseModel):
    Common_Topics: List[str]
    Unique_Topics_in_Article_1: List[str]
    Unique_Topics_in_Article_2: List[str]

class ComparativeSentimentScoreModel(BaseModel):
    Sentiment_Distribution: SentimentDistributionModel
    Coverage_Differences: List[CoverageDifferenceModel]
    Topic_Overlap: TopicOverlapModel

class DataModel(BaseModel):
    Company: str
    Articles: List[ArticleModel]
    Comparative_Sentiment_Score: ComparativeSentimentScoreModel
    Final_Sentiment_Analysis: str
    Audio: str

stored_data: List[DataModel] = []


@application.post("/receive_data")
async def receive_data(data: DataModel):
    stored_data.append(data)
    return {"message": "Data received successfully!", "received_data": data.dict()}

@application.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@application.get("/data")
def get_data():
    return {"stored_data": [item.dict() for item in stored_data]}
