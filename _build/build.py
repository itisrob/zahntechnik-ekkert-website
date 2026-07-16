#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static site generator for Dentallabor Ekkert (zahntechnik-ekkert.de rebuild).
Rebuilt to faithfully match the original Framer template + client fixes.
Run:  python3 _build/build.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://zahntechnik-ekkert.de"

# ---------------------------------------------------------------------------
BIZ = {
    "name": "Dentallabor Ekkert",
    "legal": "Zahntechnik Aleksandr Ekkert",
    "owner": "Aleksandr Ekkert",
    "role": "Dentaltechniker",
    "street": "Max-Brod-Weg 14",
    "zip": "75175",
    "city": "Pforzheim",
    "phone_display": "+49 1515 7916602",
    "phone_href": "+4915157916602",
    "email": "zahntechnik-ekkert@web.de",
    "lat": "48.881310409690556",
    "lng": "8.706356762138205",
    "hours_short": "Mo–Fr 08:00–18:00 Uhr",
}
MAP_EMBED = "https://maps.google.com/maps?q=%s,%s&z=15&output=embed" % (BIZ["lat"], BIZ["lng"])
YT_ID = "PwmMA5fmEe4"
# Kontaktformular → GrowPotential-Endpoint (Resend + Telegram + Kundenakte). Siehe portal/api/lead.js
LEAD_ENDPOINT = "https://app.growpotential.de/api/submit"
LEAD_CLIENT = "zahntechnik-ekkert"

def _svg(p, vb="0 0 24 24", w="2"):
    return ('<svg viewBox="%s" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (vb, w, p))

IC = {
    "pin": _svg('<path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/>'),
    "clock": _svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "phone": _svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>'),
    "mail": _svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    "arrow": _svg('<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>'),
    "arrowc": _svg('<circle cx="12" cy="12" r="9"/><path d="M10 8l4 4-4 4"/>'),
    "play": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>',
    "cal": _svg('<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>'),
    "check": _svg('<path d="M20 6 9 17l-5-5"/>', w="2.4"),
    "star": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l3 6.5 7 .9-5 4.9 1.2 7L12 18l-6.4 3.3L6.9 14 2 9.4l7-.9z"/></svg>',
    "shield": _svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>'),
}

# service tile icons (white stroke on cyan tile)
SVC_ICONS = {
    # bright smile / Hollywood → sparkle
    "schoenheitsschiene": _svg('<path d="M12 2.5l1.9 5.1 5.1 1.9-5.1 1.9L12 16.5l-1.9-5.1L5 9.5l5.1-1.5z"/><path d="M18.4 14.6l.6 1.7 1.7.6-1.7.6-.6 1.7-.6-1.7-1.7-.6 1.7-.6z"/>', w="1.5"),
    # aligner / tray
    "kunststoffschiene": _svg('<path d="M4.6 8.6c0 6.4 3 9.4 7.4 9.4s7.4-3 7.4-9.4"/><path d="M4.6 8.6C4.6 6.8 7.9 5.7 12 5.7s7.4 1.1 7.4 2.9"/><path d="M7.6 9.4c2.9.7 5.9.7 8.8 0"/>', w="1.6"),
    # dental implant (crown + threaded post)
    "implantate": _svg('<path d="M9.7 4.6h4.6l-.5 3.1h-3.6z"/><path d="M10 8.7h4l-.6 8.3a1.4 1.4 0 0 1-2.8 0z"/><path d="M10.4 11.2h3.2M10.6 13.7h2.8"/>', w="1.6"),
    # crown
    "zahnersatz": _svg('<path d="M3.5 9.5 7 12l5-6 5 6 3.5-2.5-1.7 9.5H5.2z"/>', w="1.6"),
    # flexible partial → single tooth silhouette
    "valplast": _svg('<path d="M12 4.2c-2.1-1.5-4.4-1.1-5.8.2C4.6 5.9 4.6 8.4 5.6 11.3c.7 2.1.6 5.7 2.2 5.7 1.3 0 1.1-2.7 2.2-2.7s.9 2.7 2.2 2.7c1.6 0 1.5-3.6 2.2-5.7 1-2.9 1-5.4-.6-6.9C16.4 3.1 14.1 2.7 12 4.2Z"/>', w="1.6"),
    # partial denture with clasp
    "klammerprothese": _svg('<path d="M9 4.2C6.8 4.2 5.6 6 5.6 8.2c0 2.6.3 6.4 1.9 6.4 1.1 0 1-2.1 1.9-2.1s.8 2.1 1.9 2.1c1.6 0 1.9-3.8 1.9-6.4C13.1 6 11.2 4.2 9 4.2"/><path d="M14 8c2.1 0 3.4 1.6 3.4 4S16.1 16 14 16"/>', w="1.6"),
}

BENEFITS = [
    ("Höchste Qualität und Präzision", "Ich fertige Ihre Prothesen und Zahnersatzlösungen mit modernster CAD-Technologie, um eine perfekte Passform und Langlebigkeit zu gewährleisten."),
    ("Komfort und Ästhetik", "Im Labor verwende ich hochwertige, biokompatible Materialien, die nicht nur allergiefrei sind, sondern auch für höchsten Tragekomfort und eine natürliche Optik sorgen."),
    ("Individuelle Beratung und Betreuung", "Sie erhalten von mir eine umfassende, individuelle Beratung, um die bestmögliche Lösung für Ihre Bedürfnisse zu finden und langfristig zufrieden zu sein."),
]

SERVICES = [
    {"slug": "schoenheitsschiene", "file": "schoenheitsschiene.html", "name": "Hollywood-Schönheitsschiene", "short": "Hollywood-Schönheitsschiene",
     "card": "Zahnfarbige Schönheitsschienen in verschiedenen Farbnuancen korrigieren Zahnfehlstellungen unauffällig und passen sich harmonisch Ihrer Zahnfarbe an.",
     "hero_img": "schiene-hero.png", "detail_img": "schiene-detail.png",
     "intro": "Erfahren Sie die Vorteile der zahnfarbigen Schönheitsschienen:",
     "bullets": [("Ästhetische Vielfalt", "Die Schönheitsschienen sind in verschiedenen Farben erhältlich, um Ihren persönlichen Vorlieben und ästhetischen Bedürfnissen gerecht zu werden."),
                 ("Effektive Korrektur", "Die Schienen bieten eine effektive Lösung für Zahnfehlstellungen, um Ihr Lächeln wieder zu voller Schönheit zu bringen."),
                 ("Komfortable Anwendung", "Die Schönheitsschienen sind angenehm zu tragen und ermöglichen eine einfache Anpassung an Ihre individuelle Mundstruktur.")],
     "engagement": "Ich verstehe, dass jeder Patient einzigartige ästhetische Anliegen hat. Ich stehe Ihnen zur Seite, um Ihnen eine individuelle Beratung und Behandlung zu bieten, die auf Ihre spezifischen Bedürfnisse zugeschnitten sind. Ihre Zufriedenheit und Ihr Wohlbefinden sind mein oberstes Ziel.",
     "has_video": True},
    {"slug": "kunststoffschiene", "file": "kunststoffschiene.html", "name": "Kunststoffschiene", "short": "Kunststoffschiene",
     "card": "Schienen aus speziellem Kunststoff mit weicher Innenseite bieten höchsten Tragekomfort und eine ästhetisch ansprechende Optik.",
     "hero_img": "kunststoff-hero.jpg", "detail_img": "kunststoff-detail.png",
     "intro": "Entdecken Sie die Vorteile meiner allergiefreien Kunststoffschienen:",
     "bullets": [("Natürliche Ästhetik", "Die Schienen überzeugen durch ihre natürliche Optik und tragen dazu bei, Ihr Lächeln wieder zu voller Schönheit zu bringen."),
                 ("Komfortables Tragegefühl", "Die weichen Innenseiten sorgen für ein angenehmes Tragegefühl und minimieren mögliche Unannehmlichkeiten."),
                 ("Langfristige Haltbarkeit", "Dank modernster Materialien und Technologien bieten die Schienen eine langfristige und zuverlässige Lösung für Ihre Bedürfnisse.")],
     "engagement": "Ich bin bestrebt, Ihnen nicht nur hochwertige Produkte anzubieten, sondern auch einen erstklassigen Service. Ich stehe Ihnen zur Seite, um Ihre individuellen Bedürfnisse zu verstehen und Ihnen die bestmögliche Lösung zu bieten. Ihre Zufriedenheit steht bei mir an erster Stelle, und ich setze alles daran, Ihnen ein strahlendes Lächeln zu schenken."},
    {"slug": "implantate", "file": "implantate.html", "name": "Implantate", "short": "Implantate",
     "card": "Implantate bieten eine dauerhafte, stabile Lösung für Zahnersatz und sorgen für ein natürliches Aussehen sowie optimale Kaufunktion.",
     "hero_img": "implantate-hero.jpg", "detail_img": None,
     "intro": "Erfahren Sie die Vorteile der Implantatlösungen:",
     "bullets": [("Permanente Lösung", "Eine dauerhafte Lösung für fehlende Zähne, die sich wie natürliche Zähne anfühlen und aussehen."),
                 ("Natürliche Ästhetik", "Sie werden sorgfältig an Ihre individuelle Mundstruktur angepasst, um eine natürliche Ästhetik zu gewährleisten."),
                 ("Verbesserte Funktionalität", "Ermöglichen eine verbesserte Kaukraft und Sprachfunktion, damit Sie wieder unbeschwert essen, sprechen und lachen können.")],
     "engagement": "Ich lege großen Wert darauf, dass die Implantatarbeit ein Erfolg wird und stehe Ihnen zur Seite, um eine umfassende Beratung bieten zu können, die auf Ihre individuellen Bedürfnisse zugeschnitten ist. Ihre Zufriedenheit und Ihr Wohlbefinden sind mein oberstes Ziel."},
    {"slug": "zahnersatz", "file": "zahnersatz.html", "name": "Zahnersatz", "short": "Zahnersatz",
     "card": "Hochwertiger Zahnersatz aus Kronen und Brücken, gefertigt mit CAD-Unterstützung, garantiert präzise Passform und langlebige Ästhetik.",
     "hero_img": "zahnersatz-hero.jpg", "detail_img": None,
     "intro": "Entdecken Sie die Vielfalt der Zahnersatzlösungen:",
     "bullets": [("Präzise Passform", "Dank der CAD-Unterstützung garantiere ich Ihnen eine präzise Passform und ein optimales Ergebnis."),
                 ("Ästhetische Vielfalt", "Von Vollkeramik bis Metallkeramik biete ich Ihnen eine breite Palette an Materialien und Farben, um Ihren individuellen ästhetischen Ansprüchen gerecht zu werden."),
                 ("Langlebige Qualität", "Meine Zahnersatzlösungen zeichnen sich durch ihre Langlebigkeit und Zuverlässigkeit aus, damit Sie sich wieder unbeschwert Ihrem Alltag widmen können.")],
     "engagement": "Ich lege großen Wert darauf, dass Ihre Bedürfnisse und Erwartungen erfüllt werden. Ich stehe Ihnen zur Seite, um Ihnen eine persönliche Beratung zu bieten und sicherzustellen, dass Sie mit Ihrem Zahnersatz vollkommen zufrieden sind."},
    {"slug": "valplast", "file": "valplast.html", "name": "Valplast", "short": "Valplast",
     "card": "Valplast-Prothesen sind flexible, allergiefreie und biokompatible Teilprothesen, die hohen Tragekomfort und eine nahezu unsichtbare Optik bieten.",
     "hero_img": "valplast-hero.jpg", "detail_img": None,
     "intro": "Erfahren Sie die Vorteile meiner Valplast-Prothesen:",
     "bullets": [("Flexibilität und Komfort", "Die Valplast-Prothesen passen sich flexibel an Ihre Mundstruktur an und bieten Ihnen ein angenehmes Tragegefühl ohne Druckstellen."),
                 ("Natürliche Ästhetik", "Die transluzente Eigenschaft von Valplast sorgt für eine natürliche Ästhetik, die Ihr Lächeln wieder zum Strahlen bringt."),
                 ("Langlebige Lösungen", "Dank der hochwertigen Materialien und Technologien bieten die Valplast-Prothesen eine langanhaltende und zuverlässige Lösung für Ihren Zahnersatz.")],
     "engagement": "Ich stehe Ihnen nicht nur bei der Auswahl Ihrer Prothese zur Seite, sondern begleite Sie auch während des gesamten Prozesses, um sicherzustellen, dass Ihre Bedürfnisse und Erwartungen erfüllt werden."},
    {"slug": "klammerprothese", "file": "klammerprothese.html", "name": "Klammerprothese", "short": "Klammerprothese",
     "card": "Klammerprothesen bieten eine kostengünstige Möglichkeit, einzelne Zahnlücken zu schließen und Funktion sowie Ästhetik des Gebisses wiederherzustellen.",
     "hero_img": "klammer-hero.jpg", "detail_img": None,
     "intro": "Erfahren Sie die Vorteile der Klammerprothesen:",
     "bullets": [("Gezielte Behandlung", "Die Klammerprothese ist eine kostengünstige Option, um gezielt einzelne Zähne zu ersetzen und größere Zahnlücken zu schließen."),
                 ("Ästhetische Verbesserung", "Die maßgeschneiderten Prothesen bieten eine natürliche Ästhetik, die Ihr Lächeln wieder vervollständigt und Ihnen neues Selbstbewusstsein schenkt."),
                 ("Bezahlbare Lösung", "Eine Klammerprothese ist eine kostengünstige Alternative zu anderen Zahnersatzoptionen, ohne Kompromisse bei Qualität und Komfort einzugehen.")],
     "engagement": "Ich stehe Ihnen nicht nur bei der Auswahl Ihrer Prothese zur Seite, sondern begleite Sie auch während des gesamten Prozesses, um sicherzustellen, dass Ihre Bedürfnisse und Erwartungen erfüllt werden."},
]

NAV = [("Home", "index.html"), ("Über mich", "ueber.html"), ("Leistungen", "leistungen.html")]

def esc(s):
    return (s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;"))

# ---------------------------------------------------------------------------
def jsonld():
    data = {
        "@context": "https://schema.org", "@type": ["LocalBusiness", "MedicalBusiness"],
        "name": BIZ["name"],
        "description": "Zahntechnik-Labor in Pforzheim für hochwertigen, maßgeschneiderten Zahnersatz – Hollywood-Schönheitsschiene, Kunststoffschiene, Implantate, Zahnersatz, Valplast und Klammerprothese.",
        "url": BASE + "/", "image": BASE + "/assets/img/og-cover.jpg", "logo": BASE + "/assets/img/logo.png",
        "telephone": BIZ["phone_display"], "email": BIZ["email"], "priceRange": "€€",
        "address": {"@type": "PostalAddress", "streetAddress": BIZ["street"], "postalCode": BIZ["zip"], "addressLocality": BIZ["city"], "addressCountry": "DE"},
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        "areaServed": {"@type": "City", "name": "Pforzheim"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
        "founder": {"@type": "Person", "name": BIZ["owner"], "jobTitle": BIZ["role"]},
    }
    return '<script type="application/ld+json">%s</script>' % json.dumps(data, ensure_ascii=False)

def head(title, desc, slug, extra_ld=""):
    canonical = BASE + "/" + ("" if slug == "index.html" else slug)
    og_img = BASE + "/assets/img/og-cover.jpg"
    return """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=" js";</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#073e44">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{name}">
<meta property="og:locale" content="de_DE">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{name} – Zahntechnik in Pforzheim">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">
<link rel="preload" href="assets/fonts/cabinet-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/lato-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/style.css?v=4">
{ld}{extra_ld}
</head>
<body>
<a class="skip-link" href="#main">Zum Inhalt springen</a>
""".format(title=esc(title), desc=esc(desc), canonical=canonical, name=BIZ["name"], og_img=og_img, ld=jsonld(), extra_ld=extra_ld)

def header(active, termin):
    links = "".join('<li><a href="{f}"{cur}>{l}</a></li>'.format(f=f, l=l, cur=' aria-current="page"' if f == active else "") for l, f in NAV)
    mlinks = "".join('<a href="{f}"{cur}>{l}</a>'.format(f=f, l=l, cur=' aria-current="page"' if f == active else "") for l, f in NAV)
    return """<header class="site-header">
  <div class="container nav">
    <a class="brand" href="index.html" aria-label="{name} – Startseite"><img src="assets/img/logo.png" alt="" width="40" height="40"><span>{name}</span></a>
    <nav aria-label="Hauptnavigation"><ul class="nav-links">{links}</ul></nav>
    <div class="nav-cta">
      <a class="btn btn--primary" href="{termin}">Termin vereinbaren</a>
      <button class="burger" aria-label="Menü öffnen" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div class="nav-mobile" id="mnav"><ul>{mlinks}</ul><a class="btn btn--primary" href="{termin}">Termin vereinbaren</a></div>
</header>
""".format(name=BIZ["name"], links=links, mlinks=mlinks, termin=termin)

def info_strip():
    return """<div class="reveal trust">
  <div class="trust__item"><span class="trust__ico">{pin}</span><span><span class="trust__k">Adresse</span><span class="trust__v">{street}, {city}</span></span></div>
  <div class="trust__item"><span class="trust__ico">{clock}</span><span><span class="trust__k">Öffnungszeiten</span><span class="trust__v">{hours}</span></span></div>
  <div class="trust__item"><span class="trust__ico">{phone}</span><span><span class="trust__k">Anruf & Beratung</span><span class="trust__v"><a href="tel:{ph}">{phd}</a></span></span></div>
</div>""".format(pin=IC["pin"], clock=IC["clock"], phone=IC["phone"], street=BIZ["street"], city=BIZ["city"], hours=BIZ["hours_short"], ph=BIZ["phone_href"], phd=BIZ["phone_display"])

def service_icon_cards(items):
    out = []
    for s in items:
        out.append("""<a class="icard reveal" href="{f}">
  <span class="icard__ico">{ico}</span>
  <h3>{name}</h3>
  <p>{desc}</p>
  <span class="icard__link">Mehr erfahren {arrow}</span>
</a>""".format(f=s["file"], ico=SVC_ICONS[s["slug"]], name=s["name"], desc=s["card"], arrow=IC["arrowc"]))
    return '<div class="icards">%s</div>' % "".join(out)

def contact_form(page_label):
    return """<form class="form" data-lead data-endpoint="{endpoint}" data-client="{slug}">
  <div class="form__msg" role="status" aria-live="polite"></div>
  <input type="checkbox" name="botcheck" class="skip-link" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="field"><label for="f-name">Ihr Name</label><input id="f-name" type="text" name="name" placeholder="Vor- und Nachname" required></div>
  <div class="field"><label for="f-mail">Ihre E-Mail</label><input id="f-mail" type="email" name="email" placeholder="name@beispiel.de" required></div>
  <div class="field"><label for="f-tel">Telefonnummer <span class="muted">(optional)</span></label><input id="f-tel" type="tel" name="telefon" placeholder="Für einen schnellen Rückruf" autocomplete="tel"></div>
  <div class="field"><label for="f-msg">Wie kann ich Ihnen helfen?</label><textarea id="f-msg" name="nachricht" placeholder="Ihr Anliegen, gewünschte Leistung oder Wunschtermin …" required></textarea></div>
  <input type="hidden" name="seite" value="{page}">
  <p class="form__note">Mit dem Absenden stimmen Sie der Verarbeitung Ihrer Angaben gemäß <a href="datenschutz.html">Datenschutzerklärung</a> zu.</p>
  <button class="btn btn--primary btn--block btn--lg" type="submit">Anfrage senden {arrow}</button>
</form>""".format(endpoint=LEAD_ENDPOINT, slug=LEAD_CLIENT, page=esc(page_label), arrow=IC["arrow"])

def booking_block(page_label):
    return """<section class="section section--tint" id="termin">
  <div class="container">
    <div class="sec-head center reveal"><span class="eyebrow">Kontaktieren Sie uns</span><h2>Buchen Sie einen Termin</h2><p class="lead">Nachdem Sie das Formular ausgefüllt haben, melde ich mich innerhalb von 24 Stunden persönlich bei Ihnen.</p></div>
    <div class="contact-grid">
      <div class="reveal">
        <ul class="info-list">
          <li><span class="trust__ico">{phone}</span><span class="info-list__txt"><span class="trust__k">Telefon</span><span class="trust__v"><a href="tel:{ph}">{phd}</a></span></span></li>
          <li><span class="trust__ico">{mail}</span><span class="info-list__txt"><span class="trust__k">E-Mail</span><span class="trust__v"><a href="mailto:{em}">{em}</a></span></span></li>
          <li><span class="trust__ico">{pin}</span><span class="info-list__txt"><span class="trust__k">Adresse</span><span class="trust__v">{street}, {zip} {city}</span></span></li>
          <li><span class="trust__ico">{clock}</span><span class="info-list__txt"><span class="trust__k">Öffnungszeiten</span><span class="trust__v">{hours}</span></span></li>
        </ul>
        <div class="map" data-map="{map}"><div class="map__consent" role="button" tabindex="0" aria-label="Google Maps laden"><div><p>Zum Schutz Ihrer Daten wird die Karte erst nach Ihrer Zustimmung von Google Maps geladen.</p><span class="btn btn--ghost">{pin} Karte anzeigen</span></div></div></div>
      </div>
      <div class="reveal">{form}</div>
    </div>
  </div>
</section>""".format(phone=IC["phone"], mail=IC["mail"], pin=IC["pin"], clock=IC["clock"], ph=BIZ["phone_href"], phd=BIZ["phone_display"], em=BIZ["email"], street=BIZ["street"], zip=BIZ["zip"], city=BIZ["city"], hours=BIZ["hours_short"], map=MAP_EMBED, form=contact_form(page_label))

def hours_card():
    days = [("Montag", "08:00 – 18:00 Uhr", False), ("Dienstag", "08:00 – 18:00 Uhr", False), ("Mittwoch", "08:00 – 18:00 Uhr", False),
            ("Donnerstag", "08:00 – 18:00 Uhr", False), ("Freitag", "08:00 – 18:00 Uhr", False), ("Samstag", "Geschlossen", True), ("Sonntag", "Geschlossen", True)]
    rows = "".join('<div class="hours__row{c}"><span>{d}</span><span>{h}</span></div>'.format(c=" is-closed" if cl else "", d=d, h=h) for d, h, cl in days)
    return '<div class="hours reveal"><h3><span class="ico-sm">{clock}</span> Meine Arbeitszeiten</h3>{rows}</div>'.format(clock=IC["clock"], rows=rows)

def footer(termin):
    svc_links = "".join('<li><a href="{f}">{n}</a></li>'.format(f=s["file"], n=s["short"]) for s in SERVICES)
    return """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="index.html"><img src="assets/img/logo.png" alt="" width="40" height="40"><span>{name}</span></a>
        <p>{legal} – Ihr Partner für hochwertigen und maßgeschneiderten Zahnersatz. Für ein strahlendes Lächeln und mehr Lebensqualität.</p>
        <p class="footer-contact"><a href="tel:{ph}">{phd}</a><br><a href="mailto:{em}">{em}</a></p>
      </div>
      <div class="footer-col">
        <h4>Navigation</h4>
        <ul><li><a href="index.html">Home</a></li><li><a href="ueber.html">Über mich</a></li><li><a href="leistungen.html">Leistungen</a></li><li><a href="{termin}">Termin vereinbaren</a></li></ul>
      </div>
      <div class="footer-col">
        <h4>Leistungen</h4>
        <ul>{svc}</ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Copyright © <span data-year>2026</span> {name}</p>
      <nav class="footer-legal" aria-label="Rechtliches"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></nav>
    </div>
  </div>
</footer>
<div class="mobilebar"><a class="btn btn--ghost" href="tel:{ph}">{phone} Anrufen</a><a class="btn btn--primary" href="{termin}">{cal} Termin</a></div>
<script src="js/main.js?v=4" defer></script>
</body>
</html>""".format(name=BIZ["name"], legal=BIZ["legal"], svc=svc_links, ph=BIZ["phone_href"], phd=BIZ["phone_display"], em=BIZ["email"], phone=IC["phone"], cal=IC["cal"], termin=termin)

def video_facade():
    return """<div class="video reveal" data-yt="{id}" data-title="Snap on Smile – Hollywood-Schönheitsschiene" role="button" tabindex="0" aria-label="Video abspielen: Snap on Smile">
  <img src="assets/img/video-poster.jpg" alt="Video: Snap on Smile – die Hollywood-Schönheitsschiene erklärt" loading="lazy" width="1280" height="720">
  <span class="video__btn"><span class="video__play">{play}</span></span>
</div>
<p class="video__cap">Video: „Snap on Smile" – die Hollywood-Schönheitsschiene im Überblick</p>""".format(id=YT_ID, play=IC["play"])

# ---------------------------------------------------------------------------
def page_index():
    t = "Dentallabor Ekkert Pforzheim – Zahnersatz & Zahntechnik-Labor"
    d = "Ihr Zahntechnik-Labor in Pforzheim: maßgeschneiderter Zahnersatz, Hollywood-Schönheitsschiene, Implantate & mehr. Modernste CAD-Technik, persönliche Beratung – für Ihr strahlendes Lächeln."
    benefits = "".join('<div class="bpt reveal"><h3>{h}</h3><p>{p}</p></div>'.format(h=h, p=p) for h, p in BENEFITS)
    return "".join([
        head(t, d, "index.html"), header("index.html", "kontakt.html"), '<main id="main">',
        # HERO
        """<section class="hero">
  <span class="hero__glow" aria-hidden="true"></span>
  <div class="container">
    <div class="hero__grid">
      <div class="hero__copy reveal">
        <span class="eyebrow">Verändern Sie Ihr Leben mit einem Lächeln</span>
        <h1>Verleihen Sie Ihrem Lächeln neuen Glanz.</h1>
        <p class="hero__sub">Hochwertige zahntechnische Lösungen, maßgeschneidert für Ihre Bedürfnisse – gefertigt mit Präzision und persönlicher Betreuung in Pforzheim.</p>
        <div class="hero__cta"><a class="btn btn--primary btn--lg" href="kontakt.html">Lassen Sie sich beraten! {arrow}</a><a class="btn btn--ghost btn--lg" href="leistungen.html">Meine Leistungen</a></div>
      </div>
      <div class="hero__media reveal">
        <img src="assets/img/hero.png" alt="Strahlendes Lächeln – hochwertiger Zahnersatz vom Dentallabor Ekkert" width="816" height="1456" fetchpriority="high">
        <div class="hero-badge hero-badge--tl"><span class="hero-badge__ico">{star}</span><span><strong>100 %</strong><small>Präzision</small></span></div>
        <div class="hero-badge hero-badge--br"><span class="hero-badge__ico">{shield}</span><span><strong>+20 Jahre</strong><small>Erfahrung</small></span></div>
      </div>
    </div>
    {strip}
  </div>
</section>""".format(arrow=IC["arrow"], star=IC["star"], shield=IC["shield"], strip=info_strip()),
        # SERVICES (icons)
        """<section class="section">
  <div class="container">
    <div class="sec-head center reveal"><span class="eyebrow">Professionell und persönlich</span><h2>Profitieren Sie von meinem Service</h2><p class="lead">Mit persönlichem Service ist es mein Ziel, dass Sie von einem gesunden und schönen Lächeln profitieren, das Ihr Leben bereichert.</p></div>
    {cards}
    <div class="center" style="margin-top:2.6rem"><a class="btn btn--primary btn--lg" href="leistungen.html">Alle Services {arrow}</a></div>
  </div>
</section>""".format(cards=service_icon_cards(SERVICES[:3]), arrow=IC["arrow"]),
        # WARUM ICH (text + Alexander photo)
        """<section class="section section--tint">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Ihre Vorteile</span><h2>Warum Ich?</h2>
        <p class="lead">Als erfahrener Zahntechniker biete ich Ihnen maßgeschneiderte Lösungen für Ihren Zahnersatz.</p>
        <div class="benefit-list">{benefits}</div>
      </div>
      <div class="split__media reveal"><img src="assets/img/svc-schoenheitsschiene.jpg" alt="Aleksandr Ekkert bei der individuellen Beratung im Dentallabor Ekkert" loading="lazy"></div>
    </div>
  </div>
</section>""".format(benefits=benefits),
        # MODERNSTE GERÄTE (cyan band)
        """<section class="section section--cyan">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Höchste Präzision</span><h2>Modernste Geräte und höchste Präzision für Ihren Zahnersatz</h2>
        <p class="lead">Mit modernster Technologie und höchster Präzision sorge ich dafür, dass Ihr Zahnersatz perfekt passt und von bester Qualität ist.</p>
        <div class="grid-2" style="margin-top:1.6rem;gap:1.6rem">
          <div class="bpt"><h3>Perfekte Passgenauigkeit</h3><p>Dank hochmoderner Technologie fertige ich Ihren Zahnersatz exakt auf Ihre individuellen Bedürfnisse abgestimmt.</p></div>
          <div class="bpt"><h3>Langlebige Qualität</h3><p>Durch fortschrittliche Geräte und Materialien gewährleiste ich langlebigen Zahnersatz, der funktional und ästhetisch überzeugt.</p></div>
        </div>
      </div>
      <div class="split__media reveal"><img src="assets/img/svc-kunststoffschiene.jpg" alt="Aleksandr Ekkert am Dental-Mikroskop – modernste Geräte im Labor" loading="lazy"></div>
    </div>
  </div>
</section>""",
        # ÜBER MICH (text + profile card)
        """<section class="section">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Erfahrung & Skill</span><h2>Über mich</h2>
        <p>Meine Leidenschaft für die Zahntechnik entstand aus dem Wunsch, Menschen zu einem schönen und gesunden Lächeln zu verhelfen. Ich bin überzeugt, dass ein gesundes Lächeln das Wohlbefinden und die Lebensqualität erheblich steigert.</p>
        <p>Mit Hingabe und Präzision arbeite ich daran, Ihren individuellen Zahnersatz zu fertigen, der sowohl funktional als auch ästhetisch überzeugt.</p>
        <a class="btn btn--ghost" href="ueber.html" style="margin-top:.6rem">Mehr über mich {arrow}</a>
      </div>
      <div class="reveal profile"><img src="assets/img/svc-implantate.jpg" alt="Aleksandr Ekkert, Dentaltechniker im Dentallabor Ekkert Pforzheim"><div class="profile__name"><strong>{owner}</strong><span>{role}</span></div></div>
    </div>
  </div>
</section>""".format(arrow=IC["arrow"], owner=BIZ["owner"], role=BIZ["role"]),
        booking_block("Startseite"), '</main>', footer("kontakt.html"),
    ])

def page_ueber():
    t = "Über mich – Aleksandr Ekkert, Zahntechniker in Pforzheim | Dentallabor Ekkert"
    d = "Seit über 20 Jahren fertige ich mit Hingabe hochwertigen, ästhetischen Zahnersatz. Lernen Sie Aleksandr Ekkert und das Dentallabor Ekkert in Pforzheim kennen."
    stats = [("+20 J.", "Erfahrung"), ("100 %", "Präzision"), ("+1000", "Lächeln")]
    stat_html = "".join('<div class="reveal"><div class="stat__n">{n}</div><div class="stat__l">{l}</div></div>'.format(n=n, l=l) for n, l in stats)
    return "".join([
        head(t, d, "ueber.html"), header("ueber.html", "kontakt.html"), '<main id="main">',
        """<section class="page-hero">
  <div class="container">
    <div class="split">
      <div class="reveal"><span class="eyebrow">Über meinen Service</span><h1>Die Expertise, der Sie vertrauen können.</h1></div>
      <div class="reveal"><p class="lead">Seit über 20 Jahren biete ich Ihnen fachkundige Zahntechnik auf höchstem Niveau. Vertrauen Sie auf meine langjährige Erfahrung und Leidenschaft für detailgenaue, ästhetisch ansprechende Lösungen – gemeinsam erreichen wir das beste Ergebnis für Ihr schönstes Lächeln.</p><a class="btn btn--primary" href="kontakt.html">Kennenlernen {arrow}</a></div>
    </div>
  </div>
</section>""".format(arrow=IC["arrow"]),
        # gallery
        """<section class="section" style="padding-top:0">
  <div class="container">
    <div class="gallery reveal">
      <img src="assets/img/svc-schoenheitsschiene.jpg" alt="Aleksandr Ekkert bei der Beratung">
      <img src="assets/img/ueber-1.jpg" alt="Aleksandr Ekkert bei der Feinarbeit am Arbeitsplatz">
      <img src="assets/img/ueber-2.jpg" alt="Präzise Handarbeit im Dentallabor Ekkert">
    </div>
  </div>
</section>""",
        # statement + cyan stats
        """<section class="section section--tint">
  <div class="container">
    <div class="narrow center reveal"><p class="lead" style="font-size:1.35rem;color:var(--teal-900)">Mit langjähriger Erfahrung, unermüdlicher Hingabe zur Perfektion und dem Glück, unzählige strahlende Lächeln zu schaffen, steht meine Arbeit für höchste Qualität und Kundenzufriedenheit.</p></div>
    <div class="stats stats--cyan" style="margin-top:2.6rem">{stats}</div>
  </div>
</section>""".format(stats=stat_html),
        # modernste geräte
        """<section class="section">
  <div class="container">
    <div class="split split--rev">
      <div class="split__media reveal"><img src="assets/img/ueber-3.jpg" alt="Modernste CAD/CAM-Geräte (Ceramill-Scanner) im Dentallabor Ekkert" loading="lazy"></div>
      <div class="reveal"><span class="eyebrow">Modernste Geräte</span><h2>Fortschrittliche Technologie für perfekten Zahnersatz</h2><p class="lead">Moderne Technologien sind der Schlüssel zu erstklassigem Zahnersatz. Verlassen Sie sich auf höchste Präzision und Qualität für Ihr strahlendes Lächeln.</p><a class="btn btn--ghost" href="leistungen.html" style="margin-top:1rem">Meine Leistungen {arrow}</a></div>
    </div>
  </div>
</section>""".format(arrow=IC["arrow"]),
        # services teaser
        """<section class="section section--tint">
  <div class="container">
    <div class="sec-head center reveal"><span class="eyebrow">Professionell und persönlich</span><h2>Profitieren Sie von meinem Service</h2></div>
    {cards}
    <div class="center" style="margin-top:2.4rem"><a class="btn btn--primary btn--lg" href="leistungen.html">Alle Services {arrow}</a></div>
  </div>
</section>""".format(cards=service_icon_cards(SERVICES[:3]), arrow=IC["arrow"]),
        booking_block("Über mich"), '</main>', footer("kontakt.html"),
    ])

def page_leistungen():
    t = "Leistungen – Zahnersatz, Schönheitsschiene & Implantate | Dentallabor Ekkert Pforzheim"
    d = "Entdecken Sie meine Leistungen: Hollywood-Schönheitsschiene, Kunststoffschiene, Implantate, Zahnersatz, Valplast und Klammerprothese – hochwertig gefertigt in Pforzheim."
    return "".join([
        head(t, d, "leistungen.html"), header("leistungen.html", "kontakt.html"), '<main id="main">',
        """<section class="page-hero">
  <div class="container narrow center reveal">
    <span class="eyebrow" style="justify-content:center">Arbeiten Sie mit mir</span>
    <h1>Meine Mission ist es, mich um Ihr Lächeln zu kümmern.</h1>
    <p class="lead center">Ich gebe Ihnen das Selbstvertrauen, das Sie verdienen – mit einer umfassenden Palette hochwertiger Leistungen für Ihre Zahngesundheit.</p>
  </div>
</section>""",
        """<section class="section" style="padding-top:0"><div class="container">{cards}</div></section>""".format(cards=service_icon_cards(SERVICES)),
        booking_block("Leistungen"), '</main>', footer("kontakt.html"),
    ])

def page_service(s):
    t = "%s – Dentallabor Ekkert Pforzheim" % s["name"]
    d = "Erleben Sie bei Zahntechnik Ekkert eine hochwertige, individuelle Dienstleistung im Bereich %s. Mit langjähriger Erfahrung und persönlichem Engagement für Ihre Zahngesundheit." % s["name"]
    bullets = "".join("<li><strong>{a}</strong><span>{b}</span></li>".format(a=a, b=b) for a, b in s["bullets"])
    detail = s.get("detail_img") or s["hero_img"]
    video = video_facade() if s.get("has_video") else ""
    crumb = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Leistungen", "item": BASE + "/leistungen.html"},
        {"@type": "ListItem", "position": 3, "name": s["name"], "item": BASE + "/" + s["file"]}]}, ensure_ascii=False)
    others = [x for x in SERVICES if x["slug"] != s["slug"]][:3]
    return "".join([
        head(t, d, s["file"], extra_ld='<script type="application/ld+json">%s</script>' % crumb),
        header("leistungen.html", "kontakt.html"), '<main id="main">',
        """<section class="page-hero">
  <div class="container">
    <nav aria-label="Brotkrümel" class="reveal" style="margin-bottom:1rem"><a href="leistungen.html" style="font-weight:700;font-size:.9rem">← Alle Leistungen</a></nav>
    <div class="grid-2">
      <div class="reveal"><span class="eyebrow">Leistung</span><h1>{name}</h1><p class="lead">{intro}</p><div class="hero__cta" style="margin-top:1.4rem"><a class="btn btn--primary btn--lg" href="#termin">Termin anfragen {arrow}</a></div></div>
      <div class="split__media reveal"><img src="assets/img/{hero}" alt="{name} – Dentallabor Ekkert" loading="eager"></div>
    </div>
  </div>
</section>""".format(name=s["name"], intro=s["intro"], hero=s["hero_img"], arrow=IC["arrow"]),
        ('<section class="section" style="padding-top:0"><div class="container narrow">%s</div></section>' % video) if video else "",
        """<section class="section section--tint">
  <div class="container">
    <div class="split">
      <div class="reveal"><span class="eyebrow">Service im Überblick</span><ul class="checks">{bullets}</ul></div>
      <div class="split__media reveal"><img src="assets/img/{detail}" alt="{name}" loading="lazy"></div>
    </div>
    <div class="narrow reveal" style="margin-top:3rem"><h2>Mein Engagement für Ihre Zufriedenheit</h2><p>{eng}</p></div>
  </div>
</section>""".format(bullets=bullets, detail=detail, name=s["name"], eng=s["engagement"]),
        """<section class="section">
  <div class="container">
    <div class="split">
      {hours}
      <div class="reveal"><h2>Kontaktieren Sie mich noch heute!</h2><p class="lead">Füllen Sie das untenstehende Formular aus und ich melde mich innerhalb der nächsten 24 Stunden bei Ihnen.</p><div class="hero__cta" style="margin-top:1rem"><a class="btn btn--primary" href="#termin">Zum Formular {arrow}</a><a class="btn btn--ghost" href="tel:{ph}">Anrufen</a></div></div>
    </div>
  </div>
</section>""".format(hours=hours_card(), arrow=IC["arrow"], ph=BIZ["phone_href"]),
        booking_block(s["name"]),
        """<section class="section section--tint">
  <div class="container"><div class="sec-head center reveal"><span class="eyebrow">Weitere Leistungen</span><h2>Das könnte Sie auch interessieren</h2></div>{cards}</div>
</section>""".format(cards=service_icon_cards(others)),
        '</main>', footer("kontakt.html"),
    ])

def page_kontakt():
    t = "Termin vereinbaren – Kontakt | Dentallabor Ekkert Pforzheim"
    d = "Vereinbaren Sie jetzt Ihren Termin im Dentallabor Ekkert in Pforzheim – telefonisch, per E-Mail oder direkt über das Formular. Ich melde mich innerhalb von 24 Stunden."
    return "".join([
        head(t, d, "kontakt.html"), header("kontakt.html", "#termin"), '<main id="main">',
        """<section class="page-hero">
  <div class="container narrow center reveal">
    <span class="eyebrow" style="justify-content:center">Kontakt-Info</span>
    <h1>Kontaktieren Sie mich noch heute</h1>
    <p class="lead center">Haben Sie Fragen oder möchten Sie einen Termin vereinbaren? Ich stehe Ihnen gerne zur Verfügung, um die beste Lösung für Ihren Zahnersatz zu finden und Ihr Lächeln wieder zum Strahlen zu bringen.</p>
  </div>
</section>""",
        booking_block("Kontakt"), '</main>', footer("#termin"),
    ])

def legal_page(fname, title, desc, h1, body_html):
    return "".join([head(title, desc, fname), header(fname, "kontakt.html"),
        '<main id="main"><section class="section"><div class="container prose">', '<h1>%s</h1>' % h1, body_html,
        '</div></section></main>', footer("kontakt.html")])

def impressum_body():
    return """<p><strong>{name}</strong><br>Firmeninhaber: Herr {owner}<br>{street}<br>{zip} {city}<br>Telefon: <a href="tel:{ph}">{phd}</a><br>E-Mail: <a href="mailto:{em}">{em}</a></p>
<h2>Umsatzsteuer-Identifikationsnummer</h2>
<p>gemäß §27a Umsatzsteuergesetz:<br>Umsatzsteuer-ID: DE292459759</p>
<h2>Hinweis gemäß Online-Streitbeilegungs-Verordnung</h2>
<p>Nach geltendem Recht sind wir verpflichtet, Verbraucher auf die Existenz der Europäischen Online-Streitbeilegungs-Plattform hinzuweisen, die für die Beilegung von Streitigkeiten genutzt werden kann, ohne dass ein Gericht eingeschaltet werden muss. Für die Einrichtung der Plattform ist die Europäische Kommission zuständig. Die Europäische Online-Streitbeilegungs-Plattform ist hier zu finden: <a href="https://ec.europa.eu/odr" rel="noopener" target="_blank">ec.europa.eu/odr</a>. Unsere E-Mail lautet: <a href="mailto:{em}">{em}</a>.</p>
<p>Wir weisen darauf hin, dass wir nicht bereit sind, uns am Streitbeilegungsverfahren im Rahmen der Europäischen Online-Streitbeilegungs-Plattform zu beteiligen. Nutzen Sie zur Kontaktaufnahme bitte unsere obige E-Mail und Telefonnummer.</p>
<h2>Disclaimer – rechtliche Hinweise</h2>
<h3>§ 1 Warnhinweis zu Inhalten</h3>
<p>Die kostenlosen und frei zugänglichen Inhalte dieser Webseite wurden mit größtmöglicher Sorgfalt erstellt. Der Anbieter dieser Webseite übernimmt jedoch keine Gewähr für die Richtigkeit und Aktualität der bereitgestellten kostenlosen und frei zugänglichen journalistischen Ratgeber und Nachrichten. Namentlich gekennzeichnete Beiträge geben die Meinung des jeweiligen Autors und nicht immer die Meinung des Anbieters wieder. Allein durch den Aufruf der kostenlosen und frei zugänglichen Inhalte kommt keinerlei Vertragsverhältnis zwischen dem Nutzer und dem Anbieter zustande, insoweit fehlt es am Rechtsbindungswillen des Anbieters.</p>
<h3>§ 2 Externe Links</h3>
<p>Diese Website enthält Verknüpfungen zu Websites Dritter („externe Links"). Diese Websites unterliegen der Haftung der jeweiligen Betreiber. Der Anbieter hat bei der erstmaligen Verknüpfung der externen Links die fremden Inhalte daraufhin überprüft, ob etwaige Rechtsverstöße bestehen. Zu dem Zeitpunkt waren keine Rechtsverstöße ersichtlich. Der Anbieter hat keinerlei Einfluss auf die aktuelle und zukünftige Gestaltung und auf die Inhalte der verknüpften Seiten. Das Setzen von externen Links bedeutet nicht, dass sich der Anbieter die hinter dem Verweis oder Link liegenden Inhalte zu Eigen macht. Eine ständige Kontrolle der externen Links ist für den Anbieter ohne konkrete Hinweise auf Rechtsverstöße nicht zumutbar. Bei Kenntnis von Rechtsverstößen werden jedoch derartige externe Links unverzüglich gelöscht.</p>
<h3>§ 3 Urheber- und Leistungsschutzrechte</h3>
<p>Die auf dieser Website veröffentlichten Inhalte unterliegen dem deutschen Urheber- und Leistungsschutzrecht. Jede vom deutschen Urheber- und Leistungsschutzrecht nicht zugelassene Verwertung bedarf der vorherigen schriftlichen Zustimmung des Anbieters oder jeweiligen Rechteinhabers. Dies gilt insbesondere für Vervielfältigung, Bearbeitung, Übersetzung, Einspeicherung, Verarbeitung bzw. Wiedergabe von Inhalten in Datenbanken oder anderen elektronischen Medien und Systemen. Die unerlaubte Vervielfältigung oder Weitergabe einzelner Inhalte oder kompletter Seiten ist nicht gestattet und strafbar. Lediglich die Herstellung von Kopien und Downloads für den persönlichen, privaten und nicht kommerziellen Gebrauch ist erlaubt. Die Darstellung dieser Website in fremden Frames ist nur mit schriftlicher Erlaubnis zulässig.</p>
<h3>§ 4 Besondere Nutzungsbedingungen</h3>
<p>Soweit besondere Bedingungen für einzelne Nutzungen dieser Website von den vorgenannten Paragraphen abweichen, wird an entsprechender Stelle ausdrücklich darauf hingewiesen. In diesem Falle gelten im jeweiligen Einzelfall die besonderen Nutzungsbedingungen.</p>""".format(name=BIZ["name"], owner=BIZ["owner"], street=BIZ["street"], zip=BIZ["zip"], city=BIZ["city"], ph=BIZ["phone_href"], phd=BIZ["phone_display"], em=BIZ["email"])

def build():
    pages = {"index.html": page_index(), "ueber.html": page_ueber(), "leistungen.html": page_leistungen(), "kontakt.html": page_kontakt(),
             "impressum.html": legal_page("impressum.html", "Impressum | Dentallabor Ekkert Pforzheim", "Impressum und rechtliche Angaben zum Dentallabor Ekkert, Zahntechnik Aleksandr Ekkert in Pforzheim.", "Impressum", impressum_body()),
             "datenschutz.html": legal_page("datenschutz.html", "Datenschutzerklärung | Dentallabor Ekkert Pforzheim", "Datenschutzerklärung des Dentallabor Ekkert: So verarbeiten und schützen wir Ihre personenbezogenen Daten.", "Datenschutzerklärung", DATENSCHUTZ_HTML)}
    for s in SERVICES:
        pages[s["file"]] = page_service(s)
    for fname, html in pages.items():
        with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
            f.write(html)
    print("Wrote %d pages:" % len(pages))
    for f in sorted(pages):
        print("  ", f)

DATENSCHUTZ_HTML = ""
if __name__ == "__main__":
    from datenschutz_text import DATENSCHUTZ_HTML as _DS
    DATENSCHUTZ_HTML = _DS
    build()
