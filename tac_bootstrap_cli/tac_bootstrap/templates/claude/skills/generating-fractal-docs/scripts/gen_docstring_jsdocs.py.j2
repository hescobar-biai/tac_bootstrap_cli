#!/usr/bin/env python3
"""
docgen_openai_compatible_v3_idk_local.py

Adds "local IDK" generation for Python docstrings and TS JSDoc, leveraging:
- Global/canonical IDK from docs/**/*.md frontmatter (idk: [...])
- Domain registries (optional): docs/idk/domains/<domain>.yml (not required in this v3)
- Conservative "complement" mode to avoid losing existing docs.

Modes:
- add: add docs only if missing
- overwrite: replace docs entirely (dangerous)
- complement: append missing sections without deleting anything

IDK concept:
- IDK line must be 5–12 domain keywords (kebab-case), NO sentences, NO verbs.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import sys
import time
import urllib.request
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from pydantic import BaseModel

DEFAULT_TAG_TAXONOMY = [
    "expert:backend", "expert:frontend", "expert:data", "expert:infra", "expert:observability",
    "level:L1", "level:L2", "level:L3", "level:L4", "level:L5",
    "topic:auth", "topic:routing", "topic:logging", "topic:db", "topic:caching",
    "topic:queue", "topic:api", "topic:performance",
]

TAG_TAXONOMY: list[str] = list(DEFAULT_TAG_TAXONOMY)


def load_tag_taxonomy(path: str | None) -> list[str]:
    """Load tag taxonomy from a JSON file (array of strings) or fall back to defaults."""
    if not path:
        return list(DEFAULT_TAG_TAXONOMY)
    p = Path(path)
    if not p.exists():
        print(f"Warning: tag taxonomy file not found: {path}, using defaults", file=sys.stderr)
        return list(DEFAULT_TAG_TAXONOMY)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, list) and all(isinstance(t, str) for t in data):
            return data
        print(f"Warning: tag taxonomy file must contain a JSON array of strings: {path}, using defaults", file=sys.stderr)
        return list(DEFAULT_TAG_TAXONOMY)
    except Exception as e:
        print(f"Warning: failed to load tag taxonomy file {path}: {e}, using defaults", file=sys.stderr)
        return list(DEFAULT_TAG_TAXONOMY)

IDK_PREFIX = "IDK:"
DEFAULT_IDK_RULES = (
    "IDK rules:\n"
    "- Provide 5–12 INFORMATION DENSE KEYWORDS\n"
    "- NO sentences, NO verbs, NO filler words\n"
    "- Use canonical technical nouns; kebab-case\n"
    "- Prefer terms from the provided canonical/global IDK list when relevant\n"
    "- If uncertain, choose broader canonical terms\n"
)

IGNORE_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build",
    ".next", ".turbo", ".cache", "target", "vendor", ".idea", ".vscode"
}


# ---------------------------
# OpenAI-compatible client
# ---------------------------
class OpenAICompatClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        timeout_s: int = 120,
        temperature: float = 0.2,
        max_tokens: int = 520,
        extra_headers_json: str | None = None,
        extra_body_json: str | None = None,
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

    def chat(self, messages: list[dict[str, str]]) -> str:
        url = f"{self.base_url}/{self.endpoint}"
        body: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        body.update(self.extra_body)

        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
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
# Helpers
# ---------------------------
def is_ignored_path(p: Path) -> bool:
    return any(part in IGNORE_DIRS for part in p.parts)

def repo_rel(repo: Path, p: Path) -> str:
    return str(p.resolve().relative_to(repo.resolve())).replace("\\", "/")

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def write_text(p: Path, s: str) -> None:
    p.write_text(s, encoding="utf-8")

def backup_file(p: Path) -> None:
    bak = p.with_suffix(p.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(p, bak)

def normalize_llm_output(s: str) -> str:
    s = s.strip()
    s = re.sub(r"^```[a-zA-Z0-9]*\n", "", s)
    s = re.sub(r"\n```$", "", s)
    return s.strip()

def iter_code_files(repo: Path, include_glob: str | None = None) -> Iterable[Path]:
    if include_glob:
        for p in repo.glob(include_glob):
            if p.is_file() and not is_ignored_path(p):
                yield p
        return
    for p in repo.rglob("*"):
        if not p.is_file() or is_ignored_path(p):
            continue
        if p.suffix in {".py", ".ts", ".tsx"} and not p.name.endswith(".d.ts"):
            yield p

def extract_window(text: str, start_line: int, max_lines: int) -> str:
    lines = text.splitlines()
    start = max(0, start_line - 1)
    end = min(len(lines), start + max_lines)
    return "\n".join(lines[start:end])


# ---------------------------
# Docs frontmatter IDK loader
# ---------------------------
FRONTMATTER_RE = re.compile(r"^---\s*$", re.M)

def parse_frontmatter(text: str) -> str | None:
    """
    Return raw YAML frontmatter (string) or None.
    """
    # Find first two '---' lines
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, min(len(lines), 200)):  # keep cheap
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return None

def parse_idk_from_frontmatter_yaml(yaml_text: str) -> list[str]:
    """
    Minimal parser for:
      idk:
        - term
        - term2
    or:
      idk: [a, b]
    """
    idk: list[str] = []
    # inline list
    m = re.search(r"(?m)^\s*idk\s*:\s*\[(.*?)\]\s*$", yaml_text)
    if m:
        inside = m.group(1)
        parts = [p.strip().strip('"').strip("'") for p in inside.split(",")]
        return [p for p in parts if p]

    # block list
    lines = yaml_text.splitlines()
    in_idk = False
    base_indent = None
    for ln in lines:
        if re.match(r"^\s*idk\s*:\s*$", ln):
            in_idk = True
            base_indent = len(ln) - len(ln.lstrip())
            continue
        if in_idk:
            # end if indentation goes back or line is a new key
            indent = len(ln) - len(ln.lstrip())
            if ln.strip() and indent <= (base_indent or 0) and re.match(r"^\s*[A-Za-z0-9_]+\s*:", ln):
                break
            m2 = re.match(r"^\s*-\s*(.+?)\s*$", ln)
            if m2:
                term = m2.group(1).strip().strip('"').strip("'")
                if term:
                    idk.append(term)
    return idk

def detect_domain_from_path(relpath: str) -> str:
    """
    Heuristic:
    - docs/<domain>/... => <domain>
    - src/<domain>/...  => <domain>
    - services/<name>/... => services
    else => "unknown"
    """
    parts = relpath.split("/")
    if len(parts) >= 2 and parts[0] in {"docs", "src"}:
        return parts[1]
    if len(parts) >= 2 and parts[0] in {"services", "apps", "packages"}:
        return parts[0]
    return "unknown"

def build_docs_idk_index(repo: Path, docs_dir: str = "docs") -> dict[str, list[str]]:
    """
    Index canonical/global IDK by "domain" based on <docs-dir>/<domain>/**/*.md frontmatter.
    Returns domain -> merged unique idk terms (order preserved).
    """
    out: dict[str, list[str]] = {}
    seen: dict[str, set] = {}

    docs = repo / docs_dir
    if not docs.exists():
        return out

    for p in docs.rglob("*.md"):
        if is_ignored_path(p):
            continue
        rel = repo_rel(repo, p)
        dom = detect_domain_from_path(rel)
        fm = parse_frontmatter(read_text(p))
        if not fm:
            continue
        terms = parse_idk_from_frontmatter_yaml(fm)
        if not terms:
            continue
        if dom not in out:
            out[dom] = []
            seen[dom] = set()
        for t in terms:
            if t not in seen[dom]:
                seen[dom].add(t)
                out[dom].append(t)
    return out


# ---------------------------
# Python symbol detection + docstring manipulation
# ---------------------------
class PyTarget(BaseModel):
    kind: str
    name: str
    lineno: int
    indent: str

def parse_python_targets(text: str) -> list[PyTarget]:
    out: list[PyTarget] = []
    try:
        tree = ast.parse(text)
    except Exception:
        return out

    lines = text.splitlines()

    class V(ast.NodeVisitor):
        def __init__(self):
            self.class_stack: list[str] = []

        def _indent(self, lineno: int) -> str:
            s = lines[lineno - 1] if 1 <= lineno <= len(lines) else ""
            return s[: len(s) - len(s.lstrip(" \t"))]

        def visit_ClassDef(self, node: ast.ClassDef):
            name = ".".join(self.class_stack + [node.name]) if self.class_stack else node.name
            out.append(PyTarget("class", name, node.lineno, self._indent(node.lineno)))
            self.class_stack.append(node.name)
            self.generic_visit(node)
            self.class_stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef):
            kind = "method" if self.class_stack else "function"
            name = ".".join(self.class_stack + [node.name]) if self.class_stack else node.name
            out.append(PyTarget(kind, name, node.lineno, self._indent(node.lineno)))
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
            self.visit_FunctionDef(node)  # type: ignore[arg-type]

    V().visit(tree)
    return out

TRIPLE_QUOTE_RE = re.compile(r'^(\s*)([rubfRUBF]{0,2})("""|\'\'\')')

def find_python_docstring_block(text: str, def_line_no: int) -> tuple[int, int, str, str] | None:
    """
    Return (start_idx, end_idx_excl, quote, body)
    """
    lines = text.splitlines(True)
    i = def_line_no - 1
    if not (0 <= i < len(lines)):
        return None
    j = i
    while j < len(lines) and not lines[j].strip().endswith(":"):
        j += 1
    j += 1

    while j < len(lines):
        s = lines[j].strip()
        if not s or s.startswith("#"):
            j += 1
            continue
        break
    if j >= len(lines):
        return None
    m = TRIPLE_QUOTE_RE.match(lines[j])
    if not m:
        return None
    quote = m.group(3)
    start = j

    after = lines[j][m.end():]
    if quote in after:
        body = after.split(quote, 1)[0]
        return (start, start + 1, quote, body.strip("\n"))

    k = start + 1
    body_lines = [lines[start][m.end():]]
    while k < len(lines):
        if quote in lines[k]:
            before, _ = lines[k].split(quote, 1)
            body_lines.append(before)
            end = k + 1
            body = "".join(body_lines)
            return (start, end, quote, body.strip("\n"))
        body_lines.append(lines[k])
        k += 1
    return None

def replace_python_docstring_body(text: str, start: int, end: int, quote: str, new_body: str) -> str:
    lines = text.splitlines(True)
    indent_match = TRIPLE_QUOTE_RE.match(lines[start])
    indent = indent_match.group(1) if indent_match else ""
    prefix = indent_match.group(2) if indent_match else ""
    inner_indent = indent
    rebuilt = []
    rebuilt.append(f"{inner_indent}{prefix}{quote}\n")
    for ln in new_body.strip("\n").splitlines():
        rebuilt.append(f"{inner_indent}{ln.rstrip()}\n")
    rebuilt.append(f"{inner_indent}{quote}\n")
    return "".join(lines[:start] + rebuilt + lines[end:])

def insert_python_docstring(text: str, target: PyTarget, body: str) -> str:
    lines = text.splitlines(True)
    i = target.lineno - 1
    if not (0 <= i < len(lines)):
        return text
    j = i
    while j < len(lines) and not lines[j].strip().endswith(":"):
        j += 1
    j += 1
    inner_indent = target.indent + " " * 4
    body = body.strip("\n").replace('"""', r'\"\"\"')
    doc = [f'{inner_indent}"""\n']
    for ln in body.splitlines():
        doc.append(f"{inner_indent}{ln.rstrip()}\n")
    doc.append(f'{inner_indent}"""\n')
    return "".join(lines[:j] + doc + lines[j:])


# ---------------------------
# TS: JSDoc manipulation
# ---------------------------
JSDOC_START = re.compile(r"^\s*/\*\*")
JSDOC_END = re.compile(r".*\*/\s*$")

TS_SYMBOL_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^\s*export\s+class\s+([A-Za-z0-9_]+)"), "class"),
    (re.compile(r"^\s*export\s+interface\s+([A-Za-z0-9_]+)"), "interface"),
    (re.compile(r"^\s*export\s+type\s+([A-Za-z0-9_]+)"), "type"),
    (re.compile(r"^\s*export\s+function\s+([A-Za-z0-9_]+)\s*\("), "function"),
    (re.compile(r"^\s*export\s+const\s+([A-Za-z0-9_]+)\s*="), "const"),
]

class TSTarget(BaseModel):
    kind: str
    name: str
    line: int

def find_jsdoc_block_above(lines: list[str], symbol_line_idx: int, lookback: int = 30) -> tuple[int, int, str] | None:
    start_search = max(0, symbol_line_idx - lookback)
    for i in range(symbol_line_idx - 1, start_search - 1, -1):
        if JSDOC_END.match(lines[i].rstrip("\n")):
            for j in range(i, start_search - 1, -1):
                if JSDOC_START.match(lines[j].rstrip("\n")):
                    block = "".join(lines[j:i+1])
                    return (j, i + 1, block)
    return None

def parse_ts_targets(text: str) -> list[TSTarget]:
    out: list[TSTarget] = []
    lines = text.splitlines(True)
    for i, line in enumerate(lines):
        for pat, kind in TS_SYMBOL_PATTERNS:
            m = pat.match(line)
            if m:
                out.append(TSTarget(kind, m.group(1), i + 1))
    return out

def insert_ts_jsdoc(text: str, symbol_line: int, jsdoc_block: str) -> str:
    lines = text.splitlines(True)
    idx = symbol_line - 1
    block = jsdoc_block.strip("\n")
    if not block.startswith("/**"):
        block = "/**\n" + block + "\n*/"
    if not block.endswith("\n"):
        block += "\n"
    return "".join(lines[:idx] + [block] + lines[idx:])

def replace_ts_jsdoc(text: str, start: int, end: int, new_block: str) -> str:
    lines = text.splitlines(True)
    block = new_block.strip("\n")
    if not block.startswith("/**"):
        block = "/**\n" + block + "\n*/"
    if not block.endswith("\n"):
        block += "\n"
    return "".join(lines[:start] + [block] + lines[end:])


# ---------------------------
# Prompts with local IDK
# ---------------------------
PY_REQUIRED = ["Purpose:", "Tags:", "Ownership:", "Invariants:", "Side effects:", "Inputs:", "Outputs:", "Failure modes:", IDK_PREFIX]
TS_REQUIRED = ["Purpose:", "Tags:", "Ownership:", "Invariants:", "Side effects:", "Failure modes:", IDK_PREFIX]

def missing_sections(existing: str, required: list[str]) -> list[str]:
    lower = existing.lower()
    miss = [sec for sec in required if sec.lower() not in lower]
    return miss

def prompt_python_missing(existing: str, missing: list[str], file_path: str, name: str, kind: str, snippet: str, canonical_idk: list[str]) -> list[dict[str, str]]:
    system = (
        "You generate ONLY missing sections to append to an existing Python docstring body.\n"
        "Do NOT modify existing text. Do NOT repeat existing sections.\n"
        "Return ONLY the lines to append (no triple quotes, no markdown).\n"
        + DEFAULT_IDK_RULES
    )
    user = f"""Existing docstring BODY (reference only):
---BEGIN EXISTING---
{existing.strip()}
---END EXISTING---

Missing sections to generate (ONLY these):
{chr(10).join('- ' + m for m in missing)}

Allowed tags: {", ".join(TAG_TAXONOMY)}

Canonical/global IDK terms for this domain (prefer when relevant):
{", ".join(canonical_idk) if canonical_idk else "NONE"}

Symbol: {name} ({kind})
File: {file_path}

Code snippet (authoritative):
{snippet}

IMPORTANT:
- For {IDK_PREFIX} output: produce 5–12 comma-separated keywords ONLY (no sentences).
Example: {IDK_PREFIX} cqrs, outbox, idempotency, transactions, correlation-id
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]

def prompt_python_full(file_path: str, name: str, kind: str, snippet: str, canonical_idk: list[str]) -> list[dict[str, str]]:
    system = (
        "You generate Python docstring bodies (no triple quotes). Be accurate and conservative.\n"
        "Do NOT invent behavior not visible in the code snippet.\n"
        + DEFAULT_IDK_RULES
    )
    user = f"""Create a Python docstring BODY.

Constraints:
- Use only allowed tags: {", ".join(TAG_TAXONOMY)}
- Include {IDK_PREFIX} once (5–12 keywords, no sentences).

Canonical/global IDK terms for this domain (prefer when relevant):
{", ".join(canonical_idk) if canonical_idk else "NONE"}

Template:
Purpose: <1 line>
Tags: <comma-separated allowed tags>
Ownership: <layer + MUST NOTs>
Invariants:
  - MUST/MUST NOT ...
Side effects:
  - ...
Inputs:
  - ...
Outputs:
  - ...
Failure modes:
  - ...
{IDK_PREFIX} <k1>, <k2>, ...

Symbol: {name} ({kind})
File: {file_path}

Code snippet:
{snippet}
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]

def prompt_ts_missing(existing_block: str, missing: list[str], file_path: str, name: str, kind: str, snippet: str, canonical_idk: list[str]) -> list[dict[str, str]]:
    system = (
        "You generate ONLY missing lines to append INSIDE an existing JSDoc block.\n"
        "Do NOT modify existing lines. Do NOT repeat existing sections.\n"
        "Return ONLY new JSDoc lines starting with ' * '. No /** */.\n"
        + DEFAULT_IDK_RULES
    )
    user = f"""Existing JSDoc (reference only):
---BEGIN EXISTING---
{existing_block.strip()}
---END EXISTING---

Missing items to generate (ONLY these):
{chr(10).join('- ' + m for m in missing)}

Allowed tags: {", ".join(TAG_TAXONOMY)}

Canonical/global IDK terms for this domain (prefer when relevant):
{", ".join(canonical_idk) if canonical_idk else "NONE"}

Symbol: {name} ({kind})
File: {file_path}

Code snippet:
{snippet}

IMPORTANT:
- For {IDK_PREFIX} line: output exactly like:
 * {IDK_PREFIX} routing, api, validation, structured-logging, correlation-id
(no sentences)
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]

def prompt_ts_full(file_path: str, name: str, kind: str, snippet: str, canonical_idk: list[str]) -> list[dict[str, str]]:
    system = (
        "You generate complete JSDoc blocks. Be accurate and conservative.\n"
        "Return ONLY a JSDoc block including /** */.\n"
        + DEFAULT_IDK_RULES
    )
    user = f"""Create a JSDoc block.

Constraints:
- Must include: Purpose, Tags, Ownership, Invariants, Side effects, Failure modes, {IDK_PREFIX}
- Use only allowed tags: {", ".join(TAG_TAXONOMY)}
- {IDK_PREFIX}: 5–12 keywords, no sentences.

Canonical/global IDK terms for this domain (prefer when relevant):
{", ".join(canonical_idk) if canonical_idk else "NONE"}

Symbol: {name} ({kind})
File: {file_path}

Code snippet:
{snippet}
"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


# ---------------------------
# Processing
# ---------------------------
def process_python_file(client: OpenAICompatClient, repo: Path, path: Path, mode: str, dry_run: bool, backup: bool, snippet_lines: int, sleep_s: float, domain_idk: dict[str, list[str]]) -> tuple[bool, int]:
    text = read_text(path)
    rel = repo_rel(repo, path)
    dom = detect_domain_from_path(rel)
    canonical_idk = domain_idk.get(dom, [])

    targets = parse_python_targets(text)
    if not targets:
        return False, 0
    targets.sort(key=lambda t: t.lineno, reverse=True)

    changed = False
    edits = 0

    for t in targets:
        block = find_python_docstring_block(text, t.lineno)
        has_doc = block is not None

        if mode == "add" and has_doc:
            continue

        snippet = extract_window(text, t.lineno, snippet_lines)

        if mode == "overwrite":
            msgs = prompt_python_full(rel, t.name, t.kind, snippet, canonical_idk)
            body = normalize_llm_output(client.chat(msgs))
            if IDK_PREFIX.lower() not in body.lower():
                body = body.rstrip() + f"\n{IDK_PREFIX} unknown\n"
            if has_doc:
                s, e, quote, _ = block
                new_text = replace_python_docstring_body(text, s, e, quote, body)
            else:
                new_text = insert_python_docstring(text, t, body)

        elif mode == "complement" and has_doc:
            s, e, quote, existing_body = block
            miss = missing_sections(existing_body, PY_REQUIRED)
            if not miss:
                continue
            msgs = prompt_python_missing(existing_body, miss, rel, t.name, t.kind, snippet, canonical_idk)
            addition = normalize_llm_output(client.chat(msgs))
            merged = existing_body.rstrip() + "\n\n" + addition.strip() + "\n"
            new_text = replace_python_docstring_body(text, s, e, quote, merged)

        else:
            # add missing or complement missing doc => full create
            msgs = prompt_python_full(rel, t.name, t.kind, snippet, canonical_idk)
            body = normalize_llm_output(client.chat(msgs))
            if IDK_PREFIX.lower() not in body.lower():
                body = body.rstrip() + f"\n{IDK_PREFIX} unknown\n"
            new_text = insert_python_docstring(text, t, body)

        if new_text != text:
            text = new_text
            changed = True
            edits += 1

        if sleep_s > 0:
            time.sleep(sleep_s)

    if changed and not dry_run:
        if backup:
            backup_file(path)
        write_text(path, text)

    return changed, edits


def process_ts_file(client: OpenAICompatClient, repo: Path, path: Path, mode: str, dry_run: bool, backup: bool, snippet_lines: int, sleep_s: float, domain_idk: dict[str, list[str]]) -> tuple[bool, int]:
    text = read_text(path)
    rel = repo_rel(repo, path)
    dom = detect_domain_from_path(rel)
    canonical_idk = domain_idk.get(dom, [])

    lines = text.splitlines(True)
    targets = parse_ts_targets(text)
    if not targets:
        return False, 0
    targets.sort(key=lambda t: t.line, reverse=True)

    changed = False
    edits = 0

    for t in targets:
        idx = t.line - 1
        js = find_jsdoc_block_above(lines, idx)
        has_jsdoc = js is not None

        if mode == "add" and has_jsdoc:
            continue

        snippet = extract_window(text, t.line, snippet_lines)

        if mode == "overwrite":
            msgs = prompt_ts_full(rel, t.name, t.kind, snippet, canonical_idk)
            block = normalize_llm_output(client.chat(msgs))
            if IDK_PREFIX.lower() not in block.lower():
                # minimal fix
                block = block.rstrip() + f"\n * {IDK_PREFIX} unknown\n */"
            if has_jsdoc:
                s, e, _ = js
                new_text = replace_ts_jsdoc(text, s, e, block)
            else:
                new_text = insert_ts_jsdoc(text, t.line, block)

        elif mode == "complement" and has_jsdoc:
            s, e, existing_block = js
            miss = missing_sections(existing_block, TS_REQUIRED)
            if not miss:
                continue
            msgs = prompt_ts_missing(existing_block, miss, rel, t.name, t.kind, snippet, canonical_idk)
            addition = normalize_llm_output(client.chat(msgs))

            existing_lines = existing_block.splitlines(True)
            insert_at = None
            for i in range(len(existing_lines) - 1, -1, -1):
                if "*/" in existing_lines[i]:
                    insert_at = i
                    break
            if insert_at is None:
                continue

            add_lines = []
            for ln in addition.splitlines():
                ln = ln.rstrip()
                if not ln:
                    continue
                if not ln.lstrip().startswith("*"):
                    add_lines.append(f" * {ln}\n")
                else:
                    content = ln.lstrip().lstrip("*").lstrip()
                    add_lines.append(f" * {content}\n")

            merged_block = "".join(existing_lines[:insert_at] + [" *\n"] + add_lines + existing_lines[insert_at:])
            new_text = replace_ts_jsdoc(text, s, e, merged_block)

        else:
            msgs = prompt_ts_full(rel, t.name, t.kind, snippet, canonical_idk)
            block = normalize_llm_output(client.chat(msgs))
            new_text = insert_ts_jsdoc(text, t.line, block)

        if new_text != text:
            text = new_text
            lines = text.splitlines(True)
            changed = True
            edits += 1

        if sleep_s > 0:
            time.sleep(sleep_s)

    if changed and not dry_run:
        if backup:
            backup_file(path)
        write_text(path, text)

    return changed, edits


def main() -> int:
    ap = argparse.ArgumentParser(description="Docstring/JSDoc generator w/ local IDK using OpenAI-compatible APIs.")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--include-glob", default=None)
    ap.add_argument("--base-url", default="http://localhost:11434/v1/", required=True)
    ap.add_argument("--api-key", default="ollama")
    ap.add_argument("--model", default="cogito:3b")
    ap.add_argument("--endpoint", default="chat/completions")
    ap.add_argument("--timeout-s", type=int, default=120)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--max-tokens", type=int, default=520)
    ap.add_argument("--extra-headers-json", default=None)
    ap.add_argument("--extra-body-json", default=None)

    ap.add_argument("--mode", choices=["add", "overwrite", "complement"], default="complement")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-backup", action="store_true")
    ap.add_argument("--snippet-lines", type=int, default=220)
    ap.add_argument("--sleep-s", type=float, default=0.0)
    ap.add_argument("--tag-taxonomy-file", default=None, help="Path to JSON file with custom tag taxonomy (array of strings)")
    ap.add_argument("--docs-dir", default="docs", help="Docs directory name for IDK index (default: docs)")
    args = ap.parse_args()

    global TAG_TAXONOMY
    TAG_TAXONOMY = load_tag_taxonomy(args.tag_taxonomy_file)

    repo = Path(args.repo).resolve()
    if not repo.exists() or not repo.is_dir():
        print(f"Repo not found: {repo}", file=sys.stderr)
        return 2

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

    # Build canonical/global IDK index from docs frontmatter
    domain_idk = build_docs_idk_index(repo, docs_dir=args.docs_dir)

    files = list(iter_code_files(repo, include_glob=args.include_glob))
    if not files:
        print("No code files found.")
        return 0

    backup = not args.no_backup
    total_changed = 0
    total_edits = 0

    print(f"Mode: {args.mode}")
    print(f"Loaded canonical IDK from {args.docs_dir}/ for domains: {', '.join(sorted(domain_idk.keys())) or 'none'}")
    print(f"Scanning {len(files)} file(s)...")

    for p in files:
        try:
            if p.suffix == ".py":
                changed, edits = process_python_file(client, repo, p, args.mode, args.dry_run, backup, args.snippet_lines, args.sleep_s, domain_idk)
            elif p.suffix in {".ts", ".tsx"}:
                changed, edits = process_ts_file(client, repo, p, args.mode, args.dry_run, backup, args.snippet_lines, args.sleep_s, domain_idk)
            else:
                continue

            if changed:
                total_changed += 1
                total_edits += edits
                action = "DRY-RUN would change" if args.dry_run else "Changed"
                print(f"{action}: {repo_rel(repo, p)}  (+{edits} edit(s))")

        except Exception as e:
            print(f"ERROR processing {repo_rel(repo, p)}: {e}", file=sys.stderr)

    print("\nDone.")
    print(f"Files changed: {total_changed}")
    print(f"Edits applied: {total_edits}")
    if args.dry_run:
        print("Dry-run mode: no files were modified.")
    else:
        if backup:
            print("Backups: created *.bak next to modified files (first time only).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
