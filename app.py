import os
import json
import google.generativeai as genai
# Убедитесь, что send_from_directory добавлен в импорт
from flask import Flask, request, jsonify, render_template, send_from_directory 
from flask_cors import CORS

# ... (остальной код до маршрутов) ...
app = Flask(__name__)
# ...
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- Маршруты (Routes) ---

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# !!! НОВЫЙ БЛОК КОДА, КОТОРЫЙ ВСЕ ИСПРАВИТ !!!
# Этот маршрут будет ловить запросы типа /static/css/style.css
# и правильно отдавать файлы из папки static
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# API-эндпоинт для генерации имен
@app.route('/generate-names', methods=['POST'])
def generate_names_api():
    # ... (код этого блока не меняется) ...
    try:
        # ...
    except Exception as e:
        # ...

# Эта часть больше не нужна на сервере, но пусть остается, не мешает
if __name__ == '__main__':
    app.run(debug=True)
