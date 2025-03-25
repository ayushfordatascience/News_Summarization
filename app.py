from src.web_scraper import WebScraper
from src.sentiment import Sentiment
from src.topic_generation import TopicGeneration
from src.coverage_differences import CoverageDifference
from src.final_sentiment import FinalSentiment
from src.generate_audio import GenerateAudio

from constants import endpoint

import json
import streamlit as st

st.title('Business News Summarization App')

api_key = st.text_input("Enter your OpenAI API Key:", type="password")

if not api_key:
    st.warning("Please enter your OpenAI API key to proceed.")
else:
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
  
    with st.spinner("Getting the data for you.."):
        data = get_response(list[endpoint])[0]

        st.markdown(f"## {data['Company']}")


        positive_count = sentiment_distribution.get("Positive", 0)
        neutral_count = sentiment_distribution.get("Neutral", 0)
        negative_count = sentiment_distribution.get("Negative", 0)

        st.markdown(f"**Sentiment Distribution:** Positive: {positive_count} | Neutral: {neutral_count} | Negative: {negative_count}")

        sentiment_colors = {
            "Positive": "green",
            "Neutral": "amber",
            "Negative": "red"
        }

        st.markdown(f"#### Articles from {data['Company']}")
        st.markdown("""
            <style>
            .scroll-container {
             max-height: 400px;
             overflow-y: auto;
             border: 1px solid #ccc;
             padding: 10px;
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
            }
            .sentiment-circle {
                width: 15px;
                height: 15px;
                border-radius: 50%;
                margin-left: 10px;
            }
            </style>      
                <article class="scroll-container">""", unsafe_allow_html=True)
        for article in data["Articles"]:
            sentiment_color = sentiment_colors.get(article["Sentiment"], "gray")
            st.markdown(f"""
                <div class="article-box">
                    <div class="article-content">
                        <h5><b>{article["Title"]}</b></h5>
                        <p>{article["Summary"]}</p>
                        <p><i>Topics: {", ".join(article["Topics"])}</i></p>
                    </div>
                <div class="sentiment-circle" style="background-color: {sentiment_color};"></div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</article>", unsafe_allow_html=True)

            st.markdown("## Coverage Differences")

st.markdown("""
    <div class="scroll-container">
""", unsafe_allow_html=True)

st.markdown("#### Coverage Differences")
st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
for coverage in data["Comparative Sentiment Score"]["Coverage Differences"]:
    st.markdown(f"""
        <div class="coverage-box">
            <div class="coverage-content">
                <h5><b>Comparison</b></h5>
                <p>{coverage["Comparison"]}</p>
                <h5><b>Impact</b></h5>
                <p>{coverage["Impact"]}</p>
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
            border-radius: 10px;
            margin-top: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Final Sentiment Analysis
final_sentiment = data['Final Sentiment Analysis']
st.markdown(f'<div class="verdict-box"><p>{final_sentiment}</p></div>', unsafe_allow_html=True)

# Audio Player
audio_url = "output.mp3"  # Replace with actual audio URL

st.audio(audio_url, format="audio/mp3")
st.markdown("#### Play it in Hindi")
