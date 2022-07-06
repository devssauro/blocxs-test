from apiflask import APIBlueprint
from .models import Person


def bp():
    _bp = APIBlueprint('person', __name__, url_prefix='/v1/')

    from .routes import person
    _bp.register_blueprint(person.bp)

    return _bp
