from flask import Flask
from pony import orm
from datetime import datetime

DB = orm.Database()

app = Flask(__name__)

class Brod(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    naziv = orm.Required(str)
    tip = orm.Required(str)
    duljina = orm.Required(float)
    godina = orm.Required(int)
    ima_jedra = orm.Required(bool)
    ima_tende = orm.Required(bool)
    operma = orm.Required(str)
    zadnji_servis = orm.Optional(datetime)
    opis = orm.Optional(str)

DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)

@app.route("/")
def home():
    return "Evidencija brodova radi!"

if __name__ == "__main__":
    app.run(port=8080)