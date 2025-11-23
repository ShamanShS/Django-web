
import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

print("--- Тест доступа к Gemini API ---")

try:

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Не удалось найти GEMINI_API_KEY в файле .env. Проверьте имя переменной и сам файл.")
    
    print("API-ключ успешно загружен.")


    genai.configure(api_key=api_key)
    print("Библиотека сконфигурирована.")


    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    print(f"Модель '{model.model_name}' успешно создана.")


    prompt = "Скажи 'Привет, мир!' на языке роботов"
    print(f"Отправка тестового промпта: '{prompt}'")
    
    response = model.generate_content(prompt)


    print("\n✅ УСПЕХ! Ответ от API получен.")
    print("---------------------------------")
    print(response.text)
    print("---------------------------------")

except Exception as e:
    print(f"\n❌ ОШИБКА! Не удалось получить доступ к API.")
    print(f"Причина: {e}")