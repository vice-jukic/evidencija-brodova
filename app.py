from models import db, Brod
from flask import Flask, render_template, request, redirect, url_for
from pony import orm
from datetime import datetime, timedelta

app = Flask(__name__)

db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

@app.template_filter("format_datum")
def formatiraj_datum(datum):
    if datum:
        return datum.strftime("%d.%m.%Y.")
    return ""

def procitaj_datum_servisa():
    datum_servisa = request.form.get("zadnji_servis")

    if datum_servisa:
        return datetime.strptime(datum_servisa, "%Y-%m-%d")
    
    return None

def datum_servisa(brod):
    return brod.zadnji_servis

def statistika_tipova(brodovi):
    tipovi = {}

    for brod in brodovi:
        if brod.tip in tipovi:
            tipovi[brod.tip] += 1
        else:
            tipovi[brod.tip] = 1

    return tipovi

def statistika_servisa(brodovi):
    servis_u_redu = 0
    servis_kasni = 0
    bez_servisa = 0

    granica_servisa = datetime.now() - timedelta(days=365)

    for brod in brodovi:
        if brod.zadnji_servis is None:
            bez_servisa += 1
        elif brod.zadnji_servis < granica_servisa:
            servis_kasni += 1
        else:
            servis_u_redu += 1
    
    return servis_u_redu, servis_kasni, bez_servisa

def statistika_starosti(brodovi):
    mladi_brodovi = 0
    srednji_brodovi = 0
    stari_brodovi = 0

    trenutna_godina = datetime.now().year

    for brod in brodovi:
        starost = trenutna_godina - brod.godina

        if starost <= 10:
            mladi_brodovi += 1
        elif starost <= 20:
            srednji_brodovi += 1
        else:
            stari_brodovi += 1
    
    return mladi_brodovi, srednji_brodovi, stari_brodovi

def brodovi_za_servis(brodovi):
    lista = []

    for brod in brodovi:
        if brod.zadnji_servis:
            lista.append(brod)
        
    lista.sort(key=datum_servisa)

    return lista[:5]

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
    app.run(port=5000)