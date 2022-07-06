from datetime import datetime

from apiflask import APIBlueprint, abort, pagination_builder
from sqlalchemy import func

from db_config import db
from .. import Transaction, Account
from ..schemas import TransactionHistoryInSchema, TransactionsOutSchema, TrasactionOperationInSchema
from app import create_app

bp = APIBlueprint('transaction', __name__, url_prefix='transactions')
app = create_app()


@bp.get('')
@app.input(TransactionHistoryInSchema, location='querystring')
@app.output(TransactionsOutSchema)
def get_transaction_history(query):
    transaction_args = []
    balance_args = []
    account = Account.query.get(query['account_id'])
    if not account:
        abort(404, 'Account not found.')
    if query.get('start_date'):
        transaction_args.append(Transaction.start_date >= query['start_date'])
    if query.get('end_date'):
        transaction_args.append(Transaction.start_date >= query['end_date'])
    transactions = Transaction.query.filter(
        *transaction_args, Transaction.account_id == query['account_id']
    ).order_by(Transaction.date_transaction.desc()).paginate(page=query.get('page', 1), per_page=query.get('per_page', 10))

    balance = Transaction.query.with_entities(
        func.sum(Transaction.value).label('balance')
    ).filter(*balance_args, Transaction.account_id == query['account_id']).first().balance

    return {
        'transactions': transactions.items,
        'balance': balance if balance is not None else 0.0,
        'pagination': pagination_builder(transactions),
    }


@bp.post('/deposit')
@app.input(TrasactionOperationInSchema)
def post_deposit_transaction(data):
    account = Account.query.get(data['account_id'])
    if not account:
        abort(404, message='Account not found.')
    if data['value'] < 0:
        abort(406, message='Deposit value not acceptable.')

    new_transaction = Transaction(**data, account_id=data['account_id'])
    db.session.add(new_transaction)
    db.session.commit()
    new_balance = Transaction.query.with_entities(
        func.sum(Transaction.value).label('balance')
    ).filter(Transaction.account_id == new_transaction.account_id).first().balance
    account.balance = new_balance
    db.session.commit()

    return {
        'trasaction_id': new_transaction.id
    }, 201


@bp.post('/withdraw')
@app.input(TrasactionOperationInSchema)
def post_withdraw_transaction(data):
    account = Account.query.get(data['account_id'])
    today = datetime.now().isoformat()[0:10]
    if not account:
        abort(404, message='Account not found.')
    if data['value'] < 0:
        abort(406, message='Withdraw value not acceptable.')

    daily_total_withdraw = Transaction.query.with_entities(
        func.sum(Transaction.value).label('total')
    ).filter(
        Transaction.account_id == data['account_id'],
        Transaction.value < 0.0,
        Transaction.date_transaction.between(f'{today} 00:00:00', f'{today} 23:59:59')
    ).first().total
    daily_remaing_withdraw = account.daily_withdraw_limit \
        if daily_total_withdraw is None else account.daily_withdraw_limit + daily_total_withdraw

    if data['value'] > daily_remaing_withdraw:
        abort(406, message='Not enough withdraw limit.')
    if data['value'] > account.balance:
        abort(406, message='Not enough balance.')

    new_transaction = Transaction(value=-data['value'], account_id=data['account_id'])
    db.session.add(new_transaction)
    db.session.add(new_transaction)
    db.session.commit()
    new_balance = Transaction.query.with_entities(
        func.sum(Transaction.value).label('balance')
    ).filter(Transaction.account_id == new_transaction.account_id).first().balance
    account.balance = new_balance
    db.session.commit()

    return {
        'trasaction_id': new_transaction.id
    }, 201
