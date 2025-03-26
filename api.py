from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import List, Dict


application = FastAPI()

stored_data=[]
class ArticleModel(BaseModel):
    Title: str
    Summary: str
    Sentiment: str
    Topics: List[str]

class CoverageDifferenceModel(BaseModel):
    Comparison: str
    Impact: str

class SentimentDistributionModel(BaseModel):
    positive: int
    neutral: int
    negative: int
class TopicOverlapModel(BaseModel):
    Common_Topics: List[str]
    Unique_Topics: Dict[str, List[str]] = Field(default_factory=dict) 
     # Dynamic keys: "Unique Topics in Article X"
    model_config = {"extra": "allow"}

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
    return {"message": "Data received successfully!", "received_data": data.model_dump_json()}

@application.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@application.get("/data")
def get_data():
    return {"stored_data": [item.model_dump_json() for item in stored_data]}
