# Dentallabor Ekkert — Website (Rebuild)

Statischer 1:1-Rebuild von **zahntechnik-ekkert.de** (vorher Framer) als eigenständige
HTML/CSS/JS-Seite — mobile-first, DSGVO-freundlich, ohne Framer-Abhängigkeit und ohne
„Made with ❤️ by GrowPotential"-Badge. Kein Build-Schritt zum Ausliefern nötig
(reines statisches HTML → direkt GitHub-Pages-fähig).

## Seiten (12)
`index.html` · `ueber.html` · `leistungen.html` · `schoenheitsschiene.html` ·
`kunststoffschiene.html` · `implantate.html` · `zahnersatz.html` · `valplast.html` ·
`klammerprothese.html` · `kontakt.html` · `impressum.html` · `datenschutz.html`

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

## ⚠️ EINE Aktion nötig, damit das Kontaktformular live Mails sendet
Das Formular nutzt **Web3Forms** (kein Server nötig, Zustellung an `zahntechnik-ekkert@web.de`):
1. Auf **web3forms.com** die E-Mail `zahntechnik-ekkert@web.de` eintragen → Access Key kommt per Mail (dort bestätigen).
2. In `_build/build.py` die Zeile `WEB3FORMS_KEY = "YOUR_WEB3FORMS_ACCESS_KEY"` durch den echten Key ersetzen.
3. `python3 _build/build.py` → fertig.
Bis dahin zeigt das Formular eine freundliche Fallback-Meldung mit E-Mail/Telefon (kein stiller Fehler).

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
- **Datenschutz rechtlich prüfen:** Ich habe Abschnitte für die neuen Dienste ergänzt (**YouTube** youtube-nocookie, **Web3Forms**) und einen Hosting-Platzhalter (z. B. GitHub Pages / DPF). Google-Analytics-Abschnitt: Hinweis, dass aktuell **kein** Analytics aktiv ist. → vor Livegang von dir/Anwalt bestätigen.
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
/Kontakt                           → /kontakt.html
/Impressum                         → /impressum.html
/Datenschutz                       → /datenschutz.html
```

## Deploy (GitHub Pages → später zahntechnik-ekkert.de)
1. Repo `itisrob/zahntechnik-ekkert-website`, Branch `main` als Pages-Quelle.
2. Live-Preview: `https://itisrob.github.io/zahntechnik-ekkert-website/`.
3. Domain-Umzug: `CNAME`-Datei mit `zahntechnik-ekkert.de` anlegen, DNS umstellen, 301-Redirects (oben) setzen, alte Framer-Seite abschalten.
