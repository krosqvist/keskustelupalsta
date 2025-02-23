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
