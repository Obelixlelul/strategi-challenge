from flask_sqlalchemy import SQLAlchemy
from enum import Enum

import datetime

db = SQLAlchemy()

class Cliente(db.Model):

    id = db.Column('id', db.Integer, primary_key=True, autoincrement = True)
    nome = db.Column(db.String(150))
    cpf = db.Column(db.String(45))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(45))
    created_at = db.Column(db.DateTime)
    vendas = db.relationship('Venda', backref='cliente', lazy=True, cascade='all, delete')

    def __init__(self, nome: str, cpf: str, email: str, telefone: str):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.created_at = datetime.datetime.now()

    def to_dict(self, columns=[]):
       return {"id": self.id, "nome": self.nome, "cpf": self.cpf, "email": self.email, 'telefone': self.telefone, "created_at": self.created_at}
    
class Corretor(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45))
    senha = db.Column(db.String(45))
    vendas = db.relationship('Venda', backref='corretor', lazy=True, cascade='all, delete')

class TipoTypes(Enum):
    lote = 1
    apartamento = 2

class Tipo(db.Model):
    __tablename__ = 'tipo'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome = db.Column(db.String(50))
    imoveis = db.relationship('Imovel', backref='tipo', lazy = True)
    
class Condicao(db.Model):
    __tablename__ = 'condicao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    vendas = db.relationship('Venda', backref='condicao', lazy=True, cascade='all, delete')
  
class Imovel(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255))
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo.id'), nullable=False)
    cep = db.Column(db.String(10))
    logradouro = db.Column(db.String(50))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50))
    numero = db.Column(db.String(50))
    complemento = db.Column(db.String(150))
    valor = db.Column(db.Float)
    comissao = db.Column(db.Integer)

    vendas = db.relationship('Venda', backref='imovel', lazy=True, cascade='all, delete')

    def __init__(self, nome: str, tipo: int, cep: str, logradouro: str, 
                 bairro: str, cidade: str, numero: int, complemento: str, valor: float, comissao: int):
        self.nome = nome
        self.tipo_id = tipo
        self.cep = cep
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade 
        self.numero = numero
        self.complemento = complemento
        self.valor = valor
        self.comissao = comissao

class Venda(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_corretor = db.Column(db.Integer, db.ForeignKey('corretor.id'), nullable=False)
    id_imovel = db.Column(db.Integer, db.ForeignKey('imovel.id'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    id_condicao = db.Column(db.Integer, db.ForeignKey('condicao.id'), nullable=False)
    valor_comissao = db.Column(db.Float)

    def __init__(self, id_corretor, id_imovel, id_cliente, id_condicao, valor_comissao):
        self.id_corretor = id_corretor
        self.id_imovel = id_imovel
        self.id_cliente = id_cliente
        self.id_condicao = id_condicao
        self.valor_comissao = valor_comissao