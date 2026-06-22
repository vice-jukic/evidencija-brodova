from pony import orm
from datetime import datetime
from app import db
from models.brod import Brod

podaci = [
    {"naziv":"Adriatic Star","tip":"Jedrilica","duljina":12.5,"godina":2018,"ima_jedra":True,"ima_tende":True,"oprema":"GPS, Radar", "zadnji_servis": datetime(2025, 5, 15), "opis":"Prostrana obiteljska jedrilica namijenjena višednevnim krstarenjima."},
    {"naziv":"Sea Queen","tip":"Jahta","duljina":15.2,"godina":2007,"ima_jedra":False,"ima_tende":True,"oprema":"GPS, Radar, Klima, Frižider", "zadnji_servis": datetime(2026, 3, 22), "opis":"Luksuzna jahta namijenjena višednevnim krstarenjima i udobnom boravku na moru."},
    {"naziv":"Blue Horizon","tip":"Katamaran","duljina":14.8,"godina":2020,"ima_jedra":True,"ima_tende":True,"oprema":"Radar, Autopilot", "zadnji_servis": datetime(2024, 12, 10), "opis":"Moderan katamaran s velikom palubom i udobnim kabinama."},
    {"naziv":"Dalmatia","tip":"Jedrilica","duljina":11.3,"godina":2015,"ima_jedra":True,"ima_tende":False,"oprema":"GPS", "zadnji_servis": None, "opis":"Klasična jedrilica pogodna za rekreativnu plovidbu."},
    {"naziv":"Aurora","tip":"Gliser","duljina":7.1,"godina":2022,"ima_jedra":False,"ima_tende":True,"oprema":"Radio", "zadnji_servis": datetime(2024, 1, 18), "opis":"Brzi gliser za sportske aktivnosti i kraće izlete."},
    {"naziv":"Sea Wolf","tip":"Jahta","duljina":16.8,"godina":2001,"ima_jedra":False,"ima_tende":True,"oprema":"GPS, Radar, Generator, Klima", "zadnji_servis": datetime(2023, 11, 2), "opis":"Prostrana jahta s velikim kokpitom i udobnim kabinama."},
    {"naziv":"Poseidon","tip":"Jedrilica","duljina":13.4,"godina":2011,"ima_jedra":True,"ima_tende":True,"oprema":"Radar", "zadnji_servis": datetime(2023, 7, 27), "opis":"Jedrilica prilagođena dužim putovanjima i regatama."},
    {"naziv":"Mistral","tip":"Katamaran","duljina":15.6,"godina":2019,"ima_jedra":True,"ima_tende":True,"oprema":"Autopilot", "zadnji_servis": None, "opis":"Prostrani katamaran za charter i obiteljski odmor."},
    {"naziv":"Libertas","tip":"Jahta","duljina":13.7,"godina":2009,"ima_jedra":False,"ima_tende":True,"oprema":"GPS, Radar, Frižider", "zadnji_servis": None, "opis":"Elegantna jahta pogodna za obiteljska krstarenja."},
    {"naziv":"Jadran","tip":"Jedrilica","duljina":12.9,"godina":2017,"ima_jedra":True,"ima_tende":False,"oprema":"Radar", "zadnji_servis": datetime(2021, 9, 30), "opis":"Dobro održavana jedrilica s izvrsnim plovnim svojstvima."},
    {"naziv":"Orion","tip":"Gliser","duljina":6.5,"godina":2016,"ima_jedra":False,"ima_tende":True,"oprema":"Radio", "zadnji_servis": datetime(2025, 6, 1), "opis":"Mali gliser namijenjen rekreativnoj plovidbi."},
    {"naziv":"Sea Breeze","tip":"Katamaran","duljina":16.2,"godina":2021,"ima_jedra":True,"ima_tende":True,"oprema":"GPS, Radar", "zadnji_servis": datetime(2025, 2, 8), "opis":"Luksuzni katamaran s modernom navigacijskom opremom."},
    {"naziv":"Marina","tip":"Jahta","duljina":14.9,"godina":2012,"ima_jedra":False,"ima_tende":True,"oprema":"GPS, Klima, Radio", "zadnji_servis": datetime(2024, 11, 19), "opis":"Moderna jahta za udobna ljetna putovanja."},
    {"naziv":"Bonaca","tip":"Jedrilica","duljina":11.8,"godina":2005,"ima_jedra":True,"ima_tende":True,"oprema":"Radio", "zadnji_servis": datetime(2024, 6, 3), "opis":"Pouzdana jedrilica za obalna krstarenja."},
    {"naziv":"Galeb","tip":"Jahta","duljina":12.8,"godina":1998,"ima_jedra":False,"ima_tende":False,"oprema":"GPS, Radar, Frižider", "zadnji_servis": datetime(2025, 12, 25), "opis":"Klasična jahta redovito održavana i prilagođena dužim putovanjima."},
    {"naziv":"Val","tip":"Jedrilica","duljina":13.7,"godina":2014,"ima_jedra":True,"ima_tende":True,"oprema":"Radar", "zadnji_servis": datetime(2023, 8, 16), "opis":"Jedrilica s prostranom kabinom i velikim spremištem."},
    {"naziv":"Neptun","tip":"Katamaran","duljina":17.1,"godina":2023,"ima_jedra":True,"ima_tende":True,"oprema":"Autopilot", "zadnji_servis": datetime(2023, 3, 11), "opis":"Novi katamaran pogodan za duže odmore na moru."},
    {"naziv":"Astra","tip":"Gliser","duljina":6.8,"godina":2018,"ima_jedra":False,"ima_tende":True,"oprema":"Radio", "zadnji_servis": datetime(2022, 12, 5), "opis":"Lagani gliser za brzu i udobnu vožnju."},
    {"naziv":"Laguna","tip":"Jahta","duljina":17.3,"godina":2010,"ima_jedra":False,"ima_tende":True,"oprema":"GPS, Radar, Generator, Klima", "zadnji_servis": datetime(2026, 5, 28), "opis":"Prostrana jahta s bogatom opremom i velikim spremišnim prostorom."},
    {"naziv":"Sirocco","tip":"Jedrilica","duljina":12.1,"godina":2008,"ima_jedra":True,"ima_tende":True,"oprema":"Radar", "zadnji_servis": datetime(2021, 11, 7), "opis":"Jedrilica s dobrim performansama u svim uvjetima."},
    {"naziv":"Titan","tip":"Jahta","duljina":14.1,"godina":2013,"ima_jedra":False,"ima_tende":True,"oprema":"GPS, Radar, Klima", "zadnji_servis": datetime(2025, 4, 12), "opis":"Pouzdana jahta za višednevne izlete i odmor."},
    {"naziv":"Mare","tip":"Jedrilica","duljina":11.6,"godina":2016,"ima_jedra":True,"ima_tende":False,"oprema":"GPS", "zadnji_servis": datetime(2024, 9, 21), "opis":"Obiteljska jedrilica jednostavna za upravljanje."},
    {"naziv":"Atlantis","tip":"Katamaran","duljina":15.4,"godina":2018,"ima_jedra":True,"ima_tende":True,"oprema":"Radar", "zadnji_servis": datetime(2024, 4, 30), "opis":"Katamaran s velikim prostorom za posadu i goste."},
    {"naziv":"Luna","tip":"Gliser","duljina":7.4,"godina":2021,"ima_jedra":False,"ima_tende":True,"oprema":"Radio", "zadnji_servis": None, "opis":"Moderan gliser namijenjen ljetnim izletima."},
    {"naziv":"Adria","tip":"Jahta","duljina":13.5,"godina":2003,"ima_jedra":False,"ima_tende":False,"oprema":"GPS, Generator, Frižider", "zadnji_servis": datetime(2026, 5, 20), "opis":"Dobro održavana jahta za rekreativna krstarenja."},
    {"naziv":"Mirna","tip":"Jedrilica","duljina":13.2,"godina":2019,"ima_jedra":True,"ima_tende":True,"oprema":"Autopilot", "zadnji_servis": datetime(2022, 8, 1), "opis":"Dobro opremljena jedrilica za duža putovanja."},
    {"naziv":"Phoenix","tip":"Katamaran","duljina":16.8,"godina":2022,"ima_jedra":True,"ima_tende":True,"oprema":"Radar", "zadnji_servis": datetime(2026, 2, 17), "opis":"Prostrani katamaran s velikim spremnicima i kabinama."},
    {"naziv":"Kornati","tip":"Jahta","duljina":15.6,"godina":2006,"ima_jedra":False,"ima_tende":True,"oprema":"GPS, Radar, Klima, Radio", "zadnji_servis": datetime(2021, 7, 6), "opis":"Komforna jahta prilagođena obiteljskim putovanjima."},
    {"naziv":"Bura","tip":"Jedrilica","duljina":12.7,"godina":2011,"ima_jedra":True,"ima_tende":True,"oprema":"Radio", "zadnji_servis": datetime(2023, 12, 13), "opis":"Jedrilica poznata po stabilnosti i sigurnosti na moru."},
    {"naziv":"Delfin","tip":"Gliser","duljina":6.9,"godina":2017,"ima_jedra":False,"ima_tende":True,"oprema":"GPS", "zadnji_servis": datetime(2022, 6, 24), "opis":"Mali gliser za brzu vožnju i vodene sportove."}
]

@orm.db_session
def dodaj_podatke():
    for brod in podaci:
        Brod(**brod)
    
    orm.commit()

dodaj_podatke()
