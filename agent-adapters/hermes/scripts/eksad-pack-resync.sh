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

[ -d "$SRC/role-system-instructions" ] || fail "missing $SRC/role-system-instructions"
[ -d "$SRC/hermes-skills" ] || fail "missing $SRC/hermes-skills"

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

sync_file() {
  local src_path="$1"
  local dst_path="$2"
  local managed_root="$3"
  local label="$4"
  local parent tmp existed=0

  [ -f "$src_path" ] || fail "missing source file: $src_path"
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
  cp -a "$src_dir"/. "$stage"/

  if [ "$existed" -eq 0 ]; then
    mv "$stage" "$dst_dir"
    ADDED=$((ADDED+1))
    CHANGED=$((CHANGED+1))
    echo "+ $label (new)"
    return 0
  fi

  backup="$(mktemp -d "$parent/.eksad-backup.XXXXXX")"
  rmdir "$backup"
  assert_safe_destination "$backup" "$managed_root"
  mv "$dst_dir" "$backup"
  if ! mv "$stage" "$dst_dir"; then
    mv "$backup" "$dst_dir"
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
)

mkdir -p "$DST_PROFILES" "$DST_SKILLS"

# Create or validate every profile. EKSAD_SKIP_PROFILE_CREATE=1 is reserved for
# isolated filesystem tests where the Hermes CLI is intentionally unavailable.
for src_file in "${!PROFILE_MAP[@]}"; do
  profile="${PROFILE_MAP[$src_file]}"
  profile_dir="$DST_PROFILES/$profile"
  config_path="$profile_dir/config.yaml"

  assert_safe_destination "$profile_dir" "$DST_PROFILES"
  assert_safe_destination "$config_path" "$DST_PROFILES"
  if [ ! -f "$config_path" ]; then
    if [ "${EKSAD_SKIP_PROFILE_CREATE:-0}" = "1" ]; then
      mkdir -p "$profile_dir"
    else
      command -v hermes >/dev/null 2>&1 || fail "Hermes CLI required to create profile $profile"
      HERMES_HOME="$HERMES_ROOT" hermes profile create "$profile" --no-alias \
        --description "${PROFILE_DESCRIPTIONS[$profile]}"
      [ -f "$config_path" ] || fail "Hermes did not create $config_path"
      ADDED=$((ADDED+1))
      CHANGED=$((CHANGED+1))
      echo "+ profile/$profile/config.yaml (created by Hermes)"
    fi
  fi

  if [ "${EKSAD_SKIP_PROFILE_CREATE:-0}" != "1" ]; then
    command -v hermes >/dev/null 2>&1 || fail "Hermes CLI required to validate profile $profile"
    HERMES_HOME="$HERMES_ROOT" hermes profile show "$profile" >/dev/null || \
      fail "Hermes rejected profile config: $config_path"
  fi

  sync_file "$SRC/role-system-instructions/$src_file" \
    "$profile_dir/SOUL.md" "$DST_PROFILES" "profile/$profile/SOUL.md"
done

# Global custom skills: each source-owned skill directory is mirrored exactly.
for domain_dir in "$SRC/hermes-skills"/*/; do
  [ -d "$domain_dir" ] || continue
  domain="$(basename "$domain_dir")"
  for skill_dir in "$domain_dir"*/; do
    [ -d "$skill_dir" ] || continue
    skill="$(basename "$skill_dir")"
    sync_tree "$skill_dir" "$DST_SKILLS/$domain/$skill" "$DST_SKILLS" \
      "skill/$domain/$skill"
  done
done

# Named profiles are isolated. Deploy only the fail-closed PM workflow into the
# project-manager profile; generic no-gates orchestration is intentionally absent.
PM_LEGACY_SKILLS=(
  "productivity/stage-gated-orchestrator"
  "business-analysis/eksad-ba-workflow"
  "technical-design/eksad-tsd-design"
  "technical-design/eksad-task-breakdown"
)
for rel in "${PM_LEGACY_SKILLS[@]}"; do
  remove_managed_tree "$DST_PROFILES/project-manager/skills/$rel" \
    "$DST_PROFILES" "profile/project-manager/skill/$rel"
done

PM_PROFILE_SKILLS=(
  "project-management/eksad-pm-delivery"
)
for rel in "${PM_PROFILE_SKILLS[@]}"; do
  sync_tree "$SRC/hermes-skills/$rel" \
    "$DST_PROFILES/project-manager/skills/$rel" "$DST_PROFILES" \
    "profile/project-manager/skill/$rel"
done

# The isolated DevOps profile receives only its fail-closed delivery skill.
# Remove generic permissive orchestration if it remains from an older/manual setup.
DEVOPS_LEGACY_SKILLS=(
  "productivity/stage-gated-orchestrator"
)
for rel in "${DEVOPS_LEGACY_SKILLS[@]}"; do
  remove_managed_tree "$DST_PROFILES/devops-engineer/skills/$rel" \
    "$DST_PROFILES" "profile/devops-engineer/skill/$rel"
done

DEVOPS_PROFILE_SKILLS=(
  "devops/eksad-devops-delivery"
)
for rel in "${DEVOPS_PROFILE_SKILLS[@]}"; do
  sync_tree "$SRC/hermes-skills/$rel" \
    "$DST_PROFILES/devops-engineer/skills/$rel" "$DST_PROFILES" \
    "profile/devops-engineer/skill/$rel"
done

if [ "$CHANGED" -eq 0 ]; then
  echo "No changes ($(date -u +%FT%TZ))"
else
  echo ""
  echo "Summary: $ADDED new, $CHANGED changed"
fi
