# News Summarization in Python

A streamlit application which help users get insight on the latest trend of a given company by lokking at news articles.

## Folder Structure

```
📦 News_Summarization
├─ .gitignore
├─ README.md  # Github Repo information
├─ api.py   # Codes for creating a server
├─ app.py   # Code for invoking functions and generating a streamlit application
├─ constants.py  # For storing constant values
├─ notebooks    # Storing the jupyter/colab notebooks 
│  └─ News_Summarization_and_Text_to_Speech_Application.ipynb # Contains rough implementation of this project
├─ output.mp3 
├─ requirements.txt  # Consists of the names of all libraries
├─ src
│  ├─ coverage_differences.py  #Consists of codes for coverage difference
│  ├─ final_sentiment.py # Consists of codes for overall sentiment of a company
│  ├─ generate_audio.py  # Consists of codes for generating the audio file
│  ├─ sentiment.py  # Consists of codes for generating the sentiment of each news article
│  ├─ topic_generation.py # Consists of codes for generating the topic for each article
│  └─ web_scraper.py  # Consists of codes for extracting information from web
└─ utils.py
```


## For app deployment we have used Streamlit and for backend deployment we have used Render.

