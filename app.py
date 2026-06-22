from models import db, Brod
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pony import orm
from datetime import datetime, timedelta

app = Flask(__name__)

# Spajanje na SQLite bazu i kreiranje tablica ako još ne postoje
db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)

# Pretvaranje datetime objekta u čitljiv datum
def formatiraj_datum(datum):
    if datum:
        return datum.strftime("%d-%m-%Y")
    return ""

# Dostupno u svim html predlošcima
app.jinja_env.globals.update(formatiraj_datum=formatiraj_datum)

# Koristi se za sortiranje brodova po datumu zadnjeg servisa
def datum_servisa(brod):
    return brod.zadnji_servis

# Brojenje brodova po tipu za graf
def statistika_tipova(brodovi):
    tipovi = {}

    for brod in brodovi:
        if brod.tip in tipovi:
            tipovi[brod.tip] += 1
        else:
            tipovi[brod.tip] = 1

    return tipovi

# Statistika servisa za pie chart
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

# Podjela brodova po starosti
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

# Brodovi koji najduže čekaju na servis
def brodovi_za_servis(brodovi):
    lista = []

    for brod in brodovi:
        if brod.zadnji_servis:
            lista.append(brod)
        
    lista.sort(key=datum_servisa)

    return lista[:5]

# Prikaz forme i spremanje novog broda
@app.route("/dodaj-brod", methods=["GET", "POST"])
@orm.db_session
def dodaj_brod():
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

            orm.commit()

            return redirect(url_for("pregled_brodova"))
    
        except Exception as e:
            return jsonify({
                "response": "Error",
                "message": str(e)
            }), 400

# Popis svih brodova
@app.route("/brodovi", methods=["GET"])
@orm.db_session
def pregled_brodova():
    brodovi = Brod.select()
    return render_template("brodovi.html", brodovi=brodovi)

# Prikaz detalja pojedinog broda
@app.route("/brod/<int:brod_id>", methods=["GET"])
@orm.db_session
def detalji_broda(brod_id):
    brod = Brod.get(id=brod_id)
    if not brod:
        return jsonify({
            "response": "Error",
            "message": f"Brod s ID-em {brod_id} ne postoji!"
        }), 404

    return render_template("detalji_broda.html", brod=brod)

# Dohvat postojećih brodova i spremanje izmjena
@app.route("/uredi-brod/<int:brod_id>", methods=["GET", "POST"])
@orm.db_session
def uredi_brod(brod_id):
    brod = Brod.get(id=brod_id)

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

# Brisanje odabranog broda
@app.route("/obrisi-brod/<int:brod_id>", methods=["POST"])
@orm.db_session
def obrisi_brod(brod_id):
    brod = Brod.get(id=brod_id)
    if not brod:
        return jsonify({
            "response": "Error",
            "message": f"Brod s ID-em {brod_id} ne postoji!"
        }), 404

    brod.delete()
    orm.commit()

    return redirect(url_for("pregled_brodova"))

# Početna stranica
@app.route("/")
@orm.db_session
def pocetna():
    brodovi = list(Brod.select())

    ukupno_brodova = len(brodovi)

    tipovi = []

    for brod in brodovi:
        if brod.tip not in tipovi:
            tipovi.append(brod.tip)
    
    broj_tipova = len(tipovi)

    servis_u_redu, servis_kasni, bez_servisa = statistika_servisa(brodovi)

    return render_template(
        "pocetna.html",
        ukupno_brodova=ukupno_brodova, servis_kasni=servis_kasni, bez_servisa=bez_servisa, broj_tipova=broj_tipova
        )

# Priprema podataka za grafove i tablicu statitike
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

# Vlastita stranica za 404 grešku
@app.errorhandler(404)
def stranica_nije_pronadena(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(port=5000)