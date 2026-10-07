#!/usr/bin/env bash
# Fetch the nine competition CSVs into data/ when the Actions cache is empty.
# URLs come from work/urls.txt inside the encrypted bundle: "filename|signed_url" per line.
set -euo pipefail
set +x
cd "$GITHUB_WORKSPACE"
files="players.csv combine_results.csv combine_tracking.csv player_career_successes.csv games.csv player_play.csv game_tracking_2023.csv game_tracking_2024.csv game_tracking_2025.csv"
missing=0
for f in $files; do [ -s "data/$f" ] || missing=1; done
if [ "$missing" = 0 ]; then echo "data: all nine files present"; exit 0; fi
if [ ! -f work/urls.txt ]; then echo "data missing and bundle has no urls.txt"; exit 1; fi
mkdir -p data
while IFS='|' read -r name url; do
  [ -z "${name:-}" ] && continue
  [ -s "data/$name" ] && continue
  curl -sS -L --retry 3 --retry-delay 5 -o "data/$name" "$url" || { echo "download failed: $name"; rm -f "data/$name"; exit 1; }
done < work/urls.txt
for f in $files; do [ -s "data/$f" ] || { echo "still missing: $f"; exit 1; }; done
du -sh data
