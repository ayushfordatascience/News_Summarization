from langchain.prompts import PromptTemplate # Import LLMChain correctly
from langchain_huggingface import HuggingFaceEndpoint
from constants import llm_model
from itertools import combinations


import os
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")



class CoverageDifference:
    def __init__(self):
        self.llm = self.create_llm_model()
        if self.llm is None:
            raise ValueError("LLM model could not be initialized. Check your API token or model access.")

        self.comparison_prompt = self.create_comparison_prompt()
        self.impact_prompt = self.create_impact_prompt()
        
        self.comparison_chain = self.create_chain(self.comparison_prompt)
        self.impact_chain = self.create_chain(self.impact_prompt)

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

    def create_comparison_prompt(self):
        return PromptTemplate(
            input_variables=["article1", "article2"],
            template=(
                """Compare the following two articles:
                Article 1: {article1}
                Article 2: {article2}

                Provide a short comparison 
                in not more than 50 words and 
                in a single sentence."""
            )
        )

    def create_impact_prompt(self):
        return PromptTemplate(
            input_variables=["comparison"],
            template=(
                "Based on this comparison: {comparison}, "
                "what is the impact on public perception or market sentiment? "
                "Answer in less than 50 words within a single sentence."
            )
        )

    def create_chain(self, prompt_template):
        if self.llm is None:
            raise ValueError("LLM is None. Cannot create an LLMChain.")
        return prompt_template|self.llm  

    def create_coverage_differences(self, articles):
        coverage_differences = []

        for article1, article2 in combinations(articles, 2):
            article1_summary = f"{article1['Title']}: {article1['Summary']}"
            article2_summary = f"{article2['Title']}: {article2['Summary']}"

            try:
                comparison = self.comparison_chain.invoke(
                    {"article1": article1_summary, "article2": article2_summary}
                )
                impact = self.impact_chain.invoke({"comparison": comparison})

                coverage_differences.append({
                    "Comparison": comparison,
                    "Impact": impact
                })
            except Exception as e:
                print(f"Error processing articles {article1['Title']} and {article2['Title']}: {e}")

        return coverage_differences
