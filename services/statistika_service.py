from datetime import datetime, timedelta

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
