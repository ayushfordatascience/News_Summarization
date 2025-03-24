from langchain.prompts import PromptTemplate # Import LLMChain correctly
from langchain_huggingface import HuggingFaceEndpoint
from constants import llm_model

import os
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")


class FinalSentiment:
    def __init__(self):
        self.llm = self.create_llm_model()
        self.sentiment_prompt = self.create_sentiment_prompt()
        self.sentiment_chain = self.create_sentiment_chain(self.sentiment_prompt)

    def create_llm_model(self):
        try:
            llm = HuggingFaceEndpoint(
                repo_id=llm_model,
                huggingfacehub_api_token=hf_token,
                max_new_tokens=250,
                temperature=0.7
            )

            if llm is None:
                raise ValueError("HuggingFaceEndpoint returned None. Check your API token or model access.")
            return llm
        except Exception as e:
            raise RuntimeError(f"Error initializing LLM model '{llm_model}': {e}")

    def create_sentiment_prompt(self):
        return PromptTemplate(
            input_variables=["articles"],
            template=(
                """
                You are given a list of {articles}
                which has titles and summaries. Read each 
                and every article and offer a conclusion
                on how the company is doing whether theoutlook is
                positive or negative in less than 10 words.
                """
            )
        )
    
    
    def create_sentiment_chain(self, prompt_template):
        if self.llm is None:
            raise ValueError("LLM is None. Cannot create an LLMChain.")
        return prompt_template|self.llm
    
    def generate_final_sentiment(self,articles):
        try:
            final_sentiment = self.sentiment_chain.invoke(
                {"articles":articles}
            )
        except Exception as e:
           print(f"Error processing articles {articles}: {e}")    
        return final_sentiment   