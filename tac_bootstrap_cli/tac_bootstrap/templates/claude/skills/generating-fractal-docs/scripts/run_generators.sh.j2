REPO_ROOT=""
AUTO_BRANCH="0"
DRY_RUN="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      REPO_ROOT="$(cd "$2" && pwd)"
      shift 2
      ;;
    --dry-run)
      DRY_RUN="1"
      shift
      ;;
    --auto-branch)
      AUTO_BRANCH="1"
      shift
      ;;
    -h|--help)
      echo "Usage: run_generators.sh --repo <path> [--dry-run] [--auto-branch]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

[[ -n "$REPO_ROOT" ]] || die "--repo <path> is required"
[[ -d "$REPO_ROOT" ]] || die "--repo must point to an existing directory"

# -----------------------------
# Preflight
# -----------------------------
command -v python3 >/dev/null 2>&1 || die "python3 not found"
command -v git >/dev/null 2>&1 || die "git not found"

[[ -d "$SCRIPT_DIR" ]] || die "Skill scripts directory not found: $SCRIPT_DIR"
[[ -f "$SCRIPT_DIR/gen_docstring_jsdocs.py" ]] || die "Missing gen_docstring_jsdocs.py"
[[ -f "$SCRIPT_DIR/gen_docs_fractal.py" ]] || die "Missing gen_docs_fractal.py"

git rev-parse --is-inside-work-tree >/dev/null 2>&1 \
  || die "Not inside a git repository"

CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

log "Current branch: $CURRENT_BRANCH"

# -----------------------------
# Auto-branch logic
# -----------------------------
if [[ "$AUTO_BRANCH" == "1" ]]; then
  if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
    TARGET_BRANCH="chore/regen-fractal-docs"

    if git show-ref --verify --quiet "refs/heads/$TARGET_BRANCH"; then
      log "Switching to existing branch: $TARGET_BRANCH"
      git checkout "$TARGET_BRANCH"
    else
      log "Creating branch: $TARGET_BRANCH"
      git checkout -b "$TARGET_BRANCH"
    fi
  else
    log "Already on non-main branch ($CURRENT_BRANCH); auto-branch skipped"
  fi
else
  if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
    log "⚠️  Running on $CURRENT_BRANCH without --auto-branch"
    log "⚠️  Recommended: rerun with --auto-branch"
  fi
fi

# -----------------------------
# Dirty tree warning
# -----------------------------
if [[ -n "$(git status --porcelain)" ]]; then
  log "⚠️  Working tree not clean — review changes carefully"
fi

log "Python: $(python3 --version)"

# -----------------------------
# Step 1: Docstrings / JSDoc
# -----------------------------
log "Step 1/2 — Generating docstrings & JSDoc"
PY_ARGS=(--repo "$REPO_ROOT")

[[ "$DRY_RUN" == "1" ]] && PY_ARGS+=(--dry-run)

python3 "${SCRIPT_DIR}/gen_docstring_jsdocs.py" "${PY_ARGS[@]}"

# -----------------------------
# Step 2: Fractal docs
# -----------------------------
log "Step 2/2 — Generating fractal docs"
python3 "${SCRIPT_DIR}/gen_docs_fractal.py" "${PY_ARGS[@]}"

# -----------------------------
# Summary
# -----------------------------
log "Generation complete"
git status --porcelain || true
git diff --stat || true

log "Review changes with: git diff"