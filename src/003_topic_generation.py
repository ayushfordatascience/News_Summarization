from keybert import KeyBERT

class TopicGeneration:
    def __init__(self,title,summaries):
        self.title = title
        self.summaries = summaries
    
    def generate_topics(self):
       topics_list = []
       try:
           kw_model = KeyBERT()
           
           for t in range(len(titles)):
                text = self.title[t]+" "+self.summaries[t]
                keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=3)
                topics = [keyword[0].capitalize() for keyword in keywords]
                topics_list.append(topics) 

           return topics_list    
       except Exception as e:
        raise ValueError(f"Could not create topic list {e}")  

    def generate_common_topics(self):
        topics_freq = {}
        try:
            topics_list = self.generate_topics()
            temp = topics_list
            temp = [t1 for t in temp for t1 in t]
            for topics in temp:
                if topics not in topics_freq:
                    topics_freq[topics] = 1
                else:
                    topics_freq[topics] += 1

            return [key for key, value in topics_freq.items() if value > 1]
        except Exception as e:
            raise ValueError("Couldn't load the common topics")
 