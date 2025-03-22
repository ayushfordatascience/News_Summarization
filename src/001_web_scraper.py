from ..utils import get_response

from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

import os
from dotenv import load_dotenv


class WebScraper:
    def __init__(self,company):
        self.company = company
        load_dotenv()
        self.site = os.getenv("SITE_LINK")
        self.news_links = self.get_news_links()

    def get_news_links(self):
        try:
            if not self.company:
                raise ValueError("Company name cannot be empty")
            
            search = DDGS()
            query = f"Top news for {self.company} Company site:{self.site}"
            
            news = search.news(query,max_results=10)
            
            return [item["url"] for item in news]
            
        except ValueError as ve:
            raise ve   
        except Exception as e:
            raise RuntimeError(f"Error fetching news links for {self.company}: {e}")           
            
    def get_headings(self):
        script_tags = ["script", "noscript", "style"]
        headings=[]
        try:
            responses = get_response(self.news_links)
            for res in responses:
                soup = BeautifulSoup(res)

                for script in soup(script_tags):
                    script.decompose()

                h1_tags = soup.select("h1")
                if h1_tags:
                    headings.append(h1_tags[0].text)
                else:
                    headings.append("No headings found")    
        except Exception as e:
            raise RuntimeError(f"Error extracting headings {e}")            
        
        return headings
    
    def get_summary(self):
        script_tags = ["script", "noscript", "style"]
        summaries=[]
        try:
            responses = get_response(news_links)
            for res in responses:
                soup = BeautifulSoup(res)
                
                for script in soup(script_tags):
                    script.decompose()
                
                h1_tags = soup.select('h1')
                if not h1_tags:
                    summaries.append(["No Content Found"])
                    continue


                h2_after_h1=[]
                siblings = h1_tags[0].find_next_siblings()
                for sibling in siblings:
                    if sibling.name == 'h2':
                        h2_after_h1.append(sibling.get_text())
                    else:
                        break
                    
                summaries.append(h2_after_h1 if h2_after_h1 else ["No Content Found"])
        except Exception as e: 
            raise RuntimeError(f"Error extracting summaries: {e}")           
        return summaries