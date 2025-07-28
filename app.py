# ----- Файл app.py для постоянного хостинга -----

import os
import json
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Создаем Flask-приложение
app = Flask(__name__)
CORS(app) 

# --- Настройка ---
# Ключ будет взят из "секретов" на хостинге, а не из кода
API_KEY = os.environ.get('API_KEY')

# Проверяем, что ключ доступен
if not API_KEY:
    # Эта ошибка будет видна только в логах сервера, а не пользователю
    raise ValueError("Секретный ключ API_KEY не найден в переменных окружения.")

genai.configure(api_key=API_KEY)

# --- Настройка модели Gemini ---
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- Маршруты (Routes) ---

# Главная страница, которая отдает наш index.html
@app.route('/')
def index():
    return render_template('index.html')

# API-эндпоинт для генерации имен
@app.route('/generate-names', methods=['POST'])
def generate_names_api():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'Промпт не был предоставлен'}), 400
        
        response = model.generate_content(prompt)
        cleaned_text = response.text.strip().replace('```json', '').replace('```', '').strip()
        names_array = json.loads(cleaned_text)
        
        return jsonify({'names': names_array})
    except Exception as e:
        print(f"Error: {e}") # Для отладки на сервере
        return jsonify({'error': str(e)}), 500

# Эта часть нужна для запуска сервера, если вы тестируете его локально
if __name__ == '__main__':
    app.run(debug=True)