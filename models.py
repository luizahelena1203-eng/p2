from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Processo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    tribunal = db.Column(db.String(50))
    andamentos = db.Column(db.Text)
