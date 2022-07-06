from apiflask import APIBlueprint, abort

from db_config import db
from ..models import Account
from ..schemas import NewAccountInSchema
from app import create_app

bp = APIBlueprint('account', __name__, url_prefix='account')
app = create_app()


@bp.post('/<int:person_id>')
@app.input(NewAccountInSchema)
def create_account(person_id: int, data):
    account = Account(person_id=person_id, **data)
    db.session.add(account)
    db.session.commit()
    return {'message': 'created', 'id': account.id}, 201


@bp.get('/<int:account_id>/balance')
def get_account_balance(account_id: int):
    account = Account.query.get(account_id)
    if not account:
        abort(404, 'Account not found.')
    return {'balance': float(account.balance)}


@bp.put('/<int:account_id>/deactivate')
def put_block_account(account_id: int):
    account = Account.query.get(account_id)
    if not account:
        abort(404, message='Account not found.')
    if account.active:
        abort(406, message='Account already inactive.')
    account.active = False

    return {'message': 'Account blocked'}
