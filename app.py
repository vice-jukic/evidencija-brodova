from flask import Flask, render_template, request, jsonify, redirect, url_for
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
    oprema = orm.Required(str)
    zadnji_servis = orm.Optional(datetime)
    opis = orm.Optional(str)

# Povezivanje aplikacije sa SQLite bazom
db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
# Kreiranje tablica iz modela ako još ne postoje
db.generate_mapping(create_tables=True)

# Pretvaranje datetime objekta u čitljiv datum
def formatiraj_datum(datum):
    if datum:
        return datum.strftime("%d-%m-%Y")
    return ""

# Dodavanje broda u bazu
@app.route("/dodaj-brod", methods=["GET", "POST"])
@orm.db_session # omogućuje komunikaciju s bazom
def dodaj_brod():
    # GET = prikaz forme, POST = dodavanje broda u bazu
    if request.method == "GET":
        return render_template("dodaj_brod.html")
    
    if request.method == "POST":
        try:

            zadnji_servis = None
            datum_servisa = request.form.get("zadnji_servis")

            if datum_servisa:
                zadnji_servis = datetime.strptime(datum_servisa, "%Y-%m-%d")
            
            Brod(
                naziv = request.form["naziv"],
                tip = request.form["tip"],
                duljina = float(request.form["duljina"]),
                godina = int(request.form["godina"]),
                ima_jedra = "ima_jedra" in request.form,
                ima_tende = "ima_tende" in request.form,
                oprema = request.form["oprema"],
                opis = request.form["opis"],
                zadnji_servis = zadnji_servis
            )

            # spremanje promjena u bazu
            orm.commit()

            return redirect(url_for("pregled_brodova"))
    
        except Exception as e:
            return jsonify({
                "response": "Error",
                "message": str(e)
            }), 400

# Dohvaćanje svih brodova iz baze
@app.route("/brodovi", methods=["GET"])
@orm.db_session
def pregled_brodova():
    brodovi = Brod.select()
    return render_template("brodovi.html", brodovi=brodovi)

# Dohvaćanje jednog broda po ID-u
@app.route("/brod/<int:brod_id>", methods=["GET"])
@orm.db_session
def detalji_broda(brod_id):
    brod = Brod.get(id=brod_id)
    if not brod: # ako brod ne postoji
        return jsonify({
            "response": "Error",
            "message": f"Brod s ID-em {brod_id} ne postoji!"
        }), 404
    
    # vraćanje podataka o brodu
    return render_template("detalji_broda.html", brod=brod)

# Uređivanje postojećeg broda
@app.route("/uredi-brod/<int:brod_id>", methods=["GET", "POST"])
@orm.db_session
def uredi_brod(brod_id):
    brod = Brod.get(id=brod_id)

    # ako brod ne postoji
    if not brod:
        return jsonify({
            "response": "Error",
            "message": f"Brod s ID-em {brod_id} ne postoji!"
        }), 404
    
    if request.method == "GET":
        return render_template("uredi_brod.html", brod=brod)
    
    try:
        zadnji_servis = None
        datum_servisa = request.form.get("zadnji_servis")

        if datum_servisa:
            zadnji_servis = datetime.strptime(datum_servisa, "%Y-%m-%d")

        # ažuriranje podataka    
        brod.naziv = request.form["naziv"]
        brod.tip = request.form["tip"]
        brod.duljina = float(request.form["duljina"])
        brod.godina = int(request.form["godina"])
        brod.ima_jedra = "ima_jedra" in request.form
        brod.ima_tende = "ima_tende" in request.form
        brod.oprema = request.form["oprema"]
        brod.opis = request.form["opis"]
        brod.zadnji_servis = zadnji_servis

        orm.commit()

        return redirect(url_for("detalji_broda", brod_id=brod.id))
    
    except Exception as e:
        return jsonify({
            "response": "Error",
            "message": str(e)
        }), 400

# Brisanje broda po ID-u
@app.route("/obrisi-brod/<int:brod_id>", methods=["POST"])
@orm.db_session
def obrisi_brod(brod_id):
    brod = Brod.get(id=brod_id)
    if not brod:
        return jsonify({
            "response": "Error",
            "message": f"Brod s ID-em {brod_id} ne postoji!"
        }), 404
    
    # brisanje broda iz baze i spremanje promjena
    brod.delete()
    orm.commit()

    return redirect(url_for("pregled_brodova"))


@app.route("/")
def pocetna():
    return render_template("pocetna.html")

if __name__ == "__main__":
    app.run(port=5000)