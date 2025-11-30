# core/gemini_utils.py
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

# Настройки для генерации
generation_config = {
  "temperature": 1,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}


model = genai.GenerativeModel(model_name="gemini-2.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def generate_content(prompt_text):

    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        print(f"Ошибка при обращении к API Gemini: {e}")
        return "Извините, галактический сервер временно перегружен. Попробуйте позже."