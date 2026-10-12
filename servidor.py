from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# Conectar ao MongoDB
MONGODB_URI = os.environ.get("MONGODB_URI")

try:
    client = MongoClient(MONGODB_URI)
    client.admin.command("ping")
    print("✅ Conectado ao MongoDB com sucesso!")
except Exception as e:
    print(f"❌ Erro ao conectar ao MongoDB: {e}")

db = client.aquavibe
colecao = db.dados

# Carregar dados salvos ou usar padrão
def carregar_dados():
    try:
        dados_salvos = colecao.find_one({"_id": "principal"})
        if dados_salvos:
            del dados_salvos["_id"]
            return dados_salvos
    except Exception as e:
        print(f"⚠️ Erro ao carregar dados: {e}")
    
    return {
        "nome": "AquaVibe",
        "volume": 0,
        "meus_peixes": [],
        "desejos": [],
        "plantas": [],
        "historico": [],
        "tarefas": [],
        "gastos": [],
        "fotos": [],
        "config": {
            "modo_escuro": False,
            "horas_luz": 8,
            "temperatura_ideal": [24, 28],
            "ph_ideal": [6.0, 7.5]
        }
    }

dados = carregar_dados()

banco_peixes = [
    {
        "id": 1,
        "nome": "Tetra Neon",
        "cientifico": "Paracheirodon innesi",
        "tamanho": 4,
        "ph": [5.5, 7.0],
        "temperatura": [20, 28],
        "dificuldade": "Fácil",
        "tamanho_grupo": 6
    },
    {
        "id": 2,
        "nome": "Coridora",
        "cientifico": "Corydoras sp.",
        "tamanho": 6,
        "ph": [6.0, 7.5],
        "temperatura": [22, 28],
        "dificuldade": "Fácil",
        "tamanho_grupo": 4
    },
    {
        "id": 3,
        "nome": "Betta",
        "cientifico": "Betta splendens",
        "tamanho": 6,
        "ph": [6.0, 7.5],
        "temperatura": [24, 30],
        "dificuldade": "Média",
        "tamanho_grupo": 1
    }
]

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/dados', methods=['GET', 'POST'])
def api_dados():
    global dados
    if request.method == 'POST':
        novos_dados = request.json
        dados.update(novos_dados)
        try:
            colecao.replace_one({"_id": "principal"}, dados, upsert=True)
            print("💾 Dados salvos no MongoDB!")
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
    return jsonify(dados)

@app.route('/api/peixes', methods=['GET'])
def api_peixes():
    return jsonify(banco_peixes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
