from flask import Flask, jsonify, request, render_template
from models import db, Processo
from services.consulta_service import consultar_andamentos
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///processos.db'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/processos', methods=['POST'])
def cadastrar_processo():
    data = request.get_json()
    numero = data.get('numero')
    tribunal = data.get('tribunal')
    andamentos = consultar_andamentos(numero, tribunal)

    processo = Processo(numero=numero, tribunal=tribunal, andamentos=str(andamentos))
    db.session.add(processo)
    db.session.commit()

    return jsonify({'mensagem': 'Processo cadastrado com sucesso!', 'andamentos': andamentos})

@app.route('/api/processos/<numero>', methods=['GET'])
def listar_processo(numero):
    processo = Processo.query.filter_by(numero=numero).first()
    if not processo:
        return jsonify({'erro': 'Processo não encontrado'}), 404
    return jsonify({'numero': processo.numero, 'andamentos': processo.andamentos})

@app.route('/api/consultar')
def consultar():
    numero = request.args.get('numero')
    tribunal = request.args.get('tribunal', 'TJSP')
    andamentos = consultar_andamentos(numero, tribunal)
    return jsonify({'numero': numero, 'andamentos': andamentos})

if __name__ == '__main__':
    app.run(debug=True)
