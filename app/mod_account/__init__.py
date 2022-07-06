from apiflask import APIBlueprint
from .models import Account, Transaction


def bp():
    _bp = APIBlueprint('account', __name__, url_prefix='/v1/')

    from .routes import account
    _bp.register_blueprint(account.bp)
    from .routes import transaction
    _bp.register_blueprint(transaction.bp)

    return _bp
