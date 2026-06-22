from models import db, Brod
from seed import init_seed
from services.statistika_service import (statistika_tipova, statistika_servisa, statistika_starosti, brodovi_za_servis)
from utils.datum_utils import (formatiraj_datum, procitaj_datum_servisa)
from flask import Flask, render_template, request, redirect, url_for
from pony import orm

app = Flask(__name__)
app.add_template_filter(formatiraj_datum, "format_datum")

db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

@app.route("/")
@orm.db_session
def pocetna():
    brodovi = list(Brod.select())

    ukupno_brodova = len(brodovi)
    
    broj_tipova = len(statistika_tipova(brodovi))

    servis_u_redu, servis_kasni, bez_servisa = statistika_servisa(brodovi)

    return render_template(
        "pocetna.html",
        ukupno_brodova=ukupno_brodova, servis_kasni=servis_kasni, bez_servisa=bez_servisa, broj_tipova=broj_tipova
        )

@app.route("/brodovi", methods=["GET"])
@orm.db_session
def pregled_brodova():
    brodovi = list(Brod.select())
    return render_template("brodovi.html", brodovi=brodovi)

@app.route("/brod/<int:brod_id>", methods=["GET"])
@orm.db_session
def detalji_broda(brod_id):
    brod = Brod.get(id=brod_id)
    if not brod:
        return render_template("404.html"), 404

    return render_template("detalji_broda.html", brod=brod)

@app.route("/dodaj-brod", methods=["GET", "POST"])
@orm.db_session
def dodaj_brod():
    if request.method == "GET":
        return render_template("dodaj_brod.html")
    
    zadnji_servis = procitaj_datum_servisa()
            
    Brod(
        naziv = request.form["naziv"],
        registracija = request.form["registracija"],
        tip = request.form["tip"],
        duljina = float(request.form["duljina"]),
        godina = int(request.form["godina"]),
        ima_jedra = "ima_jedra" in request.form,
        ima_tende = "ima_tende" in request.form,
        oprema = request.form["oprema"],
        opis = request.form["opis"],
        zadnji_servis = zadnji_servis
    )

    orm.commit()

    return redirect(url_for("pregled_brodova"))

@app.route("/uredi-brod/<int:brod_id>", methods=["GET", "POST"])
@orm.db_session
def uredi_brod(brod_id):
    brod = Brod.get(id=brod_id)

    if not brod:
        return render_template("404.html"), 404
    
    if request.method == "GET":
        return render_template("uredi_brod.html", brod=brod)
    
    zadnji_servis = procitaj_datum_servisa()
  
    brod.naziv = request.form["naziv"]
    brod.registracija = request.form["registracija"]
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

@app.route("/obrisi-brod/<int:brod_id>", methods=["POST"])
@orm.db_session
def obrisi_brod(brod_id):
    brod = Brod.get(id=brod_id)
    if not brod:
        return render_template("404.html"), 404

    brod.delete()
    orm.commit()

    return redirect(url_for("pregled_brodova"))

@app.route("/statistika")
@orm.db_session
def statistika():
    brodovi = list(Brod.select())

    tipovi = statistika_tipova(brodovi)
    servis_u_redu, servis_kasni, bez_servisa = statistika_servisa(brodovi)
    mladi_brodovi, srednji_brodovi, stari_brodovi = statistika_starosti(brodovi)
    lista_servisa = brodovi_za_servis(brodovi)

    return render_template(
        "statistika.html",
        tipovi=tipovi,
        servis_u_redu=servis_u_redu, servis_kasni=servis_kasni, bez_servisa=bez_servisa,
        mladi_brodovi=mladi_brodovi, srednji_brodovi=srednji_brodovi, stari_brodovi=stari_brodovi,
        brodovi_za_servis=lista_servisa
    )

@app.errorhandler(404)
def stranica_nije_pronadena(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    init_seed()
    app.run(host="0.0.0.0", port=5000)