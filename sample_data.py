from app import create_app
from app.mod_auth.models import Person
from db_config import db

create_app().app_context().push()

new_person = Person(name='Adam Smith', cpf='13245678909', birthdate='1996-04-26')
db.session.add(new_person)
db.session.commit()
