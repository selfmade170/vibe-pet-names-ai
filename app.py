import os
import json
import google.generativeai as genai
# ВОТ ИСПРАВЛЕНИЕ: Мы вернули send_from_directory в импорт
from flask import Flask, request, jsonify, render_template, send_from_directory 
from flask_cors import CORS

# Создаем Flask-приложение
app = Flask(__name__)
CORS(app) 

# --- Настройка ---
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("Секретный ключ API_KEY не найден в переменных окружения.")

genai.configure(api_key=API_KEY)

# --- Настройка модели Gemini ---
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- Маршруты (Routes) ---

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для обслуживания статических файлов (CSS, JS)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
    
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
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Эта часть нужна для локального тестирования
if __name__ == '__main__':
    app.run(debug=True)
