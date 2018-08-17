# Saldoseuraaja

Saldoseuraaja

Saldoseuraajan avulla käyttäjä voi tallentaa ja analysoida päivittäistä rahankäyttöään.

Toimintoja, joita voi tehdä ennen kuin on kirjautunut:
1) Kirjautuminen (edellyttää rekisteröitymistä)
2) Rekisteröityminen

Toimintoja kirjautumisen jälkeen:
1) rahalähteen lisääminen
	a. jos käyttäjä kirjautuu ensimmäisen kerran TAI hänellä ei ole vielä merkintää money_source -taulussa, niin käyttäjälle asetetaan rahalähde "Käteinen".
	b. Käyttäjä voi lisätä uuden rahalähteen antamalla tiedot: rahalähteen nimi (esim. S-pankin tili1) ja lisätiedon (esim. IBAN tai jotain muuta, jos käyttäjä haluaa antaa rahalähteelle kuvaavan nimen). Rahalähteen nimi on käyttäjäkohtaisesti uniikki.
	c. ideana tässä ei ole luoda mitään globaalia varastoa rahalähteille, jotka olisivat kaikkien käyttäjien saatavilla, vaan tässä on ideana se että kaikki käyttäjät saavat luoda omiin tarpeisiinsa sopivat ja kuvaavat rahalähteet.

Lisäämisen lisäksi rahalähdettä voi muuttaa, joko päivittämällä rahalähteen nimeä tai lisätietoja.
Rahalähteen/lähteet voi myös poistaa.

2) Kategorian lisääminen
	Käyttäjä voi lisätä kategorioita antamalla kategorian nimen (esim. auto, kesämökki, vapaa-aika, vakuutukset, sähkö)

Kategorioita voi muuttaa jälkikäteen ts. päivittämällä nimiä (esim. typojen korjaaminen jne.)

Kategorian/t voi myös poistaa.

3) Uuden menon/tulon (aka. transaktio) lisääminen
	a. Tässä annetaan tiedot: tapahtuman päivämäärä, onko kyseessä meno (oletuksena: kyllä), rahasumma, kohde, kategoria, lisätietoja tapahtumasta (vapaamuotoinen tekstikenttä)
	b. jos transaktion aikana annetaan uusi kategoria tai rahalähde, niin se lisätään money_source ja category -tauluihin
	c. transaktiolle voi toki antaa jos olemassa olevan rahalähteen tahi kategorian

Transaktiota voi päivittää luonnollisesti jälkikäteen
Transaktion/t voi myös poistaa.

4) Saldotilanteen lisääminen
	a. käyttäjä voi antaa sovellukseen saldotilanteensa esim. päivältä X (@ rahalähde Y)
	b. Annetaan siis rahalähde ja saldo euroina (aikaleima luodaan automaagisesti)

Erikoistapaus: oletetaan, että käyttäjän saldo on ollut 15.8.2018 esim. S-Pankissa 900 euroa ja sitä edeltävänä päivänä 14.8.2018 950 euroa. 14.8. on merkitty transaktioihin S-pankille 30 euroa menoja, eli 20 euroa on jäänyt merkitsemättä. Saldo-puolelta voi valinnaisesti luoda transaktio puolelle 1-n transaktiota, jotka vastaisivat tätä erotusta 50-30 euroa. Tätä ei toki ole pakko tehdä, mutta tämä on mahdollista, jos haluaakin jälkikäteen laittaa menonsa tarkemmin (esim. baari-illan kuitit löytyivät farkkujen taskusta)

Jos päivän saldoa jälkikäteen päivittää, niin tällöin tarjotaan mahdollisuus katsoa, että täsmääkö transaktio-puolen tapahtumat nykyistä saldoa. Jos ei, niin transaktioita voi käydä päivittämässä TAI sitten niitä voi taas kerran lisätä 1...n kappaletta saldo-puolelta.

Päivittäiset saldomerkinnät voi myös poistaa. 

5) raportointi

Käyttäjä saa raportit, joissa näkyy
	a. kuukausittainen rahan kulutus
	b. saldotilanne + mikä on keskimääräinen päiväkulutus, jos budjetissa halutaan pysyä (jos budjetti on asetettu), ollaanko plussalla vai miinuksella (ja miten paljon).
	c. jos käyttäjä on laittanut esim. elokuulle vain 4 saldomerkintää siinä missä toinen ahkerampi käyttäjä olisi laittanut kaikki 31 merkintää, niin laiskalle käyttäjälle raportti täyttää tyhjät kohdat automaattisesti ns. trendin mukaisilla arvoilla

Tietokanta-taulut:
User:
Tässä on käyttäjän alias/nimi, käyttäjätunnus ja salasana*

money_source:
Rahalähteen nimi ja tarkempi kuvaus
viittaus User-tauluun user 1...n money_source

category:
KAtegorian nimi
viittaus User-tauluun User 1...n category

Transactions:
päivittäiset menot/tulot
viittaus USer-tauluun user 1...n Transactions
viittaus money_source-tauluun money_source 1...n Transactions
viittaus category-tauluun category 1...n Transactions

Saldo:
Saldotilanne per päivä
viittaus USer-tauluun user 1...n Saldo
viittaus money_source-tauluun money_source 1...n Saldo




* lopullisessa toteutuksessa on tavoitteena se, että salasana on kryptattuna tietokannassa