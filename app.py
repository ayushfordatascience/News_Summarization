from src.web_scraper import WebScraper
from src.sentiment import Sentiment
from src.topic_generation import TopicGeneration
from src.coverage_differences import CoverageDifference
from src.final_sentiment import FinalSentiment

ws = WebScraper('Tesla')
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
    articles.append({"Title":title[a],"Summary":summaries[a]})

coverage_differences = CoverageDifference()
coverages = coverage_differences.create_coverage_differences(articles)    

final_sentiment = FinalSentiment()
verdict = final_sentiment.generate_final_sentiment(articles)
print(verdict)