# Evidencija brodova  

## Opis projekta

Aplikacija služi za vođenje evidencije brodova te upravljanje njihovim podacima u jedinstvenom sustavu. Sustav omogućuje unos, pregled, izmjenu i brisanje podataka o brodovima, kao i analizu osnovnih statističkih informacija vezanih uz flotu.

Cilj projekta je demonstrirati izgradnju jednostavne web aplikacije s bazom podataka, CRUD operacijama te osnovnom statistikom i prikazom podataka kroz web sučelje.

Aplikacija je razvijena koristeći Python Flask framework, Pony ORM-a te SQLite baze podataka.

## Funkcionalnosti

Aplikacija omogućuje osnovno upravljanje podacima o brodovima i pregled informacija.

U sustavu se može:
- dodati novi brod s osnovnim podacima (naziv, tip, registracija, dimenzije, godina proizvodnje, oprema)
- pregledati popis svih unesenih brodova u tabličnom obliku
- otvoriti detalje pojedinog broda
- urediti postojeće podatke o brodu
- obrisati brod iz sustava
- evidentirati datum zadnjeg servisa

Osim osnovnog CRUD dijela, aplikacija računa i prikazuje nekoliko jednostavnih statistika:
- raspodjela brodova po tipu
- podjela prema starosti brodova
- pregled statusa servisa (uredno, kasni, nema podatka)
- lista brodova kojima servis kasni

Podaci se dodatno prikazuju kroz grafove radi lakšeg pregleda.

## Pokretanje aplikacije lokalno (Docker)

Aplikacija se pokreće pomoću Dockera i Docker Composea.

### Preduvjeti

- instaliran Docker Desktop
- instaliran Git

### Koraci

Kloniranje repozitorija  
git clone https://github.com/vice-jukic/evidencija-brodova  

Ulazak u projekt  
cd evidencija-brodova  

Pokretanje aplikacije putem Dockera  
docker-compose up --build  

Nakon što se svi servisi podignu, aplikacija je dostupna na:  
http://localhost:5000  

### Zaustavljanje aplikacije

CTRL + C u terminalu ili  
docker-compose down  

### Napomena

Prvo pokretanje može trajati malo duže jer Docker mora izgraditi kontejnere i postaviti bazu podataka.

## Struktura projekta

Projekt je organiziran na sljedeći način:

- app.py – glavna Flask aplikacija i rute
- models/ – definicija baze podataka
- services/ – logika za statistiku i obradu podataka
- utils/ – pomoćne funkcije (datumi, formatiranje)
- templates/ – HTML predlošci
- static/ – CSS
- seed.py – skripta za inicijalno punjenje baze podataka
- docker-compose.yml – konfiguracija za pokretanje sustava

## Dokumentacija koda

### app.py

Glavna datoteka aplikacije koja:
- definira Flask rute
- upravlja CRUD operacijama nad brodovima
- povezuje frontend i bazu podataka
- poziva servisne funkcije za statistiku

### models

Sadrži definiciju baze podataka pomoću Pony ORM-a.  
Entitet `Brod` sadrži sve atribute koji opisuju jedan brod (naziv, tip, godina, servis i slično).

### services

Sadrži poslovnu logiku aplikacije:
- statistika brodova po tipu
- statistika servisa
- analiza starosti brodova
- filtriranje brodova za prikaz (npr. servis)

### utils

Pomoćne funkcije koje se koriste u aplikaciji:
- formatiranje datuma za prikaz u HTML-u
- dohvaćanje i parsiranje datuma iz formi

### seed.py

Skripta za inicijalno punjenje baze podacima.  
Koristi se samo po potrebi (npr. prvi start aplikacije ili testiranje), kako bi se dobio početni skup brodova bez ručnog unosa.

### .gitignore

Definira datoteke koje se ne verzioniraju na GitHubu, uključujući lokalnu SQLite bazu (`database.sqlite`) i ostale privremene datoteke.

### Dockerfile

Dockerfile definira kako se aplikacija gradi i pokreće unutar Docker kontejnera.  
U njemu se postavlja Python okruženje, instaliraju potrebne ovisnosti i pokreće Flask aplikacija.

Aplikacija se ne pokreće direktno lokalno, nego unutar Docker kontejnera kako bi radila jednako na svim računalima.

### docker-compose.yml

Definira i povezuje servise potrebne za pokretanje aplikacije.  
U ovom projektu koristi se za pokretanje web aplikacije i povezivanje s bazom podataka.

Omogućuje pokretanje cijelog sustava jednom naredbom (`docker-compose up`).

### .dockerignore

Sadrži datoteke koje se ne uključuju u Docker build proces (npr. cache, lokalne baze, nepotrebni fajlovi).  
Time se smanjuje veličina kontejnera i ubrzava build proces.

## Autor
Ime Prezime: Vice Jukić  
JMBAG: 0243106543  
FIPU 2025./2026.