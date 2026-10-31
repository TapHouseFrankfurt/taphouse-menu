#!/usr/bin/env bash
# Renders the three "Final Menus" PDFs (one-page display layout) and commits them to
# final-menus/ ONLY when the visible text changed (ratings ignored). Runs in CI after the
# normal build, once the Pages artifact has already been uploaded (so overwriting public/ is harmless).
# DRY_RUN=1 -> report only, no git commit/push.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=final-menus; mkdir -p "$OUT"

# Same label rule as the manual pipeline (Kiran, 30.09.2026): flights read "flight only".
sed -i 's/100ml (flight)"/100ml (flight only)"/g' public/_drinks.json

python pdf/render_drinks_final.py

declare -A MAP=(
  [tap-beers.pdf]=TapHouse_Tap_Beers_Print_A4.pdf
  [tap-beers-display.pdf]=TapHouse_Tap_Beers_Display_A4.pdf
  [other-drinks-display.pdf]=TapHouse_Other_Drinks_Display_A4.pdf
)

# Visible text without ratings (those drift constantly).
norm() { pdftotext -layout "$1" - | grep -v -E 'ratings' | grep -v -E '^\s*[0-9]\.[0-9]+\s*$' | tr -s ' \n'; }

# Sanity gates: never publish a broken render.
pages=$(pdfinfo public/tap-beers-display.pdf | awk '/^Pages:/{print $2}')
[ "$pages" = "1" ] || { echo "::error::tap-beers-display.pdf has $pages pages, expected 1"; exit 1; }
for f in tap-beers.pdf tap-beers-display.pdf; do
  t=$(pdftotext public/$f -)
  grep -q "flight only" <<<"$t" || { echo "::error::$f lacks 'flight only'"; exit 1; }
  ! grep -q "(flight)" <<<"$t"  || { echo "::error::$f still has '(flight)'"; exit 1; }
done

changed=()
for src in "${!MAP[@]}"; do
  dst="$OUT/${MAP[$src]}"
  if [ ! -f "$dst" ] || ! diff -q <(norm "$dst") <(norm "public/$src") >/dev/null; then
    cp "public/$src" "$dst"; changed+=("${MAP[$src]}")
  fi
done

if [ ${#changed[@]} -eq 0 ]; then echo "No menu change - final-menus/ already current."; exit 0; fi
echo "Changed: ${changed[*]}"
[ "${DRY_RUN:-0}" = "1" ] && exit 0

git config user.name  "taphouse-menu-bot"
git config user.email "actions@users.noreply.github.com"
git add "$OUT"
git commit -m "Final menus refreshed: ${changed[*]} [skip ci]"
git pull --rebase origin "${GITHUB_REF_NAME:-main}" || true
git push
