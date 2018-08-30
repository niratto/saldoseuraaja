# Saldoseuraaja

Saldoseuraaja
-------------------
heroku: https://tsoha-saldoseuraaja.herokuapp.com/
(admin-käyttäjän salasana on admin)

Lokaali asennusohje:
-----------------------
Hae saldoseuraaja githubista:
https://github.com/niratto/saldoseuraaja

pystytä virtuaaliympäristö esim. python3 -m venv myvenv<br />
pip install flask<br />
pip install flask_sqlalchemy<br />
pip install flask_login<br />
pip install flask_wtf<br />

Mene sovelluksen kansion juureen ja sieltä löydät run.py -tiedoston

aja tuo tiedosto python run.py

suuntaa http://localhost:5000/auth/login

Ala käyttämään saldoseuraajaa

<h1>Mikä on saldoseuraaja?</h1>

Saldoseuraajan avulla käyttäjä voi tallentaa ja analysoida päivittäistä rahankäyttöään.

<h2>Käyttöohjeistus</h2>
<h3>Ennen kirjautumista</h3>
1) Kirjautuminen (edellyttää rekisteröitymistä)<br />
2) Rekisteröityminen<br /><br />

Jos käyttäjä löytyy tietokannasta ja se on user-tason käyttäjä, niin käyttäjä ohjataan sovelluksen pääsivulle /booking.<br />
Jos käyttäjä on admin-tason käyttäjä, niin käyttäjä ohjataan admin-sivulle.<br />
Jos käyttäjän käyttäjätunnuksesta löytyy sana 'evil', käyttäjää ei autorisoida, vaan tulee ilmoitus tästä.<br />
Jos käyttäjä löytyy tietokannasta, mutta admin on deaktivoinut käyttäjän, käyttäjä ei voi kirjautua ja deaktivoinnista tulee käyttäjälle virheilmoitus.
<hr />
Ensimmäinen rekisteröityminen on AINA admin-tason rekisteröinti. Eli jos laitat huolimattomasti salasanan ja unohdat sen, niin tietokanta pitää palauttaa alkutekijöihin ja aloittaa alusta.<br />
Kaikki admin-rekisteröinnin jälkeiset rekisteröinnit ovat user-tason rekisteröintejä.<br />
Rekisteröinnissä pitää antaa käyttäjällä nimi/alias, käyttäjätunnus sekä salasana KAHTEEN kertaan (ja näiden pitää vastata toisiaan).
<hr />
Admin-tason kirjautumisessa voi siis deaktivoida tietokannasta löytyviä käyttäjiä TAI nollata heidän salasanat, jolloin salasana on käyttäjätunnus VÄÄRINPÄIN.
<br />
<h3>Toimintoja kirjautumisen jälkeen</h3>
<h4>muuta käyttäjän tietoja</h4>
Jos jättää kaikki kentät tyhjiksi ja painaa 'muuta tietoja' niin mitään ei itse asiassa tapahdu. <br />
Jos asettaa vain salasanan uusiksi ja nimi/alias jätetään tyhjäksi, niin salasana vaihtuu mutta alias pysyy samana.<br />
Jos asettaa vain nimen/aliaksen, niin se vaihtuu. Salasana pysyy samana.<br />
Jos vaihdetaan salasana, niin salasana pitää antaa kahteen kertaan ja näiden salasanojen pitää vastata toisiaan.
<h4>lisää rahalähteitä</h4>
	a. jos käyttäjä kirjautuu ensimmäisen kerran TAI hänellä ei ole vielä merkintää money_source -taulussa, niin käyttäjälle asetetaan rahalähde "Käteinen".<br />
	b. Käyttäjä voi lisätä uuden rahalähteen antamalla tiedot: rahalähteen nimi (esim. S-pankin tili1) ja lisätiedon (esim. IBAN tai jotain muuta, jos käyttäjä haluaa antaa rahalähteelle kuvaavan nimen). Rahalähteen nimi on käyttäjäkohtaisesti uniikki.<br />
	c. ideana tässä ei ole luoda mitään globaalia varastoa rahalähteille, jotka olisivat kaikkien käyttäjien saatavilla, vaan tässä on ideana se että kaikki käyttäjät saavat luoda omiin tarpeisiinsa sopivat ja kuvaavat rahalähteet.<br />

Lisäämisen lisäksi rahalähdettä voi muuttaa, joko päivittämällä rahalähteen nimeä tai lisätietoja.<br />
Rahalähteen/lähteet voi myös poistaa.<br />

<h4>menon/tulon (aka. transaktio) lisääminen</h4>
	a. Tässä annetaan tiedot: tapahtuman päivämäärä, rahalähde, summa, onko kyseessä meno (oletuksena: kyllä), kohde, lisätietoja tapahtumasta (vapaamuotoinen tekstikenttä)<br />
	c. transaktion rahalähteet siis otetaan money_source -taulusta (eli rahalähteen lisääminen -vaihe)<br />

<br />Transaktiota voi päivittää luonnollisesti jälkikäteen
<br />Transaktion/t voi myös poistaa.
<br />Sovellus kertoo käyttäjälle, jos käyttäjä on täyttänyt tiedot väärin/puutteellisesti.

<h4>Saldotilanteen lisääminen</h4>
	a. käyttäjä voi antaa sovellukseen saldotilanteensa esim. päivältä X (@ rahalähde Y)<br />
	b. Annetaan siis rahalähde ja saldo euroina (aikaleima luodaan automaagisesti, mutta sitä voi toki muuttaa)<br />


<br /><br />
Päivittäisiä saldomerkintöjä voi muokata ja poistaa. 

<h4>budjetin luominen</h4>
Tässä ideana on siis seuraava... Oletetaan, että palkkapäivä olisi aina kuun 15. päivä ja rahaa tulisi tilille 2500 euroa. Silloin voisi tehdä vaikka budjetin nimellä 'elokuun liksa' ja antaa budjetille suuruuden 2500 euroa ja aikaväliksi 15.8.-15.9.2018.<br />
Tämän budjetin tekeminen ei ensi näkemällä tee mitään, mutta tämän budjetin pohjalta pyöräytetään raportti raportointi-vaiheessa (seuraava) ja tällä raportilla nähdään, että miten paljon laskennallisesti käyttäjä voisi päivittäin rahaa käyttää.<br />
Jos käyttäjä on tehnyt myös saldomerkintöjä (lisää saldo) niin tämä vertailee myös budjettia näihin saldomerkintöihin ja näyttää rinnakkain budjettiin perustuvan päiväkulutuksen ja annettuihin saldoihin perustuvan päiväkulutuksen.<br />
Tällä tavoin käyttäjä voi ihailla sitä, miten oma käyttö pysyykin koko ajan vaikka laskennallisen keskiarvokulutuksen puitteissa ja säästäminen tuntuu mukavammalta.<br><br>
Voi siis lisätä halutessaan uuden budjetin, muuttaa ja poistaa.<br />
Lisäämisessä (ja muuttamisessa) kenttinä ovat<br />
- budjetin nimi<br />
- budjetin suuruus euroina<br />
- mitä rahalähdettä käsitellään<br />
- aloituspäivämäärä<br />
- lopetuspäivämäärä<br />
<br />
Budjetti-sivun (/budget) pääsivulla on jo näytetty listaus budjeteista ja tässä näkyy myös monta päivää budjetti kattaa ja mikä on laskennallinen päiväkulutus euroina (keskiarvo).<br />

<h4>raportti: menot ja tulot</h4>
Käyttäjä saa raportit, joissa näkyy<br />
	a. kuukausittainen rahan kulutus<br />
	- oletuksena kaikki rahalähteet<br />
	- sivupaneelista voi valita myös rahalähteen perusteella<br />

<h4>raportti: saldoseuraaja</h4>
	a. saldotilanne + mikä on keskimääräinen päiväkulutus, jos budjetissa halutaan pysyä (jos budjetti on asetettu), ollaanko plussalla vai miinuksella (ja miten paljon).<br />
	c. jos käyttäjä on laittanut esim. elokuulle vain 4 saldomerkintää siinä missä toinen ahkerampi käyttäjä olisi laittanut kaikki 31 merkintää, niin laiskalle käyttäjälle raportti täyttää tyhjät kohdat automaattisesti ns. trendin mukaisilla arvoilla<br />

<h2>Tietokanta-taulut<h2>

<h4>account</h4>
Tässä on käyttäjän alias/nimi, käyttäjätunnus ja salasana*.
Tämän lisäksi myös kaksi boolean-kentää: active ja admin.<br />
Jos active = true, käyttäjä saa kirjautua. Jos admin=true käyttäjä on admin.

<h4>money_source</h4>
Rahalähteen nimi ja tarkempi kuvaus
viittaus account-tauluun account 1...n money_source

<h4>Transactions</h4>
päivittäiset menot/tulot
viittaus account-tauluun account 1...n Transactions
viittaus money_source-tauluun money_source 1...n Transactions

<h4>Saldo</h4>
Saldotilanne per päivä
viittaus account-tauluun account 1...n Saldo
viittaus money_source-tauluun money_source 1...n Saldo

<h4>budget</h4>
Budjetin tiedot, eli nimi, määrä, rahalähde, aloitus- ja lopetuspvm.<br />
viittaus account-tauluun account 1...n Saldo
viittaus money_source-tauluun money_source 1...n Saldo

<hr />
* toteutuksessa salasana on kryptattuna tietokannassa

<h3>Entity-Relationship diagrammi</h3>
DBVisualizer-ohjelmalla tehtyä ERD-diagrammia voit ihailla <a href="https://github.com/niratto/saldoseuraaja/blob/master/ERD/erd.jpg">tämän linkin</a> kautta.

<h3>Skeema</h3>

CREATE TABLE account (  
	id INTEGER NOT NULL,   
	date_created DATETIME,   
	date_modified DATETIME,   
	name VARCHAR(144) NOT NULL,   
	username VARCHAR(144) NOT NULL,   
	password VARCHAR(144) NOT NULL,   
	active BOOLEAN,   
	admin BOOLEAN,   
	PRIMARY KEY (id),   
	CHECK (active IN (0, 1)),   
	CHECK (admin IN (0, 1))  
);  
  
CREATE TABLE saldo (  
	sa_id_pk INTEGER NOT NULL,   
	sa_created DATETIME,   
	sa_modified DATETIME,   
	sa_date DATE NOT NULL,   
	sa_amount NUMERIC(10, 2) NOT NULL,   
	ms_id_fk INTEGER,   
	acc_id_fk INTEGER NOT NULL,   
	PRIMARY KEY (sa_id_pk),   
	FOREIGN KEY(ms_id_fk) REFERENCES money_source (ms_id_pk),   
	FOREIGN KEY(acc_id_fk) REFERENCES account (id)  
);  
  
CREATE TABLE budget (  
	bu_id_pk INTEGER NOT NULL,   
	bu_name VARCHAR(255) NOT NULL,   
	bu_amount NUMERIC(10, 2) NOT NULL,   
	bu_start_date DATE NOT NULL,   
	bu_end_date DATE NOT NULL,   
	bu_days_count INTEGER NOT NULL,   
	bu_avg_daily_consumption NUMERIC(10, 2) NOT NULL,   
	ms_id_fk INTEGER NOT NULL,   
	acc_id_fk INTEGER NOT NULL,   
	PRIMARY KEY (bu_id_pk),   
	FOREIGN KEY(ms_id_fk) REFERENCES money_source (ms_id_pk),   
	FOREIGN KEY(acc_id_fk) REFERENCES account (id)  
);
  
CREATE TABLE transactions (  
	tr_id_pk INTEGER NOT NULL,   
	date_created DATETIME,   
	date_modified DATETIME,   
	tr_date DATE NOT NULL,   
	tr_month INTEGER NOT NULL,   
	tr_amount NUMERIC(10, 2) NOT NULL,   
	tr_participant VARCHAR(255),   
	tr_info VARCHAR(255),   
	ms_id_fk INTEGER NOT NULL,   
	acc_id_fk INTEGER NOT NULL,   
	PRIMARY KEY (tr_id_pk),   
	FOREIGN KEY(ms_id_fk) REFERENCES money_source (ms_id_pk),   
	FOREIGN KEY(acc_id_fk) REFERENCES account (id)  
);  
  
CREATE TABLE money_source (  
	ms_id_pk INTEGER NOT NULL,   
	ms_name VARCHAR(255) NOT NULL,   
	ms_extrainfo VARCHAR(255),   
	acc_id_fk INTEGER NOT NULL,   
	PRIMARY KEY (ms_id_pk),   
	FOREIGN KEY(acc_id_fk) REFERENCES account (id)  
);  

.......

Toiminnot ja rajoitukset sivuittain:

Yleiset säännöt, jotka toistuvat sovelluksessa:
- kaikki lisäys-, muokkaus- ja poistotoimenpiteet ovat toteutettu samalla logiikalla
	- esim. toiminto ”saldo”
	- saldo/add  lisäys
	- saldo/modify/<saldon id>  muokkaus
	- saldo/remove/<saldon id>  poisto
- poistoissa käyttäjän pitää vahvistaa javascript-popup-ikkunan kautta esitettyyn ”oletko varma, että haluat poistaa …”-kysymykseen myöntävä vastaus (Chromessa ainakin OK tai Peruuta)

1. Kirjautumissivu (auth/login)

- Käyttäjätunnus ei saa olla tyhjä
- Salasana ei saa olla tyhjä
- Jos käyttäjän tunnus tai salasana ei kirjautuessa täsmää käyttäjälle näytetään asiasta virheilmoitus.
- jos ylläpitäjä on deaktivoinut käyttäjän, niin kirjautumisvaiheessa näkyy käyttäjälle virheilmoitus (tunnus ja salasana oikein)
- user-tason käyttäjä jatkaa kirjautumisen jälkeen booking/ -sivulle
- admin-tason käyttäjä jatkaa kirjautumisen jälkeen admin/ -sivulle
- jos käyttäjän käyttäjätunnuksesta löytyy sana 'evil', niin häntä ei autorisoida, vaan ohjataan sivulle index.html, jossa lukee ettei pahat pojat saa käyttää softaa
- käyttäjä voi rekisteröityä

2. Rekisteröityminen
- nimi/alias ei saa olla tyhjä
- käyttäjätunnus ei saa olla tyhjä
- salasana ei saa olla tyhjä
- vahvista salasanan tulee olla identtinen salasanan kanssa
- Jos identtinen käyttäjätunnus löytyy jo tietokannasta, niin tästä ilmoitetaan rekisteröityvälle käyttäjälle ilmoituksella
- HUOM! jos tietokannassa ei ole admin-tason käyttäjää, niin ensimmäinen rekisteröityminen on admin-tason rekisteröityminen (näitä voi tehdä vain kerran; ellei sitten tuhoa tietokantaa välissä)
- jos tietokannassa on admin-tason käyttäjä, niin rekisteröitymiset ovat user-tason rekisteröitymisiä
- admin ja user-tason käyttäjien ero tietokannassa Account-taulussa on se, että adminilla Admin-sarake on true ja käyttäjällä False

3. Admin-sivu

Admin-sivulla (kirjautuminen admin-käyttäjänä) voi
- deaktivoida käyttäjän
- nollata käyttäjän salasanan (siitä tulee käyttäjätunnus väärinpäin)
- admin-sivulla näytetään kaikki käyttäjät, joiden admin-sarake account-taulussa on false

4. booking-sivu

Tämä on sivu, jonne tulee lopulta transaktioiden, saldojen yms. lisääminen. Tällä hetkellä sivulla on
- käyttäjän tietojen muokkaaminen
- rahalähteiden raportointi, lisäys, muokkaus ja poisto
- menojen/tulojen lisäys, muokkaus, poisto
- saldon raportointi, lisäys, muokkaus, poisto
- budjetin raportointi, lisäys, muokkaus, poisto
- menojen ja tulojen kuukausittainen raportointi
	- kaikki tai per rahalähde
- saldoseurannan raportointi
	- perustuu annettuihin saldomerkintöihin ja luotuun budjettiin
	- tässä vertaillaan miten pankkitilin saldo korreloi arvioidun budjetin kanssa

Sivun oletusnäkymä on vasemmassa paneelissa linkit ym. toimintoihin ja oikeassa paneelissa kaikki menot/tulot kaikista rahalähteistä, eli transactions-taulun yhteenvetokysely. Järjestetty laskevasti päivämäärän mukaan.

5. user/edit -sivu

Tällä sivulla käyttäjä voi muokata aliastaan sekä päivittää salasanansa.
- Jos alias on tyhjä ja painetaan "muuta tietoja", niin alias ei muutu tyhjäksi, vaan vanha arvo pidetään.
- Jos salasana on tyhjä ja painetaan "muuta tietoja", niin salasana ei muutu tyhjäksi, vaan vanha arvo pidetään.
- Ym. tapauksissa ainoastaan jos kenttiin laitetaan arvoja, niin ne päivitetään tietokantaan.
- salasanojen pitää täsmätä keskenään

6. source -sivu

Täällä käyttäjä näkee omat henk. koht. rahalähteensä ja voi
- poistaa
- muokata rahalähdettä
Tämän lisäksi käyttäjä voi lisätä uuden rahalähteen (linkki: lisää rahalähde)

7.	source/add -sivu

Täällä käyttäjä voi lisätä uuden rahalähteen
- nimi ei saa olla tyhjä
- lisätietoja on valinnainen kenttä
Lisää rahalähde --> vie uuden tietueen kantaan Moneysource-tauluun

8. source/modify –sivu
Periaatteessa sama toiminta kuin source/add –sivulla, mutta tässä muokattavan rahalähteen tiedot tuodaan automaattisesti kenttiin (rahalähteen nimi, lisätietoja)

9. transactions/add –sivu

Tällä sivulla käyttäjä voi lisätä menon tai tulon per rahalähde
- päivämäärän pitää olla muodossa pp.kk.vvvv
- määrän tulee olla numeerinen arvo (desimaalit erotetaan pisteellä!)
- jos ”onko tulo”-checkbox on valittuna, niin tämä tarkoittaa että kyseessä on tulo ja se viedään transactions-tauluun positiivisena numeroarvona; muussa tapauksessa numeroarvo muutetaan automaattisesti negatiiviseksi arvoksi
- kohteessa pitää olla tekstiä
Lisäyksen jälkeen käyttäjä ohjataan /booking –sivulle. Jos ym. syötteissä on vikaa, niin käyttäjää muistutaan asiasta virheilmoituksella.

10. transaction/modify –sivu

Toimii kuten transaction/add –sivu, mutta jo aiemmin täytetyt arvot populoidaan annettuihin kenttiin.
Tälle sivulle pääsee booking-sivun kautta ( muokkaa)

11. saldo-sivu

Yhteenvetosivu, jossa näytetään kunkin rahalähteen viimeisin saldo ja kaikki saldomerkinnät.
Saldomerkintöjä voi muokata ja poistaa tämän sivun kautta.
muokkaus -> saldo/modify
poisto -> saldo/remove

12. saldo/add-sivu

Tällä sivulla annetaan saldomerkinnän päivämäärä ja rahamäärä sekä myös rahalähde.
- päivämäärän tulee olla muotoa pp.kk.vvvv
- rahamäärän tulee olla numeerinen arvo
Jos ym. validoinnit eivät mene läpi, käyttäjälle ilmoitetaan asiasta.

13. budget-sivu

Tällä sivulla näytetään kaikki tehdyt budjetit ja jokaista budjettimerkintää voi muokata (budget/modify) ja budjettimerkinnän voi myös poistaa (budget/remove)
Uuden budjetin lisäys onnistuu ”lisää uusi budjetti”-linkistä, joka ohjaa käyttäjän budget/add –sivulle.
Kenttien validoinnit:
- Budjetilla pitää olla nimi
- määrän pitää olla numeerinen arvo
- aloitus- ja lopetusmäärän pitää olla muodossa pp.kk.vvvv

14. menojen ja tulojen raportointi

Ohjaa sivulle reporting/0. Tuo nolla indikoi tässä sitä, että menot ja tulot per kuukausi näytetään koskien kaikkia rahalähteitä.
Vasemmalla sivupaneelissa on linkit jokaiseen rahalähteeseen ja niitä painamalla avautuu kuukausittainen meno/tulo-raportti koskien ko. valittua rahalähdettä.

15. Saldoseurannan raportointi

Tämä siis toimii tällä logiikalla. Oletetaan, että käyttäjällä on vaikka palkkapäivä 15.8. ja palkalla pitäisi elellä seuraavaan palkkapäivään asti, eli 15.9.. Käyttäjä saa palkkaa 2500 euroa esim. Nordean tililleen ja käyttäjä tekee budjetin välille 15.8. – 15.9.2018 ja budjetin suuruus on 2500 euroa ja budjetin rahalähteenä toimii Nordea. Käyttäjä antaa budjetilleen nimen ”elo-syys”.
Saldoseurannan raportoinnissa näkyy vasemmalla nyt elo-syys –linkki. Jos sen avaa, niin saldoseurannan raportti tulee näkyviin; budjetti ”elo-syys” vs. toteutuneet saldot.
Raportissa näkyy budjetin ”elo-syys” kaikki päivämäärät (järjestetty nousevasti päivämäärän mukaan), toteutunut saldo –sarake, jossa näkyy aikavälille annetut saldomerkinnät lihavoituna ja niille päiville mitä saldoa ei ole annettu, niin nämä arvioidaan laskutoimituksen perusteella (eli trendin mukaan). Raportilla näkyy myös ”laskettu saldo” –sarake, jossa näkyy budjetille annettu rahamäärä, eli tässä tapauksessa 2500 euroa. Sitten joka riville tulee jokaiselle päivälle laskettu saldo sillä perusteella, että budjetin viimeisenä päivänä käyttäjällä on rahaa 0 euroa.
Tästä käyttäjä voi päätellä, että miten hänen saldonsa muuttuminen korreloi lasketun saldon kanssa.
