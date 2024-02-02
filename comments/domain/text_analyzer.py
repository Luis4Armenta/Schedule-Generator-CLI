from typing import List
from pydantic import BaseModel
from abc import ABC, abstractclassmethod

class SentimentAnalysis(BaseModel):
  positive_score: float
  neutral_score: float
  negative_score: float

class TextAnalyzer(ABC):

  @abstractclassmethod
  def analyze_sentiment(self, text: str) -> SentimentAnalysis:
    pass
  
  @abstractclassmethod
  def analyze_sentiment_by_block(self, texts: List[str]) -> List[SentimentAnalysis]:
    pass