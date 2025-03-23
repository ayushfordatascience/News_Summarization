import requests

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

from langchain_huggingface import HuggingFaceEndpoint

def get_response(news_links):
  responses = []
  for n in news_links:
    try:
        res = requests.get(n,timeout=10)
        res.raise_for_status()
        responses.append(res.content)
        
    
    except requests.exceptions.HTTPError:
            responses.append("HTTP Error: No content found")
    except requests.exceptions.ConnectionError:
            responses.append("Connection Error: Unable to reach the server")
    except requests.exceptions.Timeout:
            responses.append("Timeout Error: The request took too long")
    except requests.exceptions.RequestException as e:
            responses.append(f"Request Exception: {str(e)}")
  return responses 

def build_model_from_transformers(model_name,category,save_model_as):
     try:
        model_id=model_name
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForSequenceClassification.from_pretrained(model_id)
        pipe = pipeline(category, model=model, tokenizer=tokenizer)
        pipe.save_pretrained(f'./model/{save_model_as}')
     except Exception as e:
          raise e
     return pipe    


def create_llm_model():
  try:
    llm = HuggingFaceEndpoint(llm_model)
    return llm
  except Exception as e:
        raise e     