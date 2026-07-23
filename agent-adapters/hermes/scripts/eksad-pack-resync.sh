#!/usr/bin/env bash
# Deploy EKSAD profiles and skills from a checked-out Git knowledge pack.
# This script performs no Git operation and never writes root SOUL.md.

set -Eeuo pipefail

if (( BASH_VERSINFO[0] < 4 )); then
  echo "ERROR: eksad-pack-resync.sh requires Bash 4 or newer" >&2
  exit 2
fi

command -v realpath >/dev/null 2>&1 || {
  echo "ERROR: realpath is required" >&2
  exit 2
}
command -v python3 >/dev/null 2>&1 || {
  echo "ERROR: python3 is required for source-tree safety checks" >&2
  exit 2
}

HERMES_ROOT="$(realpath -m "${HERMES_HOME:-${HOME}/.hermes}")"
SRC="$(realpath -m "${EKSAD_PACK_SRC:-${HERMES_ROOT}/knowledge/eksad}")"
DST_PROFILES="${HERMES_ROOT}/profiles"
DST_SKILLS="${HERMES_ROOT}/skills"
CHANGED=0
ADDED=0

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

# Accept the curated repository root as EKSAD_PACK_SRC. Retain compatibility
# with older deployments where EKSAD_PACK_SRC already points at the Hermes
# adapter directory.
if [ -d "$SRC/agent-adapters/hermes/role-system-instructions" ] && \
   [ -d "$SRC/agent-adapters/hermes/hermes-skills" ]; then
  ADAPTER_SRC="$SRC/agent-adapters/hermes"
elif [ -d "$SRC/role-system-instructions" ] && [ -d "$SRC/hermes-skills" ]; then
  ADAPTER_SRC="$SRC"
else
  fail "missing Hermes adapter source under $SRC (expected agent-adapters/hermes or adapter-root layout)"
fi
ADAPTER_SRC="$(realpath -e "$ADAPTER_SRC")" || fail "cannot canonicalize Hermes adapter source"
case "$ADAPTER_SRC" in
  "$SRC"|"$SRC"/*) ;;
  *) fail "Hermes adapter source escapes EKSAD_PACK_SRC: $ADAPTER_SRC" ;;
esac

assert_safe_source() {
  local path="$1"
  local canonical
  canonical="$(realpath -e "$path")" || fail "cannot canonicalize source: $path"
  case "$canonical" in
    "$ADAPTER_SRC"/*) ;;
    *) fail "source escapes Hermes adapter root: $path" ;;
  esac
}

# Git source trees are copied into runtime-owned locations. Reject every source
# symlink, including nested links, so a checkout cannot preserve references to
# files outside the curated adapter root.
assert_source_tree_safe() {
  local root="$1"
  python3 - "$root" "$ADAPTER_SRC" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve(strict=True)
adapter = Path(sys.argv[2]).resolve(strict=True)
try:
    root.relative_to(adapter)
except ValueError:
    print(f"ERROR: source tree escapes Hermes adapter root: {root}", file=sys.stderr)
    raise SystemExit(1)
for path in root.rglob("*"):
    if path.is_symlink():
        print(f"ERROR: source symlink is forbidden: {path}", file=sys.stderr)
        raise SystemExit(1)
PY
}

# Reject escapes and symlinks below a trusted canonical root. This prevents a
# profile SOUL symlink from redirecting writes to root/default SOUL.md.
assert_safe_destination() {
  local path="$1"
  local root="$2"
  local path_abs root_abs current
  root_abs="$(realpath -m "$root")"
  path_abs="$(realpath -m "$path")"
  case "$path_abs" in
    "$root_abs"/*) ;;
    *) fail "destination escapes managed root: $path" ;;
  esac

  current="$path"
  while [ "$current" != "$root_abs" ] && [ "$current" != "/" ]; do
    [ ! -L "$current" ] || fail "refusing symlink destination component: $current"
    current="$(dirname "$current")"
  done
}

TXN_ACTIVE=0
TXN_DIR=""
declare -a TXN_PATHS=()
declare -a TXN_BACKUPS=()
declare -a TXN_EXISTED=()

transaction_snapshot() {
  local path="$1"
  local managed_root="$2"
  local index backup existed=0
  assert_safe_destination "$path" "$managed_root"
  [ ! -L "$path" ] || fail "refusing symlink transaction target: $path"
  index="${#TXN_PATHS[@]}"
  backup="$TXN_DIR/$index"
  if [ -e "$path" ]; then
    cp -a -- "$path" "$backup" || fail "cannot snapshot transaction target: $path"
    existed=1
  fi
  TXN_PATHS+=("$path")
  TXN_BACKUPS+=("$backup")
  TXN_EXISTED+=("$existed")
}

rollback_transaction() {
  local i path backup existed parent
  [ "$TXN_ACTIVE" -eq 1 ] || return 0
  set +e
  for ((i=${#TXN_PATHS[@]}-1; i>=0; i--)); do
    path="${TXN_PATHS[$i]}"
    backup="${TXN_BACKUPS[$i]}"
    existed="${TXN_EXISTED[$i]}"
    parent="$(dirname "$path")"
    rm -rf -- "$path"
    if [ "$existed" -eq 1 ] && [ -e "$backup" ]; then
      mkdir -p "$parent"
      mv -- "$backup" "$path"
    fi
  done
  rm -rf -- "$TXN_DIR"
  TXN_ACTIVE=0
}

finish_transaction() {
  TXN_ACTIVE=0
  rm -rf -- "$TXN_DIR"
  trap - EXIT HUP INT TERM
}

transaction_exit() {
  local rc="$1"
  if [ "$rc" -ne 0 ]; then
    rollback_transaction
  elif [ "$TXN_ACTIVE" -eq 1 ]; then
    rollback_transaction
    rc=1
  fi
  exit "$rc"
}

sync_file() {
  local src_path="$1"
  local dst_path="$2"
  local managed_root="$3"
  local label="$4"
  local parent tmp existed=0

  [ -f "$src_path" ] || fail "missing source file: $src_path"
  assert_safe_source "$src_path"
  assert_safe_destination "$dst_path" "$managed_root"
  parent="$(dirname "$dst_path")"
  mkdir -p "$parent"
  assert_safe_destination "$dst_path" "$managed_root"

  if [ -f "$dst_path" ]; then
    existed=1
    if cmp -s "$src_path" "$dst_path"; then
      return 0
    fi
  fi

  tmp="$(mktemp "$parent/.eksad-file.XXXXXX")"
  cp -p "$src_path" "$tmp"
  mv -f "$tmp" "$dst_path"

  if [ ! -e "$dst_path" ]; then
    fail "atomic file deployment did not create $dst_path"
  elif [ "$existed" -eq 0 ]; then
    echo "+ $label (new)"
    ADDED=$((ADDED+1))
    CHANGED=$((CHANGED+1))
  else
    echo "~ $label (synced)"
    CHANGED=$((CHANGED+1))
  fi
}

# Mirror one source-controlled skill tree. Atomic replacement removes files
# deleted upstream while limiting deletion to a validated managed directory.
sync_tree() {
  local src_dir="$1"
  local dst_dir="$2"
  local managed_root="$3"
  local label="$4"
  local parent stage backup rc existed=0

  [ -d "$src_dir" ] || fail "missing source directory: $src_dir"
  assert_safe_source "$src_dir"
  assert_safe_destination "$dst_dir" "$managed_root"
  parent="$(dirname "$dst_dir")"
  mkdir -p "$parent"
  assert_safe_destination "$dst_dir" "$managed_root"
  [ ! -L "$dst_dir" ] || fail "refusing symlink destination: $dst_dir"
  if [ -e "$dst_dir" ] && [ ! -d "$dst_dir" ]; then
    fail "destination exists and is not a directory: $dst_dir"
  fi

  if [ -d "$dst_dir" ]; then
    existed=1
    if diff -qr "$src_dir" "$dst_dir" >/dev/null 2>&1; then
      return 0
    else
      rc=$?
      [ "$rc" -le 1 ] || fail "cannot compare $src_dir and $dst_dir"
    fi
  fi

  stage="$(mktemp -d "$parent/.eksad-stage.XXXXXX")"
  if ! cp -a "$src_dir"/. "$stage"/; then
    rm -rf -- "$stage"
    fail "cannot stage source tree for $dst_dir"
  fi

  if [ "$existed" -eq 0 ]; then
    if ! mv "$stage" "$dst_dir"; then
      rm -rf -- "$stage"
      fail "atomic tree deployment failed for $dst_dir"
    fi
    ADDED=$((ADDED+1))
    CHANGED=$((CHANGED+1))
    echo "+ $label (new)"
    return 0
  fi

  backup="$(mktemp -d "$parent/.eksad-backup.XXXXXX")"
  rmdir "$backup"
  assert_safe_destination "$backup" "$managed_root"
  if ! mv "$dst_dir" "$backup"; then
    rm -rf -- "$stage"
    fail "cannot prepare rollback tree for $dst_dir"
  fi
  if ! mv "$stage" "$dst_dir"; then
    mv "$backup" "$dst_dir" || fail "tree deployment and local rollback both failed for $dst_dir"
    fail "atomic tree deployment failed for $dst_dir"
  fi
  rm -rf -- "$backup"
  CHANGED=$((CHANGED+1))
  echo "~ $label (updated)"
}

# Remove only an explicitly named legacy tree under a validated managed root.
# Atomic rename prevents partial removal; symlinks and path escapes are refused.
remove_managed_tree() {
  local path="$1"
  local managed_root="$2"
  local label="$3"
  local parent backup

  assert_safe_destination "$path" "$managed_root"
  if [ ! -e "$path" ] && [ ! -L "$path" ]; then
    return 0
  fi
  [ ! -L "$path" ] || fail "refusing legacy symlink removal: $path"
  [ -d "$path" ] || fail "legacy path is not a directory: $path"

  parent="$(dirname "$path")"
  backup="$(mktemp -d "$parent/.eksad-remove.XXXXXX")"
  rmdir "$backup"
  assert_safe_destination "$backup" "$managed_root"
  mv "$path" "$backup"
  rm -rf -- "$backup"
  CHANGED=$((CHANGED+1))
  echo "- $label (legacy removed)"
}

declare -A PROFILE_MAP=(
  ["business-analyst.md"]="business-analyst"
  ["system-analyst.md"]="system-analyst"
  ["technical-leader.md"]="technical-leader"
  ["developer-backend.md"]="developer-backend"
  ["developer-frontend.md"]="developer-frontend"
  ["qa-engineer.md"]="qa-engineer"
  ["general.md"]="eksad-general"
  ["project-manager.md"]="project-manager"
  ["devops-engineer.md"]="devops-engineer"
  ["data-analyst.md"]="data-analyst"
  ["data-scientist.md"]="data-scientist"
  ["ui-ux-designer.md"]="ui-ux-designer"
  ["content-creator.md"]="content-creator"
)

PROFILE_ORDER=(
  "general.md"
  "business-analyst.md"
  "system-analyst.md"
  "technical-leader.md"
  "developer-backend.md"
  "developer-frontend.md"
  "qa-engineer.md"
  "project-manager.md"
  "devops-engineer.md"
  "data-analyst.md"
  "data-scientist.md"
  "ui-ux-designer.md"
  "content-creator.md"
)

declare -A PROFILE_DESCRIPTIONS=(
  ["business-analyst"]="EKSAD requirements specialist for UR, BRD, FSD, business rules, and acceptance criteria."
  ["system-analyst"]="EKSAD system design specialist for TSD, service boundaries, data, APIs, events, and technical specifications."
  ["technical-leader"]="EKSAD technical quality specialist for architecture review, code review, ADRs, and mentoring."
  ["developer-backend"]="EKSAD backend implementation specialist for Java, Quarkus or Spring Boot, persistence, APIs, and tests."
  ["developer-frontend"]="EKSAD frontend implementation specialist for React, TypeScript, components, hooks, services, and tests."
  ["qa-engineer"]="EKSAD quality specialist for test plans, traceability, test cases, automation handoff, and evidence."
  ["eksad-general"]="EKSAD cross-role assistant for overview, routing, and management-level questions."
  ["project-manager"]="EKSAD delivery-governance specialist for Charter, Plan, RAID, status, change control, dependencies, and stage gates."
  ["devops-engineer"]="EKSAD delivery-operations specialist for GitLab CE, Jenkins CI/CD, SonarQube/Trivy evidence, deployment, rollback, observability, and release readiness."
  ["data-analyst"]="EKSAD data-analysis specialist for source assessment, metric definitions, analysis reports, and dashboard specifications."
  ["data-scientist"]="EKSAD data-science specialist for experiment design, model evaluation, evidence, limitations, and gated production handoff."
  ["ui-ux-designer"]="EKSAD UI/UX specialist for research evidence, interaction design, accessibility, and implementation-ready handoffs."
  ["content-creator"]="EKSAD content specialist for sourced briefs, calendars, drafts, release content, and publication handoffs."
)

# Build and validate the complete operation plan before the first runtime write.
assert_source_tree_safe "$ADAPTER_SRC"

if [ "${EKSAD_SKIP_PROFILE_CREATE:-0}" != "1" ]; then
  command -v hermes >/dev/null 2>&1 || fail "Hermes CLI is required for profile validation/creation"
fi

GLOBAL_SKILL_SOURCES=()
GLOBAL_SKILL_DESTS=()
GLOBAL_SKILL_LABELS=()
for domain_dir in "$ADAPTER_SRC/hermes-skills"/*/; do
  [ -d "$domain_dir" ] || continue
  domain="$(basename "$domain_dir")"
  for skill_dir in "$domain_dir"*/; do
    [ -d "$skill_dir" ] || continue
    skill="$(basename "$skill_dir")"
    assert_safe_source "$skill_dir"
    assert_safe_destination "$DST_SKILLS/$domain/$skill" "$DST_SKILLS"
    GLOBAL_SKILL_SOURCES+=("$skill_dir")
    GLOBAL_SKILL_DESTS+=("$DST_SKILLS/$domain/$skill")
    GLOBAL_SKILL_LABELS+=("skill/$domain/$skill")
  done
done

PM_LEGACY_SKILLS=(
  "productivity/stage-gated-orchestrator"
  "business-analysis/eksad-ba-workflow"
  "technical-design/eksad-tsd-design"
  "technical-design/eksad-task-breakdown"
)
PM_PROFILE_SKILLS=("project-management/eksad-pm-delivery")
DEVOPS_LEGACY_SKILLS=("productivity/stage-gated-orchestrator")
DEVOPS_PROFILE_SKILLS=("devops/eksad-devops-delivery")

for src_file in "${PROFILE_ORDER[@]}"; do
  profile="${PROFILE_MAP[$src_file]}"
  profile_dir="$DST_PROFILES/$profile"
  config_path="$profile_dir/config.yaml"
  source_soul="$ADAPTER_SRC/role-system-instructions/$src_file"
  [ -f "$source_soul" ] || fail "missing source file: $source_soul"
  assert_safe_source "$source_soul"
  assert_safe_destination "$profile_dir" "$DST_PROFILES"
  assert_safe_destination "$config_path" "$DST_PROFILES"
  assert_safe_destination "$profile_dir/SOUL.md" "$DST_PROFILES"
  if [ "${EKSAD_SKIP_PROFILE_CREATE:-0}" != "1" ] && [ -f "$config_path" ]; then
    HERMES_HOME="$HERMES_ROOT" hermes profile show "$profile" >/dev/null || \
      fail "Hermes rejected profile config during preflight: $config_path"
  fi
done

for rel in "${PM_LEGACY_SKILLS[@]}"; do
  assert_safe_destination "$DST_PROFILES/project-manager/skills/$rel" "$DST_PROFILES"
done
for rel in "${PM_PROFILE_SKILLS[@]}"; do
  assert_safe_source "$ADAPTER_SRC/hermes-skills/$rel"
  assert_safe_destination "$DST_PROFILES/project-manager/skills/$rel" "$DST_PROFILES"
done
for rel in "${DEVOPS_LEGACY_SKILLS[@]}"; do
  assert_safe_destination "$DST_PROFILES/devops-engineer/skills/$rel" "$DST_PROFILES"
done
for rel in "${DEVOPS_PROFILE_SKILLS[@]}"; do
  assert_safe_source "$ADAPTER_SRC/hermes-skills/$rel"
  assert_safe_destination "$DST_PROFILES/devops-engineer/skills/$rel" "$DST_PROFILES"
done

# Start a transaction before the first managed runtime mutation. Snapshot whole
# profile directories because Hermes profile creation may write more than SOUL.md;
# snapshot only EKSAD-owned global skill targets to avoid touching unrelated skills.
mkdir -p "$HERMES_ROOT"
TXN_DIR="$(mktemp -d "$HERMES_ROOT/.eksad-transaction.XXXXXX")"
TXN_ACTIVE=1
trap 'transaction_exit $?' EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

mkdir -p "$DST_PROFILES" "$DST_SKILLS"
for src_file in "${PROFILE_ORDER[@]}"; do
  profile="${PROFILE_MAP[$src_file]}"
  transaction_snapshot "$DST_PROFILES/$profile" "$DST_PROFILES"
done
for dst_dir in "${GLOBAL_SKILL_DESTS[@]}"; do
  transaction_snapshot "$dst_dir" "$DST_SKILLS"
done

# Create or validate every profile. EKSAD_SKIP_PROFILE_CREATE=1 is reserved for
# isolated filesystem tests where the Hermes CLI is intentionally unavailable.
for src_file in "${PROFILE_ORDER[@]}"; do
  profile="${PROFILE_MAP[$src_file]}"
  profile_dir="$DST_PROFILES/$profile"
  config_path="$profile_dir/config.yaml"

  if [ ! -f "$config_path" ]; then
    if [ "${EKSAD_SKIP_PROFILE_CREATE:-0}" = "1" ]; then
      mkdir -p "$profile_dir"
    else
      HERMES_HOME="$HERMES_ROOT" hermes profile create "$profile" --no-alias \
        --description "${PROFILE_DESCRIPTIONS[$profile]}"
      [ -f "$config_path" ] || fail "Hermes did not create $config_path"
      ADDED=$((ADDED+1))
      CHANGED=$((CHANGED+1))
      echo "+ profile/$profile/config.yaml (created by Hermes)"
    fi
  fi

  if [ "${EKSAD_SKIP_PROFILE_CREATE:-0}" != "1" ]; then
    HERMES_HOME="$HERMES_ROOT" hermes profile show "$profile" >/dev/null || \
      fail "Hermes rejected profile config: $config_path"
  fi

  sync_file "$ADAPTER_SRC/role-system-instructions/$src_file" \
    "$profile_dir/SOUL.md" "$DST_PROFILES" "profile/$profile/SOUL.md"
done

# Test-only fault injection proves operation-wide rollback after managed writes.
if [ "${EKSAD_SKIP_PROFILE_CREATE:-0}" = "1" ] && \
   [ "${EKSAD_TEST_ABORT_AFTER_PROFILES:-0}" = "1" ]; then
  fail "injected failure after profile synchronization"
fi

for ((i=0; i<${#GLOBAL_SKILL_SOURCES[@]}; i++)); do
  sync_tree "${GLOBAL_SKILL_SOURCES[$i]}" "${GLOBAL_SKILL_DESTS[$i]}" "$DST_SKILLS" \
    "${GLOBAL_SKILL_LABELS[$i]}"
done

# Named profiles are isolated. Deploy only their fail-closed delivery workflow.
for rel in "${PM_LEGACY_SKILLS[@]}"; do
  remove_managed_tree "$DST_PROFILES/project-manager/skills/$rel" \
    "$DST_PROFILES" "profile/project-manager/skill/$rel"
done
for rel in "${PM_PROFILE_SKILLS[@]}"; do
  sync_tree "$ADAPTER_SRC/hermes-skills/$rel" \
    "$DST_PROFILES/project-manager/skills/$rel" "$DST_PROFILES" \
    "profile/project-manager/skill/$rel"
done
for rel in "${DEVOPS_LEGACY_SKILLS[@]}"; do
  remove_managed_tree "$DST_PROFILES/devops-engineer/skills/$rel" \
    "$DST_PROFILES" "profile/devops-engineer/skill/$rel"
done
for rel in "${DEVOPS_PROFILE_SKILLS[@]}"; do
  sync_tree "$ADAPTER_SRC/hermes-skills/$rel" \
    "$DST_PROFILES/devops-engineer/skills/$rel" "$DST_PROFILES" \
    "profile/devops-engineer/skill/$rel"
done

finish_transaction

if [ "$CHANGED" -eq 0 ]; then
  echo "No changes ($(date -u +%FT%TZ))"
else
  echo ""
  echo "Summary: $ADDED new, $CHANGED changed"
fi
