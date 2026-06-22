from datetime import datetime
from flask import request

def formatiraj_datum(datum):
    if datum:
        return datum.strftime("%d.%m.%Y.")
    return ""

def procitaj_datum_servisa():
    datum_servisa = request.form.get("zadnji_servis")

    if datum_servisa:
        return datetime.strptime(datum_servisa, "%Y-%m-%d")
    
    return None