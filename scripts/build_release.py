#!/usr/bin/env python3
"""Build reproducible Plugin and Skill archives from a clean Git commit."""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from datetime import date
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "0.3.0"


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"FAIL {message}")


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        fail(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def archive_members(path: Path, prefix: str) -> list[str]:
    members: list[str] = []
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts:
                fail(f"unsafe archive member in {path.name}: {info.filename}")
            if not member.parts or member.parts[0] != prefix:
                fail(f"unexpected archive prefix in {path.name}: {info.filename}")
            relative = PurePosixPath(*member.parts[1:]).as_posix()
            if relative:
                members.append(relative)
    return members


def forbidden_member(relative: str, patterns: list[str], skill_only: bool) -> str | None:
    path = PurePosixPath(relative)
    parts = set(path.parts)
    name = path.name
    if parts & {".git", "__pycache__", "release-work"}:
        return "forbidden directory"
    if name in {".DS_Store", ".env", ".npmrc"}:
        return "sensitive file"
    if name.endswith((".pyc", ".pem", ".key", ".p12")):
        return "sensitive or generated file"
    if relative.startswith("dist/"):
        return "nested release artifact"
    if skill_only and (relative.startswith("tests/") or relative.startswith("docs/")):
        return "private Skill test or design file"
    if skill_only and relative.startswith("assets/visual-cases/") and name.lower().endswith((".png", ".jpg", ".jpeg")):
        return "non-public visual-case raster"
    for pattern in patterns:
        if fnmatch.fnmatch(relative, pattern):
            return f"contract pattern {pattern}"
    return None


def inspect_archive(path: Path, prefix: str, patterns: list[str], skill_only: bool) -> int:
    members = archive_members(path, prefix)
    for relative in members:
        reason = forbidden_member(relative, patterns, skill_only)
        if reason:
            fail(f"{path.name} contains {relative}: {reason}")

    required = {"SKILL.md"} if skill_only else {".codex-plugin/plugin.json", "skills/create-ip-op-poster/SKILL.md"}
    missing = sorted(required - set(members))
    if missing:
        fail(f"{path.name} missing required members: {missing}")
    return len(members)


def build_archive(output: Path, treeish: str, prefix: str) -> None:
    result = subprocess.run(
        [
            "git",
            "archive",
            "--format=zip",
            f"--prefix={prefix}/",
            f"--output={output}",
            treeish,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        fail(result.stderr.strip() or f"git archive failed for {treeish}")


def main() -> int:
    manifest_path = ROOT / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    version = manifest.get("version")
    if version != EXPECTED_VERSION:
        fail(f"manifest version must be {EXPECTED_VERSION}, found {version!r}")

    dirty = git("status", "--porcelain", "--untracked-files=all")
    if dirty:
        fail("Plugin worktree must be clean before packaging")

    contract = json.loads((ROOT / "parity" / "capabilities.json").read_text(encoding="utf-8"))
    forbidden_patterns = list(contract.get("forbidden_patterns", []))
    commit = git("rev-parse", "HEAD")
    short_commit = git("rev-parse", "--short=12", "HEAD")

    plugin_name = f"create-ip-op-poster-plugin-{version}.zip"
    skill_name = f"create-ip-op-poster-skill-{version}.zip"
    plugin_prefix = f"create-ip-op-poster-plugin-{version}"
    skill_prefix = "create-ip-op-poster"

    dist = ROOT / "dist"
    dist.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="poster-release-") as temp_value:
        temp = Path(temp_value)
        plugin_temp = temp / plugin_name
        skill_temp = temp / skill_name
        build_archive(plugin_temp, "HEAD", plugin_prefix)
        build_archive(skill_temp, "HEAD:skills/create-ip-op-poster", skill_prefix)

        plugin_count = inspect_archive(plugin_temp, plugin_prefix, forbidden_patterns, skill_only=False)
        skill_count = inspect_archive(skill_temp, skill_prefix, forbidden_patterns, skill_only=True)

        results = [
            (plugin_name, plugin_temp.stat().st_size, sha256(plugin_temp), plugin_count),
            (skill_name, skill_temp.stat().st_size, sha256(skill_temp), skill_count),
        ]

        os.replace(plugin_temp, dist / plugin_name)
        os.replace(skill_temp, dist / skill_name)

    report_lines = [
        f"# Release verification — {version}",
        "",
        f"Date: {date.today().isoformat()}",
        f"Source commit: `{commit}` (`{short_commit}`)",
        "Build method: clean-tree `git archive`",
        "",
        "## Archives",
        "",
        "| Archive | Bytes | SHA-256 | Members | Inspection |",
        "|---|---:|---|---:|---|",
    ]
    for name, size, digest, count in results:
        report_lines.append(f"| `{name}` | {size:,} | `{digest}` | {count} | PASS |")
    report_lines.extend(
        [
            "",
            "## Package boundary",
            "",
            "- Both archives were generated from the commit above; no working-tree file was copied.",
            "- Archive members passed the parity forbidden-pattern and sensitive-path inspection.",
            "- The Skill archive contains no tests, design documents, private visual-case rasters, or nested release artifacts.",
            "- Run Plugin, Skill, parity, and clean-extraction smoke tests before publication; record only direct results.",
            "",
        ]
    )
    (ROOT / "tests" / "release-report.md").write_text("\n".join(report_lines), encoding="utf-8")

    for name, size, digest, _ in results:
        print(f"PASS {name} {size} bytes sha256={digest}")
    print("PASS release archives")
    return 0


if __name__ == "__main__":
    sys.exit(main())
