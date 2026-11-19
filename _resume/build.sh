#!/usr/bin/env bash
# Builds the CV from main.tex and copies it to /resume.pdf (the file the site links to).
# Usage (from anywhere): _resume/build.sh
set -euo pipefail
cd "$(dirname "$0")"

latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex >/dev/null \
  || { echo "Build failed. See _resume/main.log" >&2; exit 1; }

pages=$(grep -o 'Output written on main.pdf ([0-9]* page' main.log | grep -o '[0-9]* page' | cut -d' ' -f1)
cp main.pdf ../resume.pdf
latexmk -c main.tex >/dev/null   # remove build artefacts (keeps main.pdf locally, which is gitignored)

echo "Built resume.pdf (${pages} page(s))."
if [ "${pages}" != "1" ]; then
  echo "WARNING: the CV is ${pages} pages. Tighten spacing/margins in main.tex to get it back to one page." >&2
  exit 2
fi
