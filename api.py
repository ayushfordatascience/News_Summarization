from fastapi import FastAPI
from pydantic import BaseModel
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
    Positive: int
    Neutral: int
    Negative: int
class TopicOverlap(BaseModel):
    Common_Topics: List[str]
    Unique_Topics: Dict[str, List[str]]  # Dynamic keys: "Unique Topics in Article X"
    
    def serialize(self):
        return {
            "Common Topics": self.Common_Topics,
            **{f"Unique Topics in Article {i+1}": topics for i, (key, topics) in enumerate(self.Unique_Topics.items())}
        }

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
