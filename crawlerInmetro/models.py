from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

import settings
import datetime

DeclarativeBase = declarative_base()

def db_connect():
    print("ON MODELS - db_connect")
    print(settings.CONNECTION_STRING)      
    return create_engine(URL(**settings.CONNECTION_STRING), encoding='utf-8')    

class Workshops(DeclarativeBase):
    __tablename__ = "oficinas_gnv"

    id = Column(Integer, primary_key=True)
    num_reg = Column('numero_registro', String, nullable=True)
    nome = Column('nome', String, nullable=True)    
    site = Column('site', String, nullable=True)
    reg_inicio = Column('registro_inicio', DateTime)
    reg_fim = Column('registro_fim', DateTime)
    email = Column('email', String, nullable=True)
    endereco = Column('endereco', String, nullable=True)
    uf = Column('uf', String)
    cidade = Column('cidade', String)
    bairro = Column('bairro', String, nullable=True)
    cep = Column('cep', String)
    tel = Column('tel', String, nullable=True)
    fax = Column('fax', String, nullable=True)
    resp_oper = Column('responsavel', String)
    google_id = Column('google_id', String, nullable=True)
    lat = Column('lat', Float, nullable=True)
    lng = Column('lng', Float, nullable=True)
    link_google = Column('link_google', String, nullable=True)
    rating = Column('rating', Float, nullable=True)

    def __eq__(self, other):
        return self.num_reg == other.num_reg