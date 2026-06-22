from pony import orm
from datetime import datetime
from app import db
from models.brod import Brod

podaci = [
    {"naziv":"Adriatic Star", "registracija":"ST-2145", "tip":"Jedrilica","duljina":12.5,"godina":2018,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Genoa, Lazy bag, Bimini, Sprayhood GPS, Radar", "zadnji_servis": datetime(2026, 5, 15), "opis":"Prostrana obiteljska jedrilica namijenjena višednevnim krstarenjima."},
    {"naziv":"Sea Queen", "registracija":"DU-5089", "tip":"Jahta","duljina":15.2,"godina":2007,"ima_jedra":False,"ima_tende":True,"oprema":"Bočne tende, GPS, Radar, Klima, Frižider", "zadnji_servis": datetime(2026, 3, 22), "opis":"Luksuzna jahta namijenjena višednevnim krstarenjima i udobnom boravku na moru."},
    {"naziv":"Blue Horizon", "registracija":"ZD-1742", "tip":"Katamaran","duljina":14.8,"godina":2020,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Genoa, Lazy bag, Sprayhood, Radar, Autopilot", "zadnji_servis": datetime(2026, 4, 4), "opis":"Moderan katamaran s velikom palubom i udobnim kabinama."},
    {"naziv":"Dalmatia", "registracija":"ST-3328", "tip":"Jedrilica","duljina":11.3,"godina":2015,"ima_jedra":True,"ima_tende":False,"oprema":"Glavno jedro, Genoa, GPS", "zadnji_servis": None, "opis":"Klasična jedrilica pogodna za rekreativnu plovidbu."},
    {"naziv":"Aurora", "registracija":"PU-6194", "tip":"Gliser","duljina":7.1,"godina":2022,"ima_jedra":False,"ima_tende":True,"oprema":"Radio", "zadnji_servis": datetime(2025, 7, 18), "opis":"Brzi gliser za sportske aktivnosti i kraće izlete."},
    {"naziv":"Sea Wolf", "registracija":"RI-2751", "tip":"Jahta","duljina":16.8,"godina":2001,"ima_jedra":False,"ima_tende":True,"oprema":"Bočna tenda, GPS, Radar, Generator, Klima", "zadnji_servis": datetime(2026, 3, 2), "opis":"Prostrana jahta s velikim kokpitom i udobnim kabinama."},
    {"naziv":"Poseidon", "registracija":"ZD-4187", "tip":"Jedrilica","duljina":13.4,"godina":2011,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Genoa, Lazy bag, Radar", "zadnji_servis": datetime(2025, 7, 27), "opis":"Jedrilica prilagođena dužim putovanjima i regatama."},
    {"naziv":"Mistral", "registracija":"ŠI-7032", "tip":"Katamaran","duljina":15.6,"godina":2019,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Genoa, Code 0, Lazy bag, Autopilot", "zadnji_servis": None, "opis":"Prostrani katamaran za charter i obiteljski odmor."},
    {"naziv":"Libertas", "registracija":"DU-2564", "tip":"Jahta","duljina":13.7,"godina":2009,"ima_jedra":False,"ima_tende":True,"oprema":"Bimini, Bočne tende, GPS, Radar, Frižider", "zadnji_servis": None, "opis":"Elegantna jahta pogodna za obiteljska krstarenja."},
    {"naziv":"Jadran", "registracija":"ST-9475", "tip":"Jedrilica","duljina":12.9,"godina":2017,"ima_jedra":True,"ima_tende":False,"oprema":"Glavno jedro, Genoa, Radar", "zadnji_servis": datetime(2025, 9, 30), "opis":"Dobro održavana jedrilica s izvrsnim plovnim svojstvima."},
    {"naziv":"Orion", "registracija":"PU-1823", "tip":"Gliser","duljina":6.5,"godina":2016,"ima_jedra":False,"ima_tende":True,"oprema":"Bimini, Radio", "zadnji_servis": datetime(2026, 6, 1), "opis":"Mali gliser namijenjen rekreativnoj plovidbi."},
    {"naziv":"Sea Breeze", "registracija":"ZD-5681", "tip":"Katamaran","duljina":16.2,"godina":2021,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Genoa, Lazy bag, GPS, Radar", "zadnji_servis": datetime(2025, 2, 8), "opis":"Luksuzni katamaran s modernom navigacijskom opremom."},
    {"naziv":"Marina", "registracija":"RI-6217", "tip":"Jahta","duljina":14.9,"godina":2012,"ima_jedra":False,"ima_tende":True,"oprema":"Bimini, Sprayhood, GPS, Klima, Radio", "zadnji_servis": datetime(2025, 11, 19), "opis":"Moderna jahta za udobna ljetna putovanja."},
    {"naziv":"Bonaca", "registracija":"ŠI-3148", "tip":"Jedrilica","duljina":11.8,"godina":2005,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Genoa, Lazy bag, Sprayhood, Radio", "zadnji_servis": datetime(2026, 6, 3), "opis":"Pouzdana jedrilica za obalna krstarenja."},
    {"naziv":"Galeb", "registracija":"ST-8452", "tip":"Jahta","duljina":12.8,"godina":1998,"ima_jedra":False,"ima_tende":False,"oprema":"GPS, Radar, Frižider", "zadnji_servis": datetime(2025, 12, 25), "opis":"Klasična jahta redovito održavana i prilagođena dužim putovanjima."},
    {"naziv":"Val", "registracija":"DU-7306", "tip":"Jedrilica","duljina":13.7,"godina":2014,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Lazy bag, Radar", "zadnji_servis": datetime(2025, 8, 16), "opis":"Jedrilica s prostranom kabinom i velikim spremištem."},
    {"naziv":"Neptun", "registracija":"ZD-2865", "tip":"Katamaran","duljina":17.1,"godina":2023,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Code 0, Lazy bag, Autopilot", "zadnji_servis": datetime(2025, 3, 11), "opis":"Novi katamaran pogodan za duže odmore na moru."},
    {"naziv":"Astra", "registracija":"PU-4901", "tip":"Gliser","duljina":6.8,"godina":2018,"ima_jedra":False,"ima_tende":True,"oprema":"Bimini, Sprayhood, Radio", "zadnji_servis": datetime(2025, 12, 5), "opis":"Lagani gliser za brzu i udobnu vožnju."},
    {"naziv":"Laguna", "registracija":"RI-1576", "tip":"Jahta","duljina":17.3,"godina":2010,"ima_jedra":False,"ima_tende":True,"oprema":"Sprayhood, GPS, Radar, Generator, Klima", "zadnji_servis": datetime(2026, 5, 28), "opis":"Prostrana jahta s bogatom opremom i velikim spremišnim prostorom."},
    {"naziv":"Sirocco", "registracija":"ŠI-6382", "tip":"Jedrilica","duljina":12.1,"godina":2008,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Sprayhood, Radar", "zadnji_servis": datetime(2025, 11, 7), "opis":"Jedrilica s dobrim performansama u svim uvjetima."},
    {"naziv":"Titan", "registracija":"DU-7219", "tip":"Jahta","duljina":14.1,"godina":2013,"ima_jedra":False,"ima_tende":True,"oprema":"Bimini, GPS, Radar, Klima", "zadnji_servis": datetime(2025, 4, 12), "opis":"Pouzdana jahta za višednevne izlete i odmor."},
    {"naziv":"Mare", "registracija":"ST-3647", "tip":"Jedrilica","duljina":11.6,"godina":2016,"ima_jedra":True,"ima_tende":False,"oprema":"Glavno jedro, Genoa, GPS", "zadnji_servis": datetime(2025, 9, 21), "opis":"Obiteljska jedrilica jednostavna za upravljanje."},
    {"naziv":"Atlantis", "registracija":"ZD-895", "tip":"Katamaran","duljina":15.4,"godina":2018,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Genoa, Lazy bag, Bimini, Radar", "zadnji_servis": datetime(2026, 4, 30), "opis":"Katamaran s velikim prostorom za posadu i goste."},
    {"naziv":"Luna", "registracija":"PU-2138", "tip":"Gliser","duljina":7.4,"godina":2021,"ima_jedra":False,"ima_tende":True,"oprema":"Sprayhood, Radio", "zadnji_servis": None, "opis":"Moderan gliser namijenjen ljetnim izletima."},
    {"naziv":"Adria", "registracija":"RI-5479", "tip":"Jahta","duljina":13.5,"godina":2003,"ima_jedra":False,"ima_tende":False,"oprema":"GPS, Generator, Frižider", "zadnji_servis": datetime(2026, 5, 20), "opis":"Dobro održavana jahta za rekreativna krstarenja."},
    {"naziv":"Mirna", "registracija":"ŠI-4625", "tip":"Jedrilica","duljina":13.2,"godina":2019,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Genoa, Lazy bag, Autopilot", "zadnji_servis": datetime(2025, 8, 1), "opis":"Dobro opremljena jedrilica za duža putovanja."},
    {"naziv":"Phoenix", "registracija":"DU-8361", "tip":"Katamaran","duljina":16.8,"godina":2022,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Code 0, Lazy bag, Radar", "zadnji_servis": datetime(2026, 2, 17), "opis":"Prostrani katamaran s velikim spremnicima i kabinama."},
    {"naziv":"Kornati", "registracija":"ZD-1297", "tip":"Jahta","duljina":15.6,"godina":2006,"ima_jedra":False,"ima_tende":True,"oprema":"Bimini, GPS, Radar, Klima, Radio", "zadnji_servis": datetime(2025, 7, 6), "opis":"Komforna jahta prilagođena obiteljskim putovanjima."},
    {"naziv":"Bura", "registracija":"ST-6583", "tip":"Jedrilica","duljina":12.7,"godina":2011,"ima_jedra":True,"ima_tende":True,"oprema":"Glavno jedro, Lazy bag, Radio", "zadnji_servis": datetime(2025, 12, 13), "opis":"Jedrilica poznata po stabilnosti i sigurnosti na moru."},
    {"naziv":"Delfin", "registracija":"PU-3746", "tip":"Gliser","duljina":6.9,"godina":2017,"ima_jedra":False,"ima_tende":True,"oprema":"Sprayhood, GPS", "zadnji_servis": datetime(2025, 6, 24), "opis":"Mali gliser za brzu vožnju i vodene sportove."}
]

if Brod.exists():
    Brod.drop_table(with_all_data=True)

Brod.create_table()

@orm.db_session
def dodaj_podatke():
    for brod in podaci:
        Brod(**brod)

dodaj_podatke()
