#!/usr/bin/env python3
# /// script
# dependencies = ["python-dotenv", "pyyaml"]
# ///
"""
gen_docs_fractal.py

Generate/update a fractal documentation tree under docs/ by reading:
- Python docstrings (module/class/function)
- TS/TSX JSDoc blocks (exported symbols)
- Existing README* files (README.md, readme.md, etc.) found in folders

Generated for project: tac-bootstrap

It produces ONE markdown per folder, named as the concatenation of the folder path:
  {path}.md

Example:
  src/backend/shared/domain  -> docs/src/backend/shared/domain.md
  src/backend/shared        -> docs/src/backend/shared.md
  src/backend              -> docs/src/backend.md
  src                      -> docs/src.md

Key behavior
------------
- Bottom-up: deeper folders are generated first, then parents (parents can summarize children)
- Merge strategy:
  - If a docs file already exists, it is "complemented" conservatively (default):
      * Frontmatter is normalized/updated
      * Existing body is preserved
      * Missing sections are appended
- Reads existing local README and uses it as authoritative context (not overwritten)
- Uses OpenAI API for summarization + structured doc generation
- Uses IDK vocabulary idea:
    * canonical IDK can be loaded from canonical_idk.yml if exists
    * local IDK is generated for each folder doc
    * IDK is keyword-only (no sentences)

Usage
-----
  # Using Claude Code CLI (recommended - no API key needed)
  python gen_docs_fractal.py \
    --repo . \
    --docs-root docs \
    --include-root tac_bootstrap_cli \
    --mode complement \
    --provider claude \
    --dry-run

  # Using OpenAI API (requires OPENAI_API_KEY)
  python gen_docs_fractal.py \
    --repo . \
    --docs-root docs \
    --include-root tac_bootstrap_cli \
    --mode complement \
    --provider api \
    --dry-run

Providers:
- claude: Uses Claude Code CLI (no API key needed, recommended)
- api: Uses OpenAI-compatible API (requires OPENAI_API_KEY environment variable)
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
import urllib.request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project-specific configuration from template
# Default app root: tac_bootstrap_cli
# Default language: Language.PYTHON
# Project name: tac-bootstrap

# ---------------------------
# Config: tags & IDK rules
# ---------------------------
TAG_TAXONOMY = [
    "expert:backend", "expert:frontend", "expert:data", "expert:infra", "expert:observability",
    "level:L1", "level:L2", "level:L3", "level:L4", "level:L5",
    "topic:auth", "topic:routing", "topic:logging", "topic:db", "topic:caching",
    "topic:queue", "topic:api", "topic:performance",
]

DEFAULT_FRONTMATTER_FIELDS = [
    "doc_type", "domain", "owner", "level", "tags", "idk", "related_code",
    "children", "source_readmes", "last_reviewed"
]

IDK_PREFIX = "IDK:"
IDK_RULES = (
    "IDK rules:\n"
    "- Output 5–12 INFORMATION DENSE KEYWORDS\n"
    "- NO sentences, NO verbs, NO filler words\n"
    "- Use canonical technical nouns; kebab-case; allow '-' and '/'\n"
    "- Prefer terms from the provided canonical/global IDK list when relevant\n"
)

IGNORE_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build",
    ".next", ".turbo", ".cache", "target", "vendor", ".idea", ".vscode",
    "templates",  # Exclude Jinja2 templates - they generate code, not source code
    ".mypy_cache", ".pytest_cache", ".ruff_cache",  # Cache directories
}

README_NAMES = {
    "readme.md", "README.md", "Readme.md", "README.MD",
    "readme.mdx", "README.mdx", "README.txt", "readme.txt"
}

# Language-based file extension defaults
DEFAULT_CODE_EXTENSIONS = [".py"]

# ---------------------------
# OpenAI-compatible client
# ---------------------------
class OpenAICompatClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        timeout_s: int = 180,
        temperature: float = 0.2,
        max_tokens: int = 1200,
        extra_headers_json: Optional[str] = None,
        extra_body_json: Optional[str] = None,
        endpoint: str = "chat/completions",
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout_s = timeout_s
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.endpoint = endpoint.lstrip("/")
        self.extra_headers = json.loads(extra_headers_json) if extra_headers_json else {}
        self.extra_body = json.loads(extra_body_json) if extra_body_json else {}

    def chat(self, messages: List[Dict[str, str]]) -> str:
        url = f"{self.base_url}/{self.endpoint}"
        body: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        body.update(self.extra_body)

        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST")
        req.add_header("Content-Type", "application/json")
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")
        for k, v in self.extra_headers.items():
            req.add_header(str(k), str(v))

        with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            payload = json.loads(raw)

        return payload["choices"][0]["message"]["content"]


# ---------------------------
# Claude Code CLI client
# ---------------------------
class ClaudeCodeClient:
    """Client that uses Claude Code CLI for LLM calls."""

    def __init__(
        self,
        model: str = "sonnet",
        timeout_s: int = 300,
        claude_path: Optional[str] = None,
    ):
        self.model = model
        self.timeout_s = timeout_s
        self.claude_path = claude_path or os.getenv("CLAUDE_CODE_PATH", "claude")

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Execute prompt via Claude Code CLI."""
        import subprocess
        import tempfile

        # Combine messages into a single prompt
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                prompt_parts.append(f"<system>\n{content}\n</system>\n")
            else:
                prompt_parts.append(content)

        full_prompt = "\n".join(prompt_parts)

        # Write prompt to temp file for large prompts
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(full_prompt)
            prompt_file = f.name

        try:
            cmd = [
                self.claude_path,
                "--model", self.model,
                "--dangerously-skip-permissions",
                "--print",
                "--output-format", "text",
            ]

            # Read prompt from file
            with open(prompt_file, 'r') as f:
                prompt_content = f.read()

            result = subprocess.run(
                cmd,
                input=prompt_content,
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
                cwd=os.getcwd(),
            )

            if result.returncode != 0:
                error_msg = result.stderr or "Unknown error"
                raise RuntimeError(f"Claude CLI failed: {error_msg}")

            return result.stdout.strip()

        finally:
            # Cleanup temp file
            try:
                os.unlink(prompt_file)
            except OSError:
                pass


# ---------------------------
# Basic filesystem helpers
# ---------------------------
def is_ignored_path(p: Path) -> bool:
    return any(part in IGNORE_DIRS for part in p.parts)

def repo_rel(repo: Path, p: Path) -> str:
    return str(p.resolve().relative_to(repo.resolve())).replace("\\", "/")

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")

def normalize_llm_output(s: str) -> str:
    s = s.strip()
    s = re.sub(r"^```[a-zA-Z0-9]*\n", "", s)
    s = re.sub(r"\n```$", "", s)
    return s.strip()


# ---------------------------
# Frontmatter parsing/writing (minimal YAML)
# ---------------------------
def split_frontmatter(md: str) -> Tuple[Optional[str], str]:
    lines = md.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, md
    # find second ---
    for i in range(1, min(len(lines), 400)):
        if lines[i].strip() == "---":
            fm = "\n".join(lines[1:i])
            body = "\n".join(lines[i+1:]).lstrip("\n")
            return fm, body
    return None, md

def parse_list_block(yaml_text: str, key: str) -> List[str]:
    """
    Parse:
      key:
        - a
        - b
    or key: [a, b]
    """
    # inline
    m = re.search(rf"(?m)^\s*{re.escape(key)}\s*:\s*\[(.*?)\]\s*$", yaml_text)
    if m:
        inside = m.group(1)
        parts = [p.strip().strip('"').strip("'") for p in inside.split(",")]
        return [p for p in parts if p]

    # block
    lines = yaml_text.splitlines()
    in_key = False
    base_indent = 0
    out: List[str] = []
    for ln in lines:
        if re.match(rf"^\s*{re.escape(key)}\s*:\s*$", ln):
            in_key = True
            base_indent = len(ln) - len(ln.lstrip())
            continue
        if in_key:
            indent = len(ln) - len(ln.lstrip())
            if ln.strip() and indent <= base_indent and re.match(r"^\s*[A-Za-z0-9_]+\s*:", ln):
                break
            m2 = re.match(r"^\s*-\s*(.+?)\s*$", ln)
            if m2:
                out.append(m2.group(1).strip().strip('"').strip("'"))
    return out

def parse_scalar(yaml_text: str, key: str) -> Optional[str]:
    m = re.search(rf"(?m)^\s*{re.escape(key)}\s*:\s*(.+?)\s*$", yaml_text)
    if not m:
        return None
    v = m.group(1).strip()
    # ignore lists
    if v.startswith("[") or v == "":
        return None
    return v.strip('"').strip("'")

def build_frontmatter(fields: Dict[str, Any]) -> str:
    """
    Write a stable frontmatter with canonical order.
    """
    def fmt_list(items: List[str], indent: int = 0) -> str:
        pad = " " * indent
        if not items:
            return f"{pad}[]"
        # block list
        out = []
        out.append("")
        for it in items:
            out.append(f"{pad}  - {it}")
        return "\n".join(out)

    out = ["---"]
    for k in DEFAULT_FRONTMATTER_FIELDS:
        if k not in fields:
            continue
        v = fields[k]
        if isinstance(v, list):
            out.append(f"{k}:{fmt_list(v)}")
        else:
            out.append(f"{k}: {v}")
    out.append("---")
    return "\n".join(out)

def detect_domain_from_relpath(relpath: str) -> str:
    # heuristic: first path segment
    parts = relpath.split("/")
    return parts[0] if parts else "unknown"

def load_canonical_idk_from_yaml(yaml_path: Path) -> Dict[str, List[str]]:
    """
    Load canonical IDK vocabulary from a YAML file.
    Expected format: domain -> list of keywords
    """
    import yaml
    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict):
                return {k: v if isinstance(v, list) else [] for k, v in data.items()}
    except Exception:
        pass
    return {}


# ---------------------------
# Code extraction: Python docstrings
# ---------------------------
@dataclass
class PyDocItem:
    kind: str  # module|class|function|method
    name: str
    doc: str

def extract_python_doc_items(py_path: Path) -> List[PyDocItem]:
    text = read_text(py_path)
    items: List[PyDocItem] = []
    try:
        tree = ast.parse(text)
    except Exception:
        return items

    module_doc = ast.get_docstring(tree)
    if module_doc:
        items.append(PyDocItem("module", py_path.stem, module_doc))

    class V(ast.NodeVisitor):
        def __init__(self):
            self.class_stack: List[str] = []

        def visit_ClassDef(self, node: ast.ClassDef):
            doc = ast.get_docstring(node) or ""
            name = ".".join(self.class_stack + [node.name]) if self.class_stack else node.name
            if doc:
                items.append(PyDocItem("class", name, doc))
            self.class_stack.append(node.name)
            self.generic_visit(node)
            self.class_stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef):
            doc = ast.get_docstring(node) or ""
            kind = "method" if self.class_stack else "function"
            name = ".".join(self.class_stack + [node.name]) if self.class_stack else node.name
            if doc:
                items.append(PyDocItem(kind, name, doc))
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            self.visit_FunctionDef(node)  # type: ignore[arg-type]

    V().visit(tree)
    return items


# ---------------------------
# Code extraction: TS/TSX JSDoc (exported symbols)
# ---------------------------
@dataclass
class TsDocItem:
    kind: str
    name: str
    doc: str

TS_EXPORT_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"^\s*export\s+class\s+([A-Za-z0-9_]+)"), "class"),
    (re.compile(r"^\s*export\s+interface\s+([A-Za-z0-9_]+)"), "interface"),
    (re.compile(r"^\s*export\s+type\s+([A-Za-z0-9_]+)"), "type"),
    (re.compile(r"^\s*export\s+function\s+([A-Za-z0-9_]+)\s*\("), "function"),
    (re.compile(r"^\s*export\s+const\s+([A-Za-z0-9_]+)\s*="), "const"),
]

JSDOC_START = re.compile(r"^\s*/\*\*")
JSDOC_END = re.compile(r".*\*/\s*$")

def extract_jsdoc_block(lines: List[str], symbol_line_idx: int, lookback: int = 40) -> Optional[str]:
    start_search = max(0, symbol_line_idx - lookback)
    for i in range(symbol_line_idx - 1, start_search - 1, -1):
        if JSDOC_END.match(lines[i]):
            for j in range(i, start_search - 1, -1):
                if JSDOC_START.match(lines[j]):
                    return "".join(lines[j:i+1])
    return None

def strip_jsdoc(block: str) -> str:
    # remove /** and */ and leading *
    body = block.strip()
    body = re.sub(r"^\s*/\*\*\s*", "", body)
    body = re.sub(r"\s*\*/\s*$", "", body)
    out_lines = []
    for ln in body.splitlines():
        ln = re.sub(r"^\s*\*\s?", "", ln)
        out_lines.append(ln.rstrip())
    return "\n".join(out_lines).strip()

def extract_ts_doc_items(ts_path: Path) -> List[TsDocItem]:
    text = read_text(ts_path)
    lines = text.splitlines(True)
    items: List[TsDocItem] = []
    for i, ln in enumerate(lines):
        for pat, kind in TS_EXPORT_PATTERNS:
            m = pat.match(ln)
            if m:
                name = m.group(1)
                block = extract_jsdoc_block([l.rstrip("\n") for l in lines], i)
                if block:
                    items.append(TsDocItem(kind, name, strip_jsdoc(block)))
    return items


# ---------------------------
# Folder scanning
# ---------------------------
def iter_target_folders(repo: Path, include_root: str) -> List[Path]:
    """
    Return all folders under include_root (including itself), bottom-up.
    """
    root = (repo / include_root).resolve()
    if not root.exists() or not root.is_dir():
        return []

    folders: List[Path] = []
    for p in root.rglob("*"):
        if p.is_dir() and not is_ignored_path(p):
            folders.append(p)
    folders.append(root)
    # deepest first
    folders.sort(key=lambda p: len(p.parts), reverse=True)
    return folders

def find_readmes_in_folder(folder: Path) -> List[Path]:
    found: List[Path] = []
    for name in README_NAMES:
        p = folder / name
        if p.exists() and p.is_file():
            found.append(p)
    return found

def list_child_docs(docs_root: Path, folder_doc_path: Path) -> List[str]:
    """
    children: list of docs paths directly under same prefix (one level deeper)
    Here we keep it simple: parent lists children docs that start with parent path + "/"
    and have exactly one more segment.
    """
    # docs_root is <repo>/docs
    # folder_doc_path is <repo>/docs/<...>.md
    # children are other md with same prefix path segments + 1
    repo = docs_root.parent
    folder_rel = repo_rel(repo, folder_doc_path)
    # docs/<X>.md -> docs/<X>
    base = folder_rel[:-3]  # strip .md
    base_parts = base.split("/")
    children: List[str] = []

    for p in docs_root.rglob("*.md"):
        rel = repo_rel(repo, p)
        if not rel.startswith("docs/"):
            continue
        if rel == folder_rel:
            continue
        rel_noext = rel[:-3]
        parts = rel_noext.split("/")
        # same prefix?
        if parts[:len(base_parts)] != base_parts:
            continue
        # exactly one deeper
        if len(parts) == len(base_parts) + 1:
            children.append(rel.replace("\\", "/"))
    children.sort()
    return children


# ---------------------------
# Prompting: build folder doc (robust model)
# ---------------------------
def prompt_folder_doc(
    folder_rel: str,
    include_root: str,
    readmes: List[Tuple[str, str]],
    py_items: List[PyDocItem],
    ts_items: List[TsDocItem],
    children_docs: List[str],
    existing_doc: Optional[str],
    canonical_idk: List[str],
    project_name: str,
) -> List[Dict[str, str]]:
    """
    Generate a COMPLETE markdown (frontmatter + body) OR a "patch" (for complement).
    We'll request full doc, but in complement mode we'll merge conservatively ourselves.
    """
    system = (
        f"You are a senior software documentation writer for tac-bootstrap project.\n"
        "You produce INFORMATION-DENSE documentation: minimal words, maximum signal.\n"
        "Never invent behavior not supported by docstrings/JSDoc/README context.\n"
        "Output must be valid markdown.\n"
        + IDK_RULES
    )

    readme_block = "\n\n".join(
        [f"README ({path}):\n---\n{content}\n---" for path, content in readmes]
    ) if readmes else "NONE"

    # To keep tokens controlled, we truncate docstrings/JSDoc collections
    def pack_items(items: List[Any], max_items: int = 80, max_chars_each: int = 800) -> str:
        chunks = []
        for it in items[:max_items]:
            doc = it.doc.strip()
            if len(doc) > max_chars_each:
                doc = doc[:max_chars_each] + "\n[TRUNCATED]"
            chunks.append(f"- {it.kind} {it.name}:\n{doc}")
        return "\n".join(chunks) if chunks else "NONE"

    py_block = pack_items(py_items)
    ts_block = pack_items(ts_items)

    existing_fm, existing_body = (None, None)
    if existing_doc:
        existing_fm, existing_body = split_frontmatter(existing_doc)

    # Ask for a structured doc with required sections & frontmatter
    user = f"""Create/Update folder documentation for a fractal docs tree.

Target folder:
- repo folder: {folder_rel}
- include_root: {include_root}

Canonical/global IDK terms for this domain (prefer when relevant):
{", ".join(canonical_idk) if canonical_idk else "NONE"}

Children docs (direct):
{json.dumps(children_docs, ensure_ascii=False, indent=2)}

Available README sources (authoritative):
{readme_block}

Python docstrings in this folder (authoritative):
{py_block}

TypeScript JSDoc in this folder (authoritative):
{ts_block}

Existing docs file content (if any):
---BEGIN EXISTING DOC---
{existing_doc if existing_doc else "NONE"}
---END EXISTING DOC---

Output requirements:
1) Output a COMPLETE markdown document (frontmatter + body).
2) Frontmatter MUST include these keys:
   - doc_type: folder
   - domain: a stable identifier derived from the folder path
   - owner: UNKNOWN if not inferable
   - level: one of L1..L5 (infer from depth; deeper => higher L number)
   - tags: choose only from allowed list: {", ".join(TAG_TAXONOMY)}
   - idk: 5–12 IDK keywords (kebab-case, no sentences)
   - related_code: list containing the folder path
   - children: list of direct children docs (from input)
   - source_readmes: list of README file paths used
   - last_reviewed: YYYY-MM-DD (write UNKNOWN if not inferable)
3) Body MUST be information-dense and include these sections (use headings):
   - Overview
   - Responsibilities
   - Key APIs / Components (bulleted)
   - Invariants & Contracts
   - Side Effects & IO
   - Operational Notes (perf, scaling, failure)
   - TODO / Gaps (only if gaps exist)
4) If existing doc has useful content, preserve it and integrate; do NOT delete valuable info.
5) Be conservative: if not sure, mark UNKNOWN or add to TODO/Gaps.

Return ONLY the markdown. No extra commentary.
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


# ---------------------------
# Merge strategy for complement
# ---------------------------
REQUIRED_SECTIONS = [
    "# Overview",
    "# Responsibilities",
    "# Key APIs / Components",
    "# Invariants & Contracts",
    "# Side Effects & IO",
    "# Operational Notes",
]

def normalize_section_headers(body: str) -> str:
    # Ensure sections are H1-ish (#). If model uses ##, we keep but validator uses substring.
    return body

def merge_frontmatter(existing_fm: Optional[str], generated_fm: str) -> str:
    """
    Merge frontmatter conservatively:
    - Use generated frontmatter as base
    - Preserve existing IDK keywords (don't regenerate)
    - Preserve existing tags if they exist
    - Update structural fields (children, related_code) from generated
    """
    if not existing_fm:
        return generated_fm

    # Parse existing frontmatter fields we want to preserve
    existing_idk = parse_list_block(existing_fm, "idk")
    existing_tags = parse_list_block(existing_fm, "tags")
    existing_owner = parse_scalar(existing_fm, "owner")
    existing_last_reviewed = parse_scalar(existing_fm, "last_reviewed")

    # Parse all generated fields
    gen_fields: Dict[str, Any] = {}
    for key in DEFAULT_FRONTMATTER_FIELDS:
        if key in ["idk", "tags", "children", "related_code", "source_readmes"]:
            gen_fields[key] = parse_list_block(generated_fm, key)
        else:
            val = parse_scalar(generated_fm, key)
            if val:
                gen_fields[key] = val

    # Apply preservation rules:
    # 1. Keep existing IDK if present (main fix for the user's issue)
    if existing_idk:
        gen_fields["idk"] = existing_idk

    # 2. Keep existing tags if present
    if existing_tags:
        gen_fields["tags"] = existing_tags

    # 3. Keep existing owner if not UNKNOWN
    if existing_owner and existing_owner != "UNKNOWN":
        gen_fields["owner"] = existing_owner

    # 4. Keep existing last_reviewed if not UNKNOWN
    if existing_last_reviewed and existing_last_reviewed != "UNKNOWN":
        gen_fields["last_reviewed"] = existing_last_reviewed

    return build_frontmatter(gen_fields)


def complement_doc(existing_md: str, generated_md: str) -> str:
    """
    Conservative merge:
    - Merge frontmatter conservatively (preserve IDK, tags, owner, last_reviewed)
    - Keep existing body verbatim
    - Append missing required sections from generated body (only those not present)
    """
    gen_fm, gen_body = split_frontmatter(generated_md)
    if not gen_fm:
        # if model failed, fallback to no changes
        return existing_md

    ex_fm, ex_body = split_frontmatter(existing_md)
    ex_body = ex_body or ""
    gen_body = gen_body or ""

    # Merge frontmatter conservatively (preserving existing IDK, tags, etc.)
    merged_fm = merge_frontmatter(ex_fm, gen_fm)

    # Append missing sections (naive: check header substring)
    merged_body = ex_body.rstrip() + "\n"
    for sec in REQUIRED_SECTIONS:
        if sec.lower() in ex_body.lower():
            continue
        # extract section from generated body
        section_text = extract_md_section(gen_body, sec)
        if section_text:
            merged_body += "\n\n" + section_text.strip() + "\n"

    # If existing body is empty, use generated
    if ex_body.strip() == "":
        merged_body = gen_body.strip() + "\n"

    merged = merged_fm + "\n\n" + merged_body.lstrip("\n")
    return merged

def extract_md_section(md_body: str, header: str) -> Optional[str]:
    """
    Extract a markdown section starting at header line until next header of same level (# ...)
    """
    lines = md_body.splitlines()
    target = header.strip()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip().lower() == target.lower():
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("# "):
            end = j
            break
    return "\n".join(lines[start:end]).strip()


# ---------------------------
# Main pipeline
# ---------------------------
def target_doc_path(repo: Path, docs_root: Path, folder: Path) -> Path:
    """
    docs/<folder_rel>.md
    """
    rel = repo_rel(repo, folder)
    return docs_root / f"{rel}.md"

def infer_level_from_depth(folder_rel: str, include_root: str) -> str:
    # depth within include_root, map to L1..L5
    parts = folder_rel.split("/")
    if parts and parts[0] == include_root:
        depth = len(parts) - 1
    else:
        depth = len(parts)
    # clamp to 1..5
    lvl = min(5, max(1, depth + 1))
    return f"L{lvl}"

def run() -> int:
    ap = argparse.ArgumentParser(description="Generate docs/ fractal markdown per folder using docstrings/JSDoc/README.")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--docs-root", default="docs", help="Docs output root folder")
    ap.add_argument("--include-root", default="tac_bootstrap_cli", help="Folder to document (e.g., src, apps, services)")
    ap.add_argument("--mode", choices=["overwrite", "complement"], default="complement")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--sleep-s", type=float, default=0.0)

    # Provider selection
    ap.add_argument("--provider", choices=["claude", "api"], default="claude",
                    help="LLM provider: 'claude' uses Claude Code CLI (no API key), 'api' uses OpenAI-compatible API")

    # Claude Code configuration
    ap.add_argument("--claude-model", default="sonnet", help="Claude model for CLI (sonnet, opus, haiku)")
    ap.add_argument("--claude-path", default=None, help="Path to claude CLI (default: from CLAUDE_CODE_PATH or 'claude')")

    # OpenAI configuration - environment variables take precedence
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    api_key = os.getenv("OPENAI_API_KEY", "")

    ap.add_argument("--base-url", default=base_url, help="OpenAI API base URL")
    ap.add_argument("--api-key", default=api_key, help="OpenAI API key")
    ap.add_argument("--model", default=model, help="OpenAI model name")
    ap.add_argument("--endpoint", default="chat/completions")
    ap.add_argument("--timeout-s", type=int, default=180)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--max-tokens", type=int, default=1200)
    ap.add_argument("--extra-headers-json", default=None)
    ap.add_argument("--extra-body-json", default=None)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    docs_root = (repo / args.docs_root).resolve()

    if not repo.exists():
        print(f"Repo not found: {repo}", file=sys.stderr)
        return 2

    # Language detection for graceful handling
    project_language = "Language.PYTHON"
    if project_language not in ['python', 'typescript', 'javascript']:
        print(f"WARNING: Language '{project_language}' not explicitly supported. Generating structure-based docs only.", file=sys.stderr)

    # Create client based on provider
    client: Union[OpenAICompatClient, ClaudeCodeClient]
    if args.provider == "claude":
        print(f"Using Claude Code CLI (model: {args.claude_model})")
        client = ClaudeCodeClient(
            model=args.claude_model,
            timeout_s=args.timeout_s,
            claude_path=args.claude_path,
        )
    else:
        # API mode requires API key
        if not args.api_key:
            print("ERROR: OPENAI_API_KEY environment variable is required for API provider.", file=sys.stderr)
            print("Set it in your .env file, export it, or use --provider claude instead.", file=sys.stderr)
            return 1
        print(f"Using OpenAI API (model: {args.model})")
        client = OpenAICompatClient(
            base_url=args.base_url,
            api_key=args.api_key,
            model=args.model,
            timeout_s=args.timeout_s,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            extra_headers_json=args.extra_headers_json,
            extra_body_json=args.extra_body_json,
            endpoint=args.endpoint,
        )

    # Canonical/global IDK from canonical_idk.yml if exists (optional, silent)
    canonical_idk_path = repo / "canonical_idk.yml"
    canonical_idk_by_domain: Dict[str, List[str]] = {}
    if canonical_idk_path.exists():
        try:
            canonical_idk_by_domain = load_canonical_idk_from_yaml(canonical_idk_path)
        except Exception:
            # Silent failure - IDK vocabulary is optional
            pass

    folders = iter_target_folders(repo, args.include_root)
    if not folders:
        print(f"No folders found under: {args.include_root}", file=sys.stderr)
        return 2

    changed = 0
    for folder in folders:
        folder_rel = repo_rel(repo, folder)
        out_path = target_doc_path(repo, docs_root, folder)

        # Collect README sources
        readmes = []
        for rp in find_readmes_in_folder(folder):
            readmes.append((repo_rel(repo, rp), read_text(rp)))

        # Collect docstrings/JSDoc from code files directly in this folder (not recursive)
        py_items: List[PyDocItem] = []
        ts_items: List[TsDocItem] = []
        for f in folder.iterdir():
            if not f.is_file():
                continue
            if f.suffix == ".py" and project_language in ['python', 'unknown']:
                py_items.extend(extract_python_doc_items(f))
            elif f.suffix in {".ts", ".tsx"} and not f.name.endswith(".d.ts") and project_language in ['typescript', 'javascript', 'unknown']:
                ts_items.extend(extract_ts_doc_items(f))

        # Children docs
        children = list_child_docs(docs_root, out_path)

        # Domain for canonical IDK: first segment under include_root if possible, else first segment
        # Example: src/backend/... => domain backend
        dom = "unknown"
        parts = folder_rel.split("/")
        if len(parts) >= 2 and parts[0] == args.include_root:
            dom = parts[1]
        elif parts:
            dom = parts[0]
        canonical_idk = canonical_idk_by_domain.get(dom, [])

        existing_doc = read_text(out_path) if out_path.exists() else None

        msgs = prompt_folder_doc(
            folder_rel=folder_rel,
            include_root=args.include_root,
            readmes=readmes,
            py_items=py_items,
            ts_items=ts_items,
            children_docs=children,
            existing_doc=existing_doc,
            canonical_idk=canonical_idk,
            project_name="tac-bootstrap",
        )
        generated = normalize_llm_output(client.chat(msgs))

        # Ensure it starts with frontmatter
        if not generated.lstrip().startswith("---"):
            # fail safe: wrap into a minimal doc
            level = infer_level_from_depth(folder_rel, args.include_root)
            fm = build_frontmatter({
                "doc_type": "folder",
                "domain": folder_rel.replace("/", "."),
                "owner": "UNKNOWN",
                "level": level,
                "tags": ["level:" + level],
                "idk": [],
                "related_code": [folder_rel],
                "children": children,
                "source_readmes": [p for p, _ in readmes],
                "last_reviewed": "UNKNOWN",
            })
            generated = fm + "\n\n# Overview\n\nUNKNOWN\n"

        # Merge based on mode
        final_md = generated
        if existing_doc and args.mode == "complement":
            final_md = complement_doc(existing_doc, generated)

        # Write (or show diff-like summary)
        if not existing_doc or final_md != existing_doc:
            changed += 1
            print(("DRY-RUN would write: " if args.dry_run else "Writing: ") + repo_rel(repo, out_path))
            if not args.dry_run:
                write_text(out_path, final_md)

        if args.sleep_s > 0:
            time.sleep(args.sleep_s)

    print(f"\nDone. Docs changed: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
