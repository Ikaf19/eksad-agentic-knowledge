#!/usr/bin/env bash
# Isolated regression tests for curated-repository and adapter-root Hermes resync.
# Every write is confined to a temporary HERMES_HOME; active runtime is untouched.

set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ADAPTER="$ROOT/agent-adapters/hermes"
SCRIPT="$ADAPTER/scripts/eksad-pack-resync.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

run_resync() {
  local source_root="$1"
  local hermes_home="$2"
  local output="$3"
  EKSAD_PACK_SRC="$source_root" \
  HERMES_HOME="$hermes_home" \
  EKSAD_SKIP_PROFILE_CREATE=1 \
    bash "$SCRIPT" >"$output"
}

declare -A PROFILE_SOURCES=(
  ["eksad-general"]="general.md"
  ["business-analyst"]="business-analyst.md"
  ["system-analyst"]="system-analyst.md"
  ["technical-leader"]="technical-leader.md"
  ["developer-backend"]="developer-backend.md"
  ["developer-frontend"]="developer-frontend.md"
  ["qa-engineer"]="qa-engineer.md"
  ["project-manager"]="project-manager.md"
  ["devops-engineer"]="devops-engineer.md"
  ["data-analyst"]="data-analyst.md"
  ["data-scientist"]="data-scientist.md"
  ["ui-ux-designer"]="ui-ux-designer.md"
  ["content-creator"]="content-creator.md"
)

CURATED_HOME="$TMP/curated-hermes"
run_resync "$ROOT" "$CURATED_HOME" "$TMP/curated-first.out"

for profile in "${!PROFILE_SOURCES[@]}"; do
  source_file="$ADAPTER/role-system-instructions/${PROFILE_SOURCES[$profile]}"
  soul="$CURATED_HOME/profiles/$profile/SOUL.md"
  if [ ! -s "$soul" ] || ! cmp -s "$source_file" "$soul"; then
    echo "FAIL: SOUL mapping mismatch for $profile" >&2
    exit 1
  fi
done

profile_dir_count="$(python3 - "$CURATED_HOME/profiles" <<'PY'
from pathlib import Path
import sys
print(sum(1 for path in Path(sys.argv[1]).iterdir() if path.is_dir()))
PY
)"
if [ "$profile_dir_count" -ne 13 ]; then
  echo "FAIL: expected exactly 13 profile directories, found $profile_dir_count" >&2
  exit 1
fi

for skill in \
  data-analysis/eksad-data-analysis \
  data-science/eksad-data-science \
  design/eksad-ui-ux-delivery \
  content/eksad-content-creation; do
  if [ ! -s "$CURATED_HOME/skills/$skill/SKILL.md" ]; then
    echo "FAIL: missing synchronized role skill: $skill" >&2
    exit 1
  fi
done

for isolated_profile in project-manager devops-engineer; do
  if [ -e "$CURATED_HOME/profiles/$isolated_profile/skills/productivity/stage-gated-orchestrator" ]; then
    echo "FAIL: generic orchestrator leaked into isolated profile: $isolated_profile" >&2
    exit 1
  fi
done

if [ -e "$CURATED_HOME/SOUL.md" ]; then
  echo "FAIL: resync must not create or overwrite root SOUL.md" >&2
  exit 1
fi

# A second run over identical source must be idempotent.
run_resync "$ROOT" "$CURATED_HOME" "$TMP/curated-second.out"
if ! grep -q '^No changes ' "$TMP/curated-second.out"; then
  echo "FAIL: second curated-layout resync was not idempotent" >&2
  exit 1
fi

# Preserve compatibility when EKSAD_PACK_SRC already points at the adapter root.
LEGACY_HOME="$TMP/adapter-root-hermes"
run_resync "$ADAPTER" "$LEGACY_HOME" "$TMP/adapter-root.out"
for profile in "${!PROFILE_SOURCES[@]}"; do
  if ! cmp -s "$ADAPTER/role-system-instructions/${PROFILE_SOURCES[$profile]}" \
      "$LEGACY_HOME/profiles/$profile/SOUL.md"; then
    echo "FAIL: adapter-root compatibility mapping mismatch for $profile" >&2
    exit 1
  fi
done

# A source symlink that escapes the adapter root must fail closed.
cp -a "$ADAPTER" "$TMP/unsafe-adapter"
printf 'outside source\n' >"$TMP/outside.md"
rm "$TMP/unsafe-adapter/role-system-instructions/data-analyst.md"
ln -s "$TMP/outside.md" "$TMP/unsafe-adapter/role-system-instructions/data-analyst.md"
if run_resync "$TMP/unsafe-adapter" "$TMP/unsafe-hermes" "$TMP/unsafe.out" 2>"$TMP/unsafe.err"; then
  echo "FAIL: source symlink escape was accepted" >&2
  exit 1
fi
if ! grep -q 'source symlink is forbidden' "$TMP/unsafe.err"; then
  echo "FAIL: source symlink escape did not produce the expected guard error" >&2
  exit 1
fi

# Nested symlinks inside copied skill trees must also fail closed.
cp -a "$ADAPTER" "$TMP/nested-link-adapter"
printf 'external nested source\n' >"$TMP/nested-outside.txt"
ln -s "$TMP/nested-outside.txt" \
  "$TMP/nested-link-adapter/hermes-skills/data-analysis/eksad-data-analysis/references-escape.txt"
if run_resync "$TMP/nested-link-adapter" "$TMP/nested-link-hermes" \
    "$TMP/nested-link.out" 2>"$TMP/nested-link.err"; then
  echo "FAIL: nested skill source symlink was accepted" >&2
  exit 1
fi
if [ -e "$TMP/nested-link-hermes/profiles/data-analyst/SOUL.md" ]; then
  echo "FAIL: nested source symlink failure left partial profile state" >&2
  exit 1
fi

# A missing late source file must be rejected during preflight before any SOUL write.
cp -a "$ADAPTER" "$TMP/missing-source-adapter"
rm "$TMP/missing-source-adapter/role-system-instructions/content-creator.md"
if run_resync "$TMP/missing-source-adapter" "$TMP/missing-source-hermes" \
    "$TMP/missing-source.out" 2>"$TMP/missing-source.err"; then
  echo "FAIL: missing profile source was accepted" >&2
  exit 1
fi
if python3 - "$TMP/missing-source-hermes" <<'PY'
from pathlib import Path
import sys
root = Path(sys.argv[1])
raise SystemExit(0 if any(root.glob('profiles/*/SOUL.md')) else 1)
PY
then
  echo "FAIL: source preflight failure left partial SOUL state" >&2
  exit 1
fi

# Failure after profile mutations must restore the complete managed baseline.
ROLLBACK_HOME="$TMP/rollback-hermes"
run_resync "$ROOT" "$ROLLBACK_HOME" "$TMP/rollback-baseline.out"
cp -a "$ROLLBACK_HOME" "$TMP/rollback-before"
cp -a "$ADAPTER" "$TMP/rollback-adapter"
printf '\n<!-- transaction rollback probe -->\n' >> \
  "$TMP/rollback-adapter/role-system-instructions/content-creator.md"
if EKSAD_PACK_SRC="$TMP/rollback-adapter" \
   HERMES_HOME="$ROLLBACK_HOME" \
   EKSAD_SKIP_PROFILE_CREATE=1 \
   EKSAD_TEST_ABORT_AFTER_PROFILES=1 \
   bash "$SCRIPT" >"$TMP/rollback-failure.out" 2>"$TMP/rollback-failure.err"; then
  echo "FAIL: injected transaction failure unexpectedly succeeded" >&2
  exit 1
fi
if ! diff -qr "$TMP/rollback-before" "$ROLLBACK_HOME" >/dev/null; then
  echo "FAIL: transaction rollback did not restore the complete baseline" >&2
  exit 1
fi

echo "PASS: isolated Hermes resync tests (13 exact mappings, two layouts, idempotent, source-confined, transactional)"
