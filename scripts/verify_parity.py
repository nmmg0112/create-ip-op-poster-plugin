#!/usr/bin/env python3
"""Verify that the public Plugin preserves the source poster Skill's capabilities."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def load_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing YAML frontmatter: {path}")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"unterminated YAML frontmatter: {path}")
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)
    print(f"FAIL {message}")


def verify_links(skill_root: Path, errors: list[str]) -> None:
    for markdown in sorted(skill_root.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            clean = target.split("#", 1)[0].strip()
            if not clean or clean.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (markdown.parent / clean).resolve()
            try:
                resolved.relative_to(skill_root.resolve())
            except ValueError:
                fail(f"link escapes Skill root: {markdown.relative_to(skill_root)} -> {target}", errors)
                continue
            if not resolved.exists():
                fail(f"broken link: {markdown.relative_to(skill_root)} -> {target}", errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--plugin", required=True, type=Path)
    args = parser.parse_args()

    source = args.source.resolve()
    plugin = args.plugin.resolve()
    skill = plugin / "skills" / "create-ip-op-poster"
    contract_path = plugin / "parity" / "capabilities.json"
    errors: list[str] = []

    if not contract_path.is_file():
        fail("missing parity/capabilities.json", errors)
        return 1
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    for relative in contract["required_files"]:
        source_path = source / relative
        plugin_path = skill / relative
        if not source_path.is_file():
            fail(f"source baseline missing required file: {relative}", errors)
        if not plugin_path.is_file():
            fail(f"Plugin missing required file: {relative}", errors)

    required_files = set(contract["required_files"])
    exact_mirror_files = set(contract["exact_mirror_files"])
    public_overrides = set(contract["public_overrides"])
    if exact_mirror_files & public_overrides:
        fail("exact_mirror_files and public_overrides must be disjoint", errors)
    if exact_mirror_files | public_overrides != required_files:
        fail("exact_mirror_files and public_overrides must partition required_files", errors)

    for relative in contract["exact_mirror_files"]:
        source_path = source / relative
        plugin_path = skill / relative
        if not source_path.is_file() or not plugin_path.is_file():
            fail(f"exact mirror missing: {relative}", errors)
            continue
        if source_path.read_bytes() != plugin_path.read_bytes():
            fail(f"exact mirror differs: {relative}", errors)

    if (source / "SKILL.md").is_file() and (skill / "SKILL.md").is_file():
        source_meta = load_frontmatter(source / "SKILL.md")
        plugin_meta = load_frontmatter(skill / "SKILL.md")
        for field in ("name", "description"):
            if source_meta.get(field) != plugin_meta.get(field):
                fail(f"SKILL.md {field} differs from source baseline", errors)

    files = [path.relative_to(plugin).as_posix() for path in plugin.rglob("*") if path.is_file()]
    for pattern in contract["forbidden_patterns"]:
        for relative in files:
            if fnmatch.fnmatch(relative, pattern):
                fail(f"forbidden public file: {relative}", errors)

    active_files = [skill / "SKILL.md", skill / "agents" / "openai.yaml"]
    for folder in (skill / "references", skill / "examples"):
        active_files.extend(sorted(folder.rglob("*.md")))
        active_files.extend(sorted(folder.rglob("*.txt")))
    for path in active_files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in contract["forbidden_legacy_markers"]:
            if marker in text:
                fail(f"forbidden legacy marker in {path.relative_to(skill)}: {marker}", errors)

    for capability in contract["capabilities"]:
        path = skill / capability["file"]
        if not path.is_file():
            fail(f"{capability['id']}: missing {capability['file']}", errors)
            continue
        text = path.read_text(encoding="utf-8").casefold()
        missing = [marker for marker in capability["markers"] if marker.casefold() not in text]
        if missing:
            fail(f"{capability['id']}: missing markers {missing}", errors)
        else:
            print(f"PASS {capability['id']}")

    if skill.is_dir():
        verify_links(skill, errors)

    if errors:
        print(f"FAIL parity ({len(errors)} errors)")
        return 1
    print("PASS parity")
    return 0


if __name__ == "__main__":
    sys.exit(main())
