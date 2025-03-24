from src.web_scraper import WebScraper
from src.sentiment import Sentiment
from src.topic_generation import TopicGeneration
from src.coverage_differences import CoverageDifference
from src.final_sentiment import FinalSentiment
from src.generate_audio import GenerateAudio

import json
import streamlit as st

st.title('Business News Summarization App')

# api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# if not api_key:
#     st.warning("Please enter your OpenAI API key to proceed.")
# else:
company = st.text_input('Enter the name of the company:')

if st.button('Get Details of the company'):
    with st.spinner(f"Getting insights for {company} Company"):
        final_dict = {}
        final_dict['Company'] = company
        ws = WebScraper(company)
        links = ws.get_news_links()
        title = ws.get_headings(links)
        summaries = ws.get_summary(links)


        sentiment = Sentiment(summaries)
        sentiment_results = sentiment.get_sentiments()
        sentiment_distribution = sentiment.generate_sentiment_distribution(sentiment_results)


        topic_generation = TopicGeneration(title,summaries)
        topics_list = topic_generation.generate_topics()
        common_topics = topic_generation.generate_common_topics()

        articles = []
        for a in range(len(summaries)):
            articles.append({"Title":title[a],
                             "Summary":summaries[a],
                             "Sentiment":sentiment_results[a],
                             "Topics":topics_list[a]
                            })

        final_dict["Articles"] = articles

        articles_for_exp = []
        for a in range(len(summaries)):
            articles_for_exp.append({"Title":title[a],"Summary":summaries[a]})

        coverage_differences = CoverageDifference()
        coverages = coverage_differences.create_coverage_differences(articles_for_exp)
        coverage_list = []
        for i in range(len(coverages)): 
            coverage_list.append({'Comparison': coverages[i]['Comparison'].content,
             'Impact':coverages[i]['Impact'].content
            })
        final_dict["Comparitive Sentiment Score"] = {
            "Sentiment Distribution":sentiment_distribution,
            "Coverage Differences":coverage_list,
            "Topic Overlap":{
             "Common Topic":common_topics,
            }
        }

        for t in range(len(topics_list)):
            c=t
            final_dict["Comparitive Sentiment Score"]['Topic Overlap'][f'Unique Topic in Article {c+1}'] = topics_list[t]


        final_sentiment = FinalSentiment()
        verdict = final_sentiment.generate_final_sentiment(articles_for_exp)

        audio = GenerateAudio()
        audio.text_to_speech(verdict.content) 

        final_dict['Final Sentiment Analysis'] = verdict.content
        final_dict['Audio']=str(audio)

        with open("data.json", "w") as json_file:
            json.dump(final_dict, json_file, indent=4)
  
        st.write("Generated Insights Successfully!!")
  
  # with st.spinner("Getting the data for you..")
