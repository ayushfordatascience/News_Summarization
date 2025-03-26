from src.web_scraper import WebScraper
from src.sentiment import Sentiment
from src.topic_generation import TopicGeneration
from src.coverage_differences import CoverageDifference
from src.final_sentiment import FinalSentiment
from src.generate_audio import GenerateAudio

from constants import endpoint
import json

import requests
import streamlit as st

st.title('Business News Summarization App')

with st.form(key="input_form"):
    api_key = st.text_input("Enter your OpenAI API Key:", key="user_input",type="password")
    submit_button = st.form_submit_button(label="Submit")


if submit_button and not api_key:
    st.warning("Please enter your OpenAI API key to proceed.")
else:
    st.session_state['api_key']=api_key
    headers = {"Authorization": f"Bearer {st.session_state['api_key']}"}
    
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

            coverage_differences = CoverageDifference(api_key)
            coverages = coverage_differences.create_coverage_differences(articles_for_exp)
            coverage_list = []
            for i in range(len(coverages)): 
                coverage_list.append({'Comparison': coverages[i]['Comparison'].content,
                'Impact':coverages[i]['Impact'].content
                })
            final_dict["Comparative_Sentiment_Score"] = {
                "Sentiment_Distribution":sentiment_distribution,
                "Coverage_Differences":coverage_list,
                "Topic_Overlap":{
                "Common_Topics":common_topics,
                 }
            }

            for t in range(len(topics_list)):
                c=t
                final_dict["Comparative_Sentiment_Score"]['Topic_Overlap'][f'Unique_Topics_in_Article {c+1}'] = topics_list[t]


            final_sentiment = FinalSentiment(api_key)
            verdict = final_sentiment.generate_final_sentiment(articles_for_exp)

            audio = GenerateAudio()
            audio.text_to_speech(verdict.content) 

            final_dict['Final_Sentiment_Analysis'] = verdict.content
            final_dict['Audio']=str(audio)
         
            response = requests.post(
                    f"{endpoint}/receive_data",  
                    json=final_dict  
            )

            if response.status_code == 200:
                    st.success("Data sent successfully!")  
            else:
                    st.error(f"Error: {response.status_code} - {response.text}") 
  
        st.write("Generated Insights Successfully!!")
        

        with st.spinner("Getting the data for you.."):
                response = requests.get(
                f"{endpoint}/data")
                if response.status_code == 200:
                    st.session_state['news_data'] = json.loads(response.json()["stored_data"][0])
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
                    st.session_state['news_data'] = []

                data = st.session_state['news_data']


                sentiment_distribution = data['Comparative_Sentiment_Score']['Sentiment_Distribution']
                positive_count = sentiment_distribution.get("positive", 0)
                neutral_count = sentiment_distribution.get("neutral", 0)
                negative_count = sentiment_distribution.get("negative", 0)

                st.markdown(f"**Sentiment Distribution:** Positive: {positive_count} | Neutral: {neutral_count} | Negative: {negative_count}")
                st.markdown("""
                <style>
                    .scroll-container {
                    max-height: 40px;
                    overflow-y: auto;
                    border: 1px solid #ccc;
                    padding-right: 10px;
                    border-radius: 10px;
                    }
                    .article-box {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        background-color: #f9f9f9;
                        padding: 15px;
                        margin-bottom: 10px;
                        border-radius: 10px;
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                    }
                    .article-content {
                        flex: 1;
                        color: #000;     
                    }
                    .sentiment-circle {
                        width: 15px;
                        height: 15px;
                        border-radius: 50%;
                        margin-left: 10px;
                    }
                </style>""",unsafe_allow_html=True)      
                sentiment_colors = {
                    "Positive": "#28a745",
                    "Neutral": "#ffbf00",
                    "Negative": "#dc3545"
                }
                st.markdown(f"#### Articles from {company}")
                st.markdown("""<div class="scroll-container">""", unsafe_allow_html=True)
                article = data["Articles"]
                for i in range(len(article)):
                    sentiment_color = sentiment_colors.get(article[i]["Sentiment"], "gray")
                    st.markdown(f"""
                        <div class="article-box">
                            <div class="article-content">
                                <h4><b>{article[i]["Title"]}</b></h4>
                                <p>{article[i]["Summary"]}</p>
                                <p><i>Topics: {", ".join(article[i]["Topics"])}</i></p>
                            </div>
                        <div class="sentiment-circle" style="background-color: {sentiment_color};"></div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("#### Coverage Differences")
                st.markdown("""
                    <style>
                    .scroll-container {
                        max-height: 40px;
                        overflow-y: auto;
                        border: 1px solid #ccc;
                        padding-right: 10px;
                        border-radius: 10px;
                    }
                    .coverage-box {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        background-color: #f9f9f9;
                        padding: 15px;
                        margin-bottom: 10px;
                        border-radius: 10px;
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                    }
                    .coverage-content {
                        flex: 1;
                        color: #000;     
                    }
                    </style>      
                <div class="scroll-container">""", unsafe_allow_html=True)
                coverage = data["Comparative_Sentiment_Score"]["Coverage_Differences"][:6]
                for i in range(len(coverage)):
                    st.markdown(f"""
                        <div class="coverage-box">
                            <div class="coverage-content">
                                <h4><b>Comparison</b></h4>
                                <p>{coverage[i]["Comparison"]}</p>
                                <h4><b>Impact</b></h4>
                                <p>{coverage[i]["Impact"]}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("#### Verdict")
                st.markdown("""
                    <style>
                        .verdict-box {
                        background-color: #f0f0f0;
                        padding: 15px;
                        color:#000;
                        border-radius: 10px;
                        margin-top: 10px;
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                        }
                    </style>
                """, unsafe_allow_html=True)


                final_sentiment = data['Final_Sentiment_Analysis']
                st.markdown(f'<div class="verdict-box"><p>{final_sentiment}</p></div>', unsafe_allow_html=True)


                audio_url = "output.mp3"  # Replace with actual audio URL
            
                st.markdown("#### Play it in Hindi")
                st.audio(audio_url, format="audio/mp3")
        
        
    if st.button("Clear API Key"):
        if "api_key" in st.session_state:
            del st.session_state["api_key"]

st.html("""
<div class="footer">
      <div>
            <p> Created by Ayush Bhattacharya</p>
      </div>            
</div>
""")           
