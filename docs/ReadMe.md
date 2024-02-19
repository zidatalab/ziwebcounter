# Hinweise zur Integration des Zi-Webcounter in Web-Seiten

## Was ist das Ziel

Mit dem Webcounter soll ein Organisationsweites datensparsames Webmonitoring implementiert werden.

## Wie wird das System eingebungen?

Der Zi-Webcounter kann entweder durch einen Zählpixel oder per Javascript eingebunden werden. Der Projektname sollte eindeutig sein, bitte ggf. mit der IT abesprechen.

### Einbindung per Zählpixel

Beispiel Snippet für den Projehtnamen "**testprojekt**" und die Seite "**/static/sample.html**". 

```html
<img src="https://analytics.api.ziapp.de/view/testproject/counter.png?pageid=/static/sample.html&cookiedissent=true" style="border:0" alt="">
```

Die Flag "**cookiedissent=true**" führt dazu, dass kein Cookie zur eindeutigen Nutzeridentifikation gesetzt wird. Sollte ein User-identifizierender 
(pseudonymer) Cookie gesetzt werden sollen, müssen Nutzer:innen dem zustimmen. Aus Sicht der IT ist dies nicht notwendig, da auch ohne Cookie eine Nutzerdifferenzierung möglich ist (s.u.).

Bei der Einbindung per Zählpixel muss auf jeder Seite eine Anpassung der "pageid" erfolgen, um Seitenzugriffe differenzieren zu können.

### Einbindung per Javascript Snippet

```javascript
<script type="text/javascript">
// Put your values here:
let trackerurl = 'https://analytics.api.ziapp.de/view/';
let sitename = "testproject"

// Do not change anything below this line
// ======================================
let docName = window.location.pathname;
let thequery = trackerurl + sitename + '/data?pageid=' + docName + "&cookiedissent=true";
// Execute Request 
const Http = new XMLHttpRequest();
Http.open("GET", thequery);
Http.withCredentials = true;
Http.send();
</script>
```

## Was ist auszuwerten?

Auswertbar sind die Zahl der pro Nutzer:in aufgerufenen Seiten und die Zahl der Nutzer, die die Webseite nutzen. Nutzer werden über die Kombination aus IP-Adresse und Browser-String identifiziert. 
Ändert sich der Browser oder die IP-Adresse wird ein neuer Nutzer gezählt. Die IP-Adresse wird nur zur erstellung des Nutzerpseudonyms verarbeitet und nicht gespeichert. Die IP-Adresse kann durch das Zi nicht im Nachhinnein rekonstruiert werden. 
Es wird allerdings vermerkt, ob der Zugriff von einer Zi-eigenen IP-Adresse erfolgt (Ja/Nein-Flag).

Exemplarische Auswertedaten:
```
uid: 4eef7ff3
pageid: /static/sample.html
time: 2022-01-04 06:50:23.907
ref: https://www.testentestentesten.de/
lang: en-US,en;q=0.5
Datum: 2022-01-04
siteid: testproject
```


