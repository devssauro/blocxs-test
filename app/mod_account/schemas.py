from apiflask import Schema, PaginationSchema
from apiflask.fields import Integer, Boolean, DateTime, Float, List, Nested, String


class NewAccountInSchema(Schema):
    type_account = Integer(required=True)


class NewAccountOutSchema(Schema):
    id = Integer()
    type_account = Integer()
    withdraw_limit = Integer()
    active = Boolean()
    date_created = DateTime()
    balance = Integer()


class TransactionHistoryInSchema(Schema):
    start_date = DateTime(required=False)
    end_date = DateTime(required=False)
    page = Integer(required=False, default=1)
    per_page = Integer(required=False, default=10)
    account_id = Integer(required=True)


class TransactionOutSchema(Schema):
    id = Integer()
    account_id = Integer()
    value = Float()
    date_transaction = String(data_key='date')


class TransactionsOutSchema(Schema):
    transactions = List(Nested(TransactionOutSchema))
    pagination = Nested(PaginationSchema)
    balance = Float()


class TrasactionOperationInSchema(Schema):
    value = Float(required=True)
    account_id = Integer(required=True)


class TransactionDepositOutSchema(Schema):
    transaction_id = Integer()
