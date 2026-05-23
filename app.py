from flask import Flask, render_template, request, redirect, url_for
from pony import orm
from datetime import datetime

db = orm.Database()

app = Flask(__name__)

class Brod(db.Entity):
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

db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

def formatiraj_datum(datum):
    if datum:
        return datum.strfitime("%d-%m-%Y")
    return ""

@app.route("/dodaj-brod", methods=["GET", "POST"])
@orm.db_session
def dodaj_brod():
    if request.method == "POST":
        Brod(
            naziv = request.form["naziv"],
            tip = request.form["tip"],
            duljina = float(request.form["duljina"]),
            godina = int(request.form["godina"]),
            ima_jedra = "ima_jedra" in request.form,
            ima_tende = "ima_tende" in request.form,
            oprema = request.form["oprema"],
            opis = request.form["opis"],
            zadnji_servis = None
        )

        return redirect(url_for("home"))
    return render_template("dodaj_brod.html")

@app.route("/")
def home():
    return "Evidencija brodova radi!"

if __name__ == "__main__":
    app.run(port=5000)