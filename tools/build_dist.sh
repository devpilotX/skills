#!/usr/bin/env bash
# Build one zip per skill plus a bundle of all of them, into dist/.
#
# Each per skill zip contains the skill folder at its root, so it can be dropped
# straight into .kiro/skills/ or uploaded through Settings, then Skills, in Kiro
# Web. The bundle contains every skill folder side by side.
#
# Usage: bash tools/build_dist.sh

set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

if [ ! -d skills ]; then
  echo "no skills directory found in $root" >&2
  exit 1
fi

rm -rf dist
mkdir -p dist

# Strip caches so they never reach a published artifact.
find skills -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
find skills -name '*.pyc' -type f -delete 2>/dev/null || true

count=0
for dir in skills/*/; do
  name="$(basename "$dir")"
  [ -f "$dir/SKILL.md" ] || { echo "skipping $name, no SKILL.md" >&2; continue; }
  (cd skills && zip -q -r "../dist/${name}.zip" "$name" -x '*.pyc' -x '*__pycache__*')
  size="$(wc -c < "dist/${name}.zip" | tr -d ' ')"
  printf 'built dist/%-22s %8s bytes\n' "${name}.zip" "$size"
  count=$((count + 1))
done

(cd skills && zip -q -r ../dist/skills-all.zip . -x '*.pyc' -x '*__pycache__*')
printf 'built dist/%-22s %8s bytes\n' "skills-all.zip" "$(wc -c < dist/skills-all.zip | tr -d ' ')"

# A checksum file so a download can be verified.
(cd dist && sha256sum ./*.zip > SHA256SUMS.txt)

echo
echo "packaged $count skills into dist/"
echo "verify a download with: sha256sum -c SHA256SUMS.txt"
