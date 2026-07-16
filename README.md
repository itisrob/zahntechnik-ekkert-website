# Dentallabor Ekkert — Website (Rebuild)

Statischer 1:1-Rebuild von **zahntechnik-ekkert.de** (vorher Framer) als eigenständige
HTML/CSS/JS-Seite — mobile-first, DSGVO-freundlich, ohne Framer-Abhängigkeit und ohne
„Made with ❤️ by GrowPotential"-Badge. Kein Build-Schritt zum Ausliefern nötig
(reines statisches HTML → direkt GitHub-Pages-fähig).

## Seiten (12)
`index.html` · `ueber.html` · `leistungen.html` · `schoenheitsschiene.html` ·
`kunststoffschiene.html` · `implantate.html` · `zahnersatz.html` · `valplast.html` ·
`klammerprothese.html` · `impressum.html` · `datenschutz.html`
> Hinweis: Die separate `kontakt.html` wurde entfernt (identisch mit dem Terminbereich). „Kontakt"/„Termin vereinbaren" führen jetzt zum Buchungsbereich `#termin`, der auf jeder Inhaltsseite steht.

## Struktur
```
├── *.html                 # generierte Seiten (NICHT direkt editieren – siehe _build/)
├── css/style.css          # Design-System (Petrol/Cyan, Cabinet Grotesk + Lato)
├── js/main.js             # Nav, Video-/Maps-Consent, Web3Forms, Scroll-Reveal
├── assets/
│   ├── img/               # optimierte Bilder (semantisch benannt)
│   ├── fonts/             # self-gehostete woff2 (Cabinet Grotesk, Lato) – DSGVO
│   ├── favicon-*.png, apple-touch-icon.png
│   └── _framer_raw/       # Original-Framer-Assets (nur lokal, .gitignore)
├── _build/
│   ├── build.py           # Generator → erzeugt alle 12 Seiten aus Partials + Daten
│   ├── datenschutz_text.py# Datenschutz-Rechtstext
│   └── prepare_assets.sh  # Bild-Optimierung + Font-/Poster-Download
├── sitemap.xml · robots.txt · .nojekyll
```

## Bearbeiten & neu bauen
Seiteninhalte/-struktur werden **zentral** in `_build/build.py` gepflegt (Header, Footer,
Formular, SEO stehen nur an EINER Stelle). Nach Änderungen:
```bash
python3 _build/build.py        # schreibt alle 12 HTML-Seiten neu
```
Assets neu aufbereiten (nur bei neuen Bildern nötig): `bash _build/prepare_assets.sh`

## Lokal ansehen
```bash
npx http-server . -p 8793 -c-1      # dann http://localhost:8793
```

## Kontaktformular → GrowPotential-Endpoint (Resend)
Das Formular POSTet an **`app.growpotential.de/api/lead`** (Portal, `portal/api/lead.js`). Der Endpoint sendet über **Resend** zwei Mails (Anfrage an `zahntechnik-ekkert@web.de` mit Reply-To=Interessent · Bestätigung an den Interessenten), pingt Robert per Telegram und schreibt den Lead in die Kundenakte.
- Konfiguriert im HTML über `data-endpoint` + `data-client="zahntechnik-ekkert"` (in `_build/build.py`: `LEAD_ENDPOINT`, `LEAD_CLIENT`).
- **Nichts pro Website einzurichten** — neuer Kunde = ein Eintrag in `portal/lib/leadConfig.js`.
- Voraussetzung serverseitig: `RESEND_API_KEY` (Vercel-Projekt „portal") + verifizierte Domain `growpotential.de`. Doku: `wissensdatenbank/prozesse/kontaktformulare.md`.
- Fällt der Endpoint aus, zeigt das Formular eine freundliche Fehlermeldung mit E-Mail/Telefon.

## SEO / Backend (umgesetzt)
- Eigener **Title** + **Meta-Description** pro Seite (vorher: alle 12 identisch „Dentallabor Ekkert").
- **Open Graph** (Title/Description/Image/URL) + Twitter-Cards, OG-Bild `assets/img/og-cover.jpg` (1200×630).
- **JSON-LD** LocalBusiness/MedicalBusiness (Adresse, Geo, Öffnungszeiten, Telefon) + BreadcrumbList auf Leistungsseiten → lokale SEO.
- `sitemap.xml`, `robots.txt`, canonical-Tags, `lang="de"`, Favicons.

## Inhaltliche Bereinigungen (bewusst vorgenommen – bitte gegenprüfen)
- **Ansprache vereinheitlicht auf „Sie"** (Original mischte Sie/Du, u. a. im Formular „Dein Name").
- Tippfehler korrigiert: „Lassen **Sie** sich beraten!", „flexible**, **allergiefreie".
- **Öffnungszeiten überall Mo–Fr 08:00–18:00** (Original: Startseite 08–18, Leistungsseiten 9–18 – vereinheitlicht wie besprochen).
- **Adresse/PLZ vereinheitlicht: Max-Brod-Weg 14, 75175 Pforzheim** (Datenschutz nannte fälschlich 75181).
- Copyright auf **2026** (dynamisch via `data-year`, bleibt aktuell).

## Offene Punkte / bitte bestätigen
- **Namensschreibweise:** Seite/Impressum sagen „**Aleksandr** Ekkert" – du hattest „Alexander Eckert" geschrieben. Aktuell steht überall die Impressums-Variante „Aleksandr Ekkert". Bitte final festlegen (Impressum ist rechtlich relevant).
- **Datenschutz rechtlich prüfen:** Abschnitte für die genutzten Dienste (**YouTube** youtube-nocookie, **Formular-Verarbeitung** — jetzt über GrowPotential/Resend statt Web3Forms) + Hosting-Platzhalter (GitHub Pages / DPF). Google-Analytics-Abschnitt: Hinweis, dass aktuell **kein** Analytics aktiv ist. → Datenschutz-Text im Generator noch von „Web3Forms" auf „GrowPotential (Auftragsverarbeiter) + Resend" umstellen; vor Livegang von dir/Anwalt bestätigen.
- **Tracking (optional):** GA4 / Clarity / Meta-Pixel sind bewusst NICHT eingebaut (bräuchten Consent-Banner). Auf Wunsch nachrüsten (dann Datenschutz ergänzen).
- **OG-Bild:** aktuell ein gecropptes Foto (1200×630). Optional ein gebrandetes OG-Motiv mit Logo/Claim.

## 301-Redirect-Map (alte Framer-URL → neue Datei) für den Domain-Umzug
```
/Über                              → /ueber.html
/Unser-Service                     → /leistungen.html
/Unser-Service/schönheitsschiene   → /schoenheitsschiene.html
/Unser-Service/kunststoffprothesen → /kunststoffschiene.html
/Unser-Service/implantate          → /implantate.html
/Unser-Service/zahnersatz          → /zahnersatz.html
/Unser-Service/valplast            → /valplast.html
/Unser-Service/klammerprothese     → /klammerprothese.html
/Kontakt                           → /#termin  (Buchungsbereich, kein eigenes File mehr)
/Impressum                         → /impressum.html
/Datenschutz                       → /datenschutz.html
```

## Deploy (GitHub Pages → zahntechnik-ekkert.de)
1. Repo `itisrob/zahntechnik-ekkert-website`, Branch `main` als Pages-Quelle.
2. Live-Preview: `https://itisrob.github.io/zahntechnik-ekkert-website/`.

### Go-Live-Plan Domain (Stand 2026-07-14)
DNS der Domain liegt bei **AWS Route 53** (Nameserver awsdns-*). Aktuell: Apex-A-Records → Framer (35.71.142.77, 52.223.52.2), `www` → CNAME `sites.framer.app`.

Reihenfolge (erst DNS, dann CNAME-Datei — sonst leitet die github.io-Preview auf die noch-Framer-Domain um):
1. **Vorher:** Web3Forms-Key in `_build/build.py` eintragen + rebuild (Formular muss ab Tag 1 senden).
2. **Route 53** (Zugang nötig): Apex-A-Records ersetzen durch GitHub-Pages-IPs `185.199.108.153 / 185.199.109.153 / 185.199.110.153 / 185.199.111.153`; `www`-CNAME von `sites.framer.app` auf `itisrob.github.io` ändern.
3. **Repo:** Datei `CNAME` mit Inhalt `zahntechnik-ekkert.de` committen; in den Repo-Settings → Pages die Custom Domain eintragen; nach Zertifikatsausstellung „Enforce HTTPS" aktivieren.
4. **Framer:** Domain-Verknüpfung im Framer-Projekt entfernen / Site depublizieren.
5. **Nachher:** Alte URLs werden durch `404.html`-Redirect-Map aufgefangen; Google Search Console: Property bestätigen + `sitemap.xml` einreichen. Canonicals/OG zeigen bereits auf die Domain.
