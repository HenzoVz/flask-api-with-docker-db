from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:docker@localhost:5432/hotel_api"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class HotelModel(db.Model):
    __tablename__ = 'hoteis'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40))
    estrelas = db.Column(db.Float(precision=1))
    diaria = db.Column(db.Float(precision=2))
    cidade = db.Column(db.String(40))

    def __init__(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def __repr__(self):
        return f"<Hotel {self.nome}>"


@app.route('/hoteis', methods=['POST', 'GET'])
def handle_hoteis():
    if request.method == 'POST':
        if request.is_json:
            dados = request.get_json()
            novo_hotel = HotelModel(nome=dados['nome'], estrelas=dados['estrelas'], diaria=dados['diaria'], cidade=dados['cidade'])
            db.session.add(novo_hotel)
            db.session.commit()
            return {"message": f"{novo_hotel.nome} criado com sucesso."}, 201
        else:
            return {"error": "A requisição não está no formato JSON"}

    elif request.method == 'GET':
        hoteis = HotelModel.query.all()
        results = [
            {
                "nome": hotel.nome,
                "estrelas": hotel.estrelas,
                "diaria": hotel.diaria,
                "cidade": hotel.cidade
            } for hotel in hoteis]

        return {"count": len(results), "hoteis": results}, 200

@app.route('/cars/<hotel_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_hotel(hotel_id):
    hotel = HotelModel.query.get_or_404(hotel_id)

    if request.method == 'GET':
        response = {
            "nome": hotel.nome,
            "estrelas": hotel.estrelas,
            "diaria": hotel.diaria,
            "cidade": hotel.cidade
        }
        return {"message": "success", "hotel": response}

    elif request.method == 'PUT':
        dados = request.get_json()
        hotel.nome = dados['nome']
        hotel.estrelas = dados['estrelas']
        hotel.diaria = dados['diaria']
        hotel.cidade = dados['cidade']
        db.session.add(hotel)
        db.session.commit()
        return {"message": f"hotel {hotel.name} atualizado com sucesso."}, 200

    elif request.method == 'DELETE':
        db.session.delete(hotel)
        db.session.commit()
        return {"message": f"hotel {hotel.nome} deletado com sucesso."} , 200
