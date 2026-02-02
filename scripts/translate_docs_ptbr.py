#!/usr/bin/env python
"""
Translate all Markdown/MDX files under docs/ into Brazilian Portuguese.

Outputs mirrored tree to docs/pt-br. Code fences/frontmatter are left intact,
inline code and link targets are preserved, while surrounding prose is translated.
Uses argostranslate for offline-ish machine translation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import re

import argostranslate.package
import argostranslate.translate


DOCS_ROOT = Path(__file__).resolve().parent.parent / "docs"
TARGET_ROOT = DOCS_ROOT / "pt-br"
VALID_EXTENSIONS = {".md", ".mdx"}


def ensure_translation_pack() -> None:
    """Install en->pt package if missing."""
    installed = argostranslate.translate.get_installed_languages()
    en_lang = next((lang for lang in installed if lang.code == "en"), None)
    if en_lang and any(tr.to_lang.code == "pt" for tr in en_lang.translations_from):
        return

    argostranslate.package.update_package_index()
    available = argostranslate.package.get_available_packages()
    pkg = next(pkg for pkg in available if pkg.from_code == "en" and pkg.to_code == "pt")
    path = pkg.download()
    argostranslate.package.install_from_path(path)


LINK_PATTERN = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")
INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")
HTML_TAG_PATTERN = re.compile(r"<[^>\n]+>")


def _link_token(idx: int) -> str:
    return f"OCTXLINK{idx}"


def _code_token(idx: int) -> str:
    return f"OCTXCODE{idx}"


def _html_token(idx: int) -> str:
    return f"OCTXHTML{idx}"


def mask_links(text: str) -> tuple[str, list[str]]:
    targets: list[str] = []

    def _sub(match: re.Match[str]) -> str:
        idx = len(targets)
        targets.append(match.group(2))
        return f"{match.group(1)}({_link_token(idx)})"

    return LINK_PATTERN.sub(_sub, text), targets


def unmask_links(text: str, targets: list[str]) -> str:
    for idx, target in enumerate(targets):
        token = _link_token(idx)
        pattern = re.compile(rf"[<\[\(\{{]*\s*OCTX\s*LINK\s*{idx}\s*[>\]\)\}}]*", re.IGNORECASE)
        text = pattern.sub(target, text)
    return text


def mask_inline_code(text: str) -> tuple[str, list[str]]:
    snippets: list[str] = []

    def _sub(match: re.Match[str]) -> str:
        idx = len(snippets)
        snippets.append(match.group(1))
        return _code_token(idx)

    return INLINE_CODE_PATTERN.sub(_sub, text), snippets


def unmask_inline_code(text: str, snippets: list[str]) -> str:
    for idx, snippet in enumerate(snippets):
        token = _code_token(idx)
        pattern = re.compile(rf"[<\[\(\{{]*\s*OCTX\s*CODE\s*{idx}\s*[>\]\)\}}]*", re.IGNORECASE)
        text = pattern.sub(f"`{snippet}`", text)
    return text


def mask_html(text: str) -> tuple[str, list[str]]:
    tags: list[str] = []

    def _sub(match: re.Match[str]) -> str:
        idx = len(tags)
        tags.append(match.group(0))
        return _html_token(idx)

    return HTML_TAG_PATTERN.sub(_sub, text), tags


def unmask_html(text: str, tags: list[str]) -> str:
    for idx, tag in enumerate(tags):
        token = _html_token(idx)
        pattern = re.compile(rf"[<\[\(\{{]*\s*OCTX\s*HTML\s*{idx}\s*[>\]\)\}}]*", re.IGNORECASE)
        text = pattern.sub(tag, text)
    return text


def translate_chunk(lines: list[str]) -> list[str]:
    """Translate a block of prose (no code fences) preserving inline code/URLs."""
    if not lines:
        return []
    combined = "\n".join(lines)
    masked, links = mask_links(combined)
    masked, code = mask_inline_code(masked)
    masked, html_tags = mask_html(masked)
    translated = argostranslate.translate.translate(masked, "en", "pt")
    restored = unmask_html(unmask_inline_code(unmask_links(translated, links), code), html_tags)
    restored = re.sub(r"\]\s+\(", "](", restored)
    restored = re.sub(r"^(#(?:\s+#)+)", lambda m: m.group(1).replace(" ", ""), restored, flags=re.MULTILINE)
    return restored.split("\n")


def translate_markdown(text: str) -> str:
    """Translate Markdown content, skipping code fences and frontmatter."""
    out: list[str] = []
    buffer: list[str] = []
    in_code = False
    in_frontmatter = False
    in_html_block = False
    lines = text.splitlines()

    def flush_buffer() -> None:
        nonlocal buffer
        if buffer:
            out.extend(translate_chunk(buffer))
            buffer = []

    for idx, line in enumerate(lines):
        stripped = line.strip()

        if idx == 0 and stripped == "---":
            flush_buffer()
            in_frontmatter = True
            out.append(line)
            continue
        if in_frontmatter:
            out.append(line)
            if stripped == "---":
                in_frontmatter = False
            continue

        if in_html_block:
            out.append(line)
            if ">" in stripped:
                in_html_block = False
            continue

        if stripped.startswith("<") and not stripped.startswith("<http"):
            if ">" not in stripped or not stripped.endswith(">"):
                flush_buffer()
                in_html_block = True
                out.append(line)
                if ">" in stripped:
                    in_html_block = False
                continue

        if stripped.startswith("```"):
            flush_buffer()
            in_code = not in_code
            out.append(line)
            continue

        if in_code:
            out.append(line)
            continue

        if not stripped:
            flush_buffer()
            out.append(line)
            continue

        buffer.append(line)

    flush_buffer()
    trailing_newline = "\n" if text.endswith("\n") else ""
    return "\n".join(out) + trailing_newline


def source_files() -> list[Path]:
    return [
        path
        for path in DOCS_ROOT.rglob("*")
        if path.suffix in VALID_EXTENSIONS
        and "pt-br" not in path.parts
        and not path.name.startswith(".")
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--paths",
        nargs="*",
        type=str,
        help="Limit to specific relative paths (file or directory, relative to docs/)",
    )
    parser.add_argument("--offset", type=int, default=0, help="Skip N files after filtering")
    parser.add_argument("--limit", type=int, help="Process at most N files after offset")
    args = parser.parse_args()

    ensure_translation_pack()

    files = sorted(source_files())
    if args.paths:
        prefixes = [Path(p).as_posix().rstrip("/") for p in args.paths]
        filtered = []
        for src in files:
            rel_posix = src.relative_to(DOCS_ROOT).as_posix()
            if any(rel_posix == prefix or rel_posix.startswith(prefix + "/") for prefix in prefixes):
                filtered.append(src)
        files = filtered
    if args.offset:
        files = files[args.offset :]
    if args.limit:
        files = files[: args.limit]

    for index, src in enumerate(files, start=1):
        rel = src.relative_to(DOCS_ROOT)
        dest = TARGET_ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text(encoding="utf-8")
        dest.write_text(translate_markdown(text), encoding="utf-8")
        print(f"[{index}/{len(files)}] {rel.as_posix()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
