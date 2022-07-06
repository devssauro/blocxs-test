from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship

from db_config import db


class Person(db.Model):
    __tablename__ = 'pessoa'

    def __int__(self, name, cpf, birthdate):
        self.name = name
        self.cpf = cpf
        self.birthdate = birthdate

    id = Column('idPessoa', Integer, primary_key=True, autoincrement=True)
    name = Column('nome', String(255), nullable=False)
    cpf = Column('cpf', String(11), unique=True, nullable=False)
    birthdate = Column('dataNascimento', Date, nullable=False)

    accounts = relationship('Account', back_populates='person')
