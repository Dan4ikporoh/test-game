from flask import Flask, jsonify, request
from flask_cors import CORS
import json

# --- Инициализация ---
app = Flask(__name__)
# CORS необходим для связи между вашим веб-приложением и сервером
CORS(app) 

# --- База Данных (в виде простого JSON файла для примера) ---
# В реальном проекте здесь будет полноценная база данных (PostgreSQL, MongoDB и т.д.)
DB_FILE = 'game_database.json'

def load_db():
    """Загружает базу данных из файла."""
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файла нет, создаем структуру по умолчанию
        return {"players": {}}

def save_db(data):
    """Сохраняет данные в файл."""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- Игровые маршруты (API) ---

@app.route('/get_player_data/<user_id>', methods=['GET'])
def get_player_data(user_id):
    """Возвращает данные игрока или создает нового."""
    db = load_db()
    if user_id in db['players']:
        return jsonify(db['players'][user_id])
    else:
        # Создание нового игрока
        db['players'][user_id] = {
            "level": 1,
            "xp": 0,
            "coins": 10,
            "damage": 1,
            "armor": 0,
            "mercenaries": 0,
            "current_monster_hp": 100 
            # TODO: Добавить логику для разных монстров
        }
        save_db(db)
        return jsonify(db['players'][user_id])

@app.route('/attack', methods=['POST'])
def attack():
    """Обрабатывает атаку игрока на монстра."""
    data = request.json
    user_id = str(data.get('user_id'))
    db = load_db()
    
    player = db['players'].get(user_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    # Уменьшаем здоровье монстра
    player['current_monster_hp'] -= player['damage']
    
    # Если монстр побежден
    if player['current_monster_hp'] <= 0:
        player['xp'] += 50  # Награда: опыт
        player['coins'] += 10 # Награда: монеты
        # TODO: Логика повышения уровня
        # TODO: Логика появления нового, более сильного монстра
        player['current_monster_hp'] = 200 # Здоровье нового монстра
        
    save_db(db)
    return jsonify(player)

# TODO: Добавить маршруты для магазина, улучшений, пассивного дохода и боссов

if __name__ == '__main__':
    # Для разработки. В продакшене используется Gunicorn или другой WSGI-сервер.
    app.run(host='0.0.0.0', port=5000, debug=True)
