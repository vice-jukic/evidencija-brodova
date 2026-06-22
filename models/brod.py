from pony import orm
from datetime import datetime

db = orm.Database()

class Brod(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    naziv = orm.Required(str)
    registracija = orm.Required(str)
    tip = orm.Required(str)
    duljina = orm.Required(float)
    godina = orm.Required(int)
    ima_jedra = orm.Required(bool)
    ima_tende = orm.Required(bool)
    oprema = orm.Required(str)
    zadnji_servis = orm.Optional(datetime)
    opis = orm.Optional(str)