from ..models import Person
from db_config import db
from apiflask import APIBlueprint

bp = APIBlueprint('person', __name__, url_prefix='person')


@bp.post('')
def create_account():
    pass


