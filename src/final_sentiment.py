from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from constants import openai_model

import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY is not set. Please check your environment variables.")

class FinalSentiment:
    def __init__(self):
        self.llm = self.create_llm_model()
        self.sentiment_prompt = self.create_sentiment_prompt()
        self.sentiment_chain = self.create_sentiment_chain()

    def create_llm_model(self):
        try:
            return ChatOpenAI(
                model=openai_model,  
                openai_api_key=openai_api_key,
                temperature=0.7
            )
        except Exception as e:
            raise RuntimeError(f"Error initializing OpenAI model: {e}")

    def create_sentiment_prompt(self):
        return PromptTemplate(
            input_variables=["articles"],
            template=(
                """
                You are given a list of {articles}
                which has titles and summaries. Read each 
                and every article and offer a conclusion
                on how the company is doing, whether the outlook is
                positive or negative, in less than 30 words.
                """
            )
        )

    def create_sentiment_chain(self):
        if self.llm is None:
            raise ValueError("LLM is None. Cannot create a processing chain.")
        return self.sentiment_prompt|self.llm

    def generate_final_sentiment(self, articles):
        try:
            final_sentiment = self.sentiment_chain.invoke({"articles": articles})
            return final_sentiment
        except Exception as e:
            print(f"Error processing articles {articles}: {e}")
            return None
