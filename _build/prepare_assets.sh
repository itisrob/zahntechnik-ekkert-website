#!/usr/bin/env bash
# Asset pipeline for zahntechnik-ekkert-website
# - Downscales + recompresses Framer originals (preserve format), renames to semantic names
# - Generates favicons + video poster
# - Best-effort self-hosts Cabinet Grotesk (display) + Lato (body) as woff2 (DSGVO)
set -u
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
ROOT="/Users/robertekkert/Downloads/claude-workspace-template/outputs/zahntechnik-ekkert-website"
RAW="$ROOT/assets/_framer_raw"
IMG="$ROOT/assets/img"
FONTS="$ROOT/assets/fonts"
mkdir -p "$IMG" "$FONTS"

# optimize <srcHash.ext> <outName> <maxw>
# preserves format; skips resize for tiny files; jpeg quality 78
optimize(){
  local src="$RAW/$1" out="$IMG/$2" maxw="$3"
  if [ ! -f "$src" ]; then echo "  MISSING $1"; return; fi
  local ext="${1##*.}"; ext="$(echo "$ext" | tr 'A-Z' 'a-z')"
  local sz=$(stat -f%z "$src" 2>/dev/null || echo 0)
  case "$ext" in
    jpg|jpeg)
      sips -Z "$maxw" -s format jpeg -s formatOptions 78 "$src" --out "$out" >/dev/null 2>&1 ;;
    png)
      sips -Z "$maxw" -s format png "$src" --out "$out" >/dev/null 2>&1 ;;
    svg)
      cp "$src" "$out" ;;
    *) cp "$src" "$out" ;;
  esac
  local nsz=$(stat -f%z "$out" 2>/dev/null || echo 0)
  printf "  %-28s %6dKB -> %5dKB\n" "$2" $((sz/1024)) $((nsz/1024))
}

echo "== Images =="
# logo + brand
optimize EiUG6FNxXtwSk2BiGQ08jAKHzyQ.png logo.png 400
optimize qerHJ0pNayyLsxmDNdRfB0aqZ1I.png og-image.png 1200
# home
optimize Y3E0XB4mCp0iYfRTxppVuuO13s.png hero.png 1500
optimize ljZyYkB8brXcHnfUAcLpkWjvef8.jpeg svc-schoenheitsschiene.jpg 900
optimize Fmcb7w7fx21GFPADhZjfR5Q30.jpeg svc-kunststoffschiene.jpg 900
optimize nlTz5UynMSHZvZIq4cSNnbtI64.jpeg svc-implantate.jpg 900
# ueber
optimize C7g5EOtcJscyS8sftKs7UMmACY.jpeg ueber-1.jpg 1100
optimize iAEqp6sIkUGlGMKzRmqxyYPKMU0.jpeg ueber-2.jpg 1100
optimize PkQbZSyHZecmR8sOQSJv8Ynns.jpeg ueber-3.jpg 1100
# service overview
optimize KSl54Tu7OWcz9ERq1W1DvOpnLs.jpeg leistungen-hero.jpg 1400
# service subpages
optimize M4Jit4BuP3JD8K24BwKYWUG60.png schiene-hero.png 1100
optimize iPhgUh8SG6KtvVBPPMEGq3jGA.png schiene-detail.png 1000
optimize tYNKHMiH7SbXfcxjRnYhGAYnQGU.jpg kunststoff-hero.jpg 1200
optimize 0WqfRgBW6mvIg0Cz96EICKCUZI.png kunststoff-detail.png 1000
optimize FQfESgSn772nK2bkzeQlgSlZefU.jpg implantate-hero.jpg 1200
optimize ZMIAgmMv0pjOIS2GHEwsvSqhs2w.jpg zahnersatz-hero.jpg 1200
optimize nW51IUdIc9hNlaji8CDYNXJCoc.jpg valplast-hero.jpg 1200
optimize bgExxwuDl1todMugzON3gpMrM4.jpg klammer-hero.jpg 1200
# kontakt
optimize 5oxNl9i9i9bS0Zo67mzCb3YWWQ.jpeg kontakt.jpg 1200
# icons (svg copy)
optimize YaOlYhM7sBA72dhpyVkk8s0xs.svg icon-qualitaet.svg 100
optimize APSVohPurFbba7oY5W8UMObQlY.svg icon-komfort.svg 100
optimize p8BR4ItLE813QhRRZXGZxzCNEQ.svg icon-beratung.svg 100
optimize Cmd8iFQB7xZbAsXGBQFe9RPKB4.svg icon-a.svg 100
optimize CNsEZEzCOVJaIUYvRcRSYtgGY00.svg icon-b.svg 100

echo "== Favicons (from site favicon 3YwSgQ...) =="
FAV="$RAW/3YwSgQ7hC4LBXZWlgFWf09E7zw.png"
if [ -f "$FAV" ]; then
  sips -z 180 180 -s format png "$FAV" --out "$ROOT/assets/apple-touch-icon.png" >/dev/null 2>&1 && echo "  apple-touch-icon.png"
  sips -z 32 32 -s format png "$FAV" --out "$ROOT/assets/favicon-32.png" >/dev/null 2>&1 && echo "  favicon-32.png"
  sips -z 16 16 -s format png "$FAV" --out "$ROOT/assets/favicon-16.png" >/dev/null 2>&1 && echo "  favicon-16.png"
fi

echo "== YouTube video poster (Snap on Smile / PwmMA5fmEe4) =="
curl -sL --max-time 30 -A "$UA" "https://i.ytimg.com/vi/PwmMA5fmEe4/maxresdefault.jpg" -o "$IMG/video-poster.jpg" \
  && echo "  video-poster.jpg $(( $(stat -f%z "$IMG/video-poster.jpg")/1024 ))KB"

echo "== Fonts (best-effort self-host) =="
# Cabinet Grotesk (Fontshare) — variable/static woff2
curl -sL --max-time 25 -A "$UA" "https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@500,700,800&display=swap" -o "$FONTS/_cabinet.css" 2>/dev/null
grep -oE 'https://[^)"]+\.woff2' "$FONTS/_cabinet.css" 2>/dev/null | sort -u | while read -r u; do
  curl -sL --max-time 25 -A "$UA" "$u" -o "$FONTS/$(basename "$u")" 2>/dev/null
done
# Lato (Google Fonts) — modern UA yields woff2; keep latin only
curl -sL --max-time 25 -A "$UA" "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap" -o "$FONTS/_lato.css" 2>/dev/null
# Google groups by subset with comments; grab URLs (we filter latin when authoring @font-face)
grep -oE 'https://[^)"]+\.woff2' "$FONTS/_lato.css" 2>/dev/null | sort -u | while read -r u; do
  curl -sL --max-time 25 -A "$UA" "$u" -o "$FONTS/lato-$(basename "$u")" 2>/dev/null
done
echo "  --- cabinet.css @font-face src refs ---"
grep -oE 'font-weight: [0-9]+|https://[^)"]+\.woff2' "$FONTS/_cabinet.css" 2>/dev/null | head -20
echo "  --- lato.css @font-face (weights + subsets) ---"
grep -oE '/\* [a-z-]+ \*/|font-weight: [0-9]+|https://[^)"]+\.woff2' "$FONTS/_lato.css" 2>/dev/null | head -40
echo ""
echo "== Font files downloaded =="
ls -la "$FONTS" | grep -iE '\.woff2$' | awk '{printf "  %-40s %6dKB\n",$9,$5/1024}'
echo ""
echo "== Final image sizes =="
du -sh "$IMG" 2>/dev/null | awk '{print "  img total: "$1}'
echo "DONE"
