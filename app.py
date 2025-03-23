from src.web_scraper import WebScraper
from src.sentiment import Sentiment
from src.topic_generation import TopicGeneration

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

print(common_topics)