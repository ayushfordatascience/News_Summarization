from langchain.prompts import PromptTemplate
from itertools import combinations

from utils import create_llm_model

class CoverageDifference:
    def __init__(self):
        self.llm = create_llm_model()
    
    def create_comparison_prompt():
        try:
            comparison_prompt = PromptTemplate(
                input_variables=["article1", "article2"],
                template="Compare the following two articles:\n\nArticle 1: {article1}\n\nArticle 2: {article2}\n\nProvide a short comparison for each of the articles in a single sentence."
            ) 
            return comparison_prompt
        except Exception as e:
            raise e
    
    
    def create_impact_prompt():
        try:
            impact_prompt = PromptTemplate(
                input_variables=["comparison"],
                template="Based on this comparison: {comparison}, what is the impact on public perception or market sentiment? Anser the question in a single sentence"
            ) 
            return impact_prompt
        except Exception as e:
            raise e

    def create_chains(type):
        try:
            chain = type|self.llm
            return chain
        except Exception as e:
            raise e 

    def create_coverage_differences(articles,comparison_chain,impact_chain):
        coverage_differences=[]
        try:
            for article1, article2 in combinations(final_dict["Articles"], 2):
                article1_summary = f"{article1['Title']}: {article1['Summary']}"
                article2_summary = f"{article2['Title']}: {article2['Summary']}"

                # Generate comparison
                comparison = comparison_chain.invoke([article1_summary,article2_summary])

                # Generate impact
                impact = impact_chain.invoke(comparison=comparison)

                coverage_differences.append({
                    "Comparison": comparison,
                    "Impact": impact
                })

            return coverage_differences
        except Exception as e:
            raise e          

       