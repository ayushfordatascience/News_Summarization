from constants import text_classification,text_classification_model
from ..utils import build_model_from_transformers
import pandas as pd

class Sentiment:
    def __init__(self,summaries):
        self.summaries = summaries

    def get_sentiments(self):
        try:
           sent_pipe = build_model_from_transformers(text_classification_model,text_classification)
           for summ in summaries:
               return [sent_pipe(summ)[0]['label'] for summ in self.summaries]
        except Exception as e:
            raise RuntimeError(f"Error in sentiment analysis: {str(e)}") from e

    def generate_sentiment_distribution(self):
        sent_dis = {}
        try:
            sentiments = self.get_sentiments()
            
            df = pd.DataFrame(sentiments,columns=['Label'])
            res = df['Label'].value_counts()
            
            index = list(res.index)
            vals = list(res.values)
            
            for idx in range(len(index)):
                sent_dis[index[idx]] = int(vals[idx])
            
            return sent_dis
        except Exception as e:
            raise ValueError(f'Could not create sentiment distribution {e}') 
