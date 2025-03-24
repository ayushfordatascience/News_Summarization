from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
from constants import translation_model

class GenerateAudio:
    def __init__(self):
        self.model_name = translation_model

    def translate_to_hindi(self, text):
        try:
            tokenizer = MarianTokenizer.from_pretrained(self.model_name)
            model = MarianMTModel.from_pretrained(self.model_name)
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=256)
            output_tokens = model.generate(**inputs)
            translated_text = tokenizer.batch_decode(output_tokens, skip_special_tokens=True)
            return translated_text[0]
        except Exception as e:
            raise e

    def text_to_speech(self, text=None, filename="output.mp3"):
        try:
            hindi_text = self.translate_to_hindi(text)
            tts = gTTS(text=hindi_text, lang="hi", slow=False)
            tts.save(filename)
            return filename
        except Exception as e:
            raise e