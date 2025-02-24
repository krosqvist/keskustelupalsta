# keskustelupalsta

## Sovellukset ominaisuudet

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan luomiaan keskusteluja.
* Käyttäjä pystyy kommentoimaan keskusteluja, sekä poistamaan omia kommenttejaan.
* Käyttäjä näkee sovellukseen lisätyt keskustelut.
* Käyttäjä pystyy etsimään keskusteluja hakusanalla tai luokituksella.
* Käyttäjä pystyy etsimään toisia käyttäjiä käyttäjänimen perusteella
* Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän keskustelut, kommentit ja niiden lukumäärän.
* Käyttäjä pystyy valitsemaan keskustelulle yhden tai useamman aiheen. Luokat ovat tietokannassa.
* Käyttäjä pystyy lisäämään kuvan keskustelunavaukseen.

## Sovelluksen käyttäminen

Asenna flask:

```
$ pip install flask
```

Alusta tietokanta:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Käynnistä sovellus:

```
$ flask run
```

## Sovelluksen toiminta 10 miljoonalla kommentilla

```
elapsed time: 2.24 s
127.0.0.1 - - [24/Feb/2025 15:16:08] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [24/Feb/2025 15:16:08] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [24/Feb/2025 15:16:08] "GET /favicon.ico HTTP/1.1" 302 -
elapsed time: 2.2 s
127.0.0.1 - - [24/Feb/2025 15:16:10] "GET / HTTP/1.1" 200 -
elapsed time: 2.22 s
127.0.0.1 - - [24/Feb/2025 15:16:15] "GET /2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [24/Feb/2025 15:16:15] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [24/Feb/2025 15:16:15] "GET /favicon.ico HTTP/1.1" 302 -
elapsed time: 0.0 s
127.0.0.1 - - [24/Feb/2025 15:16:17] "GET /find_user HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [24/Feb/2025 15:16:17] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [24/Feb/2025 15:16:17] "GET /favicon.ico HTTP/1.1" 302 -
elapsed time: 2.48 s
127.0.0.1 - - [24/Feb/2025 15:16:18] "GET / HTTP/1.1" 200 -
elapsed time: 2.46 s
127.0.0.1 - - [24/Feb/2025 15:16:19] "GET / HTTP/1.1" 200 -
```
