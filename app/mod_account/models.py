from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import DECIMAL
from datetime import datetime
from db_config import db


class Account(db.Model):
    __tablename__ = 'conta'

    def __int__(self, person_id, balance, withdraw_limit, active, type_account, date_creation = None):
        self.person_id = person_id
        self.balance = balance
        self.withdraw_limit = withdraw_limit
        self.active = active
        self.type_account = type_account
        if date_creation is None:
            self.date_creation = datetime.now()

    id = Column('idConta', Integer, primary_key=True, autoincrement=True)
    person_id = Column('idPessoa', Integer, ForeignKey('pessoa.idPessoa'))
    person = relationship('Person', back_populates='accounts')
    balance = Column('saldo', DECIMAL(15, 2), default=0.0)
    daily_withdraw_limit = Column('limiteSaqueDiario', DECIMAL(15, 2), default=1000.0)
    active = Column('flagAtivo', Boolean, default=True)
    type_account = Column('tipoConta', Integer, default=1)
    date_creation = Column('dataCriacao', DateTime, default=func.now())

    transactions = relationship('Transaction', back_populates='account')


class Transaction(db.Model):
    __tablename__ = 'transacao'

    def __int__(self, account_id, value=0.0, date_transaction=None):
        self.account_id = account_id
        self.value = value

    id = Column('idTransacao', Integer, primary_key=True, autoincrement=True)
    account_id = Column('idConta', Integer, ForeignKey('conta.idConta'))
    account = relationship('Account', back_populates='transactions')
    value = Column('value', DECIMAL(15, 2))
    date_transaction = Column('dataTransacao', DateTime, default=func.now())
