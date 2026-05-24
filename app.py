from flask import Flask, render_template, request, jsonify
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
            
            novi_brod = Brod(
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

            orm.commit() # spremanje promjena u bazu

            return jsonify({
                "response": "Success",
                "message": "Brod uspješno dodan",
                "brod": {
                    "id": novi_brod.id,
                    "naziv": novi_brod.naziv,
                    "tip": novi_brod.tip,
                    "zadnji_servis": formatiraj_datum(novi_brod.zadnji_servis)
                }
            }), 201
    
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
    rezultat = []

    for brod in brodovi:
        rezultat.append({
            "id": brod.id,
            "naziv": brod.naziv,
            "tip": brod.tip,
            "duljina": brod.duljina,
            "godina": brod.godina,
            "ima_jedra": brod.ima_jedra,
            "ima_tende": brod.ima_tende,
            "oprema": brod.oprema,
            "zadnji_servis": formatiraj_datum(brod.zadnji_servis),
            "opis": brod.opis
        })
    
    return jsonify(rezultat), 200

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
    return jsonify({
        "id": brod.id,
        "naziv": brod.naziv,
        "tip": brod.tip,
        "duljina": brod.duljina,
        "godina": brod.godina,
        "ima_jedra": brod.ima_jedra,
        "ima_tende": brod.ima_tende,
        "oprema": brod.oprema,
        "zadnji_servis": formatiraj_datum(brod.zadnji_servis),
        "opis": brod.opis
    }), 200

# Uređivanje postojećeg broda
@app.route("/uredi-brod/<int:brod_id>", methods=["PUT"])
@orm.db_session
def uredi_brod(brod_id):
    brod = Brod.get(id=brod_id)

    if not brod:
        return jsonify({
            "response": "Error",
            "message": f"Brod s ID-em {brod_id} ne postoji!"
        }), 404
    
    try:
        zadnji_servis = None
        datum_servisa = request.form.get("zadnji_servis")

        if datum_servisa:
            zadnji_servis = datetime.strptime(datum_servisa, "%Y-%m-%d")

        # ažuriranje podataka    
        brod.naziv = request.form["naziv"]
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

        return jsonify({
            "response": "Success",
            "message": "Brod uspješno ažuriran!",
            "brod": {
                "id": brod.id,
                "naziv": brod.naziv,
                "tip": brod.tip
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "repsonse": "Error",
            "message": str(e)
        }), 400

# Brisanje broda po ID-u
@app.route("/obrisi-brod/<int:brod_id>", methods=["DELETE"])
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

    return jsonify({
        "response": "Success",
        "message": f"Brod s ID-em {brod_id} je obrisan!"
    }), 200


@app.route("/")
def home():
    return jsonify({
        "message": "Evidencija brodova radi!"
    }), 200

if __name__ == "__main__":
    app.run(port=5000)