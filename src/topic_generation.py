from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
from constants import topic_model
import os 
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")

class TopicGeneration:
    def __init__(self,title,summaries,save_model=False):
        self.title = title
        self.summaries = summaries
        self.save_model = save_model
    
    def generate_topics(self):
       topics_list = []
       try:
           model = SentenceTransformer(topic_model, token=hf_token)
           kw_model = KeyBERT(model)
           
           for t in range(len(self.title)):
                text = self.title[t]+" "+self.summaries[t]
                keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=3)
                topics = [keyword[0].capitalize() for keyword in keywords]
                topics_list.append(topics) 
           
           if self.save_model:
                model.save(f'./model/{topic_keyword_generation}')
           return topics_list    
       except Exception as e:
        raise ValueError(f"Could not create topic list {e}")  

    def generate_common_topics(self):
        topics_freq = {}
        try:
            topics_list = self.generate_topics()
            temp = topics_list
            temp = [t1 for t in temp for t1 in t]
            for topics in temp:
                if topics not in topics_freq:
                    topics_freq[topics] = 1
                else:
                    topics_freq[topics] += 1

            return [key for key, value in topics_freq.items() if value > 1]
        except Exception as e:
            raise ValueError("Couldn't load the common topics")
 