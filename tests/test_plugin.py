#!/usr/bin/env python3
"""Static release checks for the create-ip-op-poster Plugin."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/Users/bytedance/Documents/work/evaluation/skill-build/create-ip-op-poster")


def check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)
        print(f"FAIL {message}")


def main() -> int:
    errors: list[str] = []
    manifest_path = ROOT / ".codex-plugin" / "plugin.json"
    check(manifest_path.is_file(), "missing .codex-plugin/plugin.json", errors)
    if not manifest_path.is_file():
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    check(manifest.get("name") == ROOT.name, "manifest name must equal Plugin folder name", errors)
    check(bool(re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", manifest.get("version", ""))), "version must be semver", errors)
    check(manifest.get("skills") == "./skills/", "skills path must be ./skills/", errors)
    check("apps" not in manifest, "skills-only Plugin must not declare apps", errors)
    check("mcpServers" not in manifest, "v0.1.0 must not declare MCP servers", errors)
    check("hooks" not in manifest, "manifest must not declare hooks", errors)

    interface = manifest.get("interface", {})
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        check(bool(interface.get(field)), f"missing interface.{field}", errors)
    prompts = interface.get("defaultPrompt", [])
    check(isinstance(prompts, list), "interface.defaultPrompt must be an array", errors)
    if isinstance(prompts, list):
        check(1 <= len(prompts) <= 3, "interface.defaultPrompt must contain 1-3 prompts", errors)
        for prompt in prompts:
            check(isinstance(prompt, str) and len(prompt) <= 128, "starter prompt exceeds 128 characters", errors)
    for field in ("composerIcon", "logo"):
        value = interface.get(field, "")
        check(value.startswith("./"), f"interface.{field} must use a relative ./ path", errors)
        check((ROOT / value).is_file(), f"interface.{field} file is missing", errors)

    parity = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "verify_parity.py"),
            "--source",
            str(SOURCE),
            "--plugin",
            str(ROOT),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    print(parity.stdout, end="")
    if parity.stderr:
        print(parity.stderr, file=sys.stderr, end="")
    check(parity.returncode == 0, "feature parity verification failed", errors)

    if errors:
        print(f"FAIL plugin ({len(errors)} errors)")
        return 1
    print("PASS plugin")
    return 0


if __name__ == "__main__":
    sys.exit(main())
