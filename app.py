from src.web_scraper import WebScraper
from src.sentiment import Sentiment
from src.topic_generation import TopicGeneration
from src.coverage_differences import CoverageDifference

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

coverage_differences = CoverageDifference()
comparison_prompt = coverage_differences.create_comparison_prompt()
impact_prompt = coverage_differences.create_impact_prompt()
comparison_chain = coverage_differences.create_chains(comparison_prompt)
impact_chain = coverage_differences.create_chains(impact_prompt)

articles = []
for a in range(len(summaries)):
    articles.append({"Title":title[a],"Summary":summaries[a]})

coverages = coverage_differences.create_coverage_differences(articles,comparison_chain,impact_chain)    
print(coverages)