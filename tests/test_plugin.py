#!/usr/bin/env python3
"""Static release checks for the create-ip-op-poster Plugin."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("POSTER_SKILL_SOURCE", ROOT / "skills" / "create-ip-op-poster"))
EXPECTED_VERSION = "0.3.0"
PUBLIC_OVERRIDES = [
    "references/workflow.md",
    "references/platform-usage.md",
    "references/visual-case-library.md",
    "examples/successful-prompt-benchmark.md",
]


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
    check(manifest.get("version") == EXPECTED_VERSION, f"manifest version must be {EXPECTED_VERSION}", errors)
    check(manifest.get("skills") == "./skills/", "skills path must be ./skills/", errors)
    check("apps" not in manifest, "skills-only Plugin must not declare apps", errors)
    check("mcpServers" not in manifest, "skills-only release must not declare MCP servers", errors)
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
        if prompts:
            prompt_text = "\n".join(prompts)
            check("人物" in prompts[0] and "人物没问题" in prompts[0], "first starter prompt must begin with the person-material gate", errors)
            check("选 1 生成" in prompt_text, "starter prompts must expose the second and final confirmation", errors)
            check("16:9 横版" in prompt_text, "starter prompts must expose the landscape default", errors)
            check("严格保真" in prompt_text, "starter prompts must explain automatic strict-fidelity routing", errors)
            for marker in ("模式 A", "模式 B", "确认生成", "prompt_pending", "direction_and_mode_pending"):
                check(marker not in prompt_text, f"starter prompts contain legacy user gate: {marker}", errors)
    for field in ("composerIcon", "logo"):
        value = interface.get(field, "")
        check(value.startswith("./"), f"interface.{field} must use a relative ./ path", errors)
        check((ROOT / value).is_file(), f"interface.{field} file is missing", errors)

    active_listing = "\n".join(
        (
            manifest_path.read_text(encoding="utf-8"),
            (ROOT / "README.md").read_text(encoding="utf-8"),
            (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"),
            (ROOT / "tests" / "openai-submission.md").read_text(encoding="utf-8"),
        )
    )
    for marker in (
        "第 1/4 步",
        "四次确认",
        "排布通过",
        "composition_pending",
        "direction_and_mode_pending",
        "prompt_pending",
        "选方向 1，用模式 B",
        "确认生成",
        "生成确认卡",
        "模式 A｜快速生图",
        "模式 B｜保真合成",
        "模式 A：快速生图",
        "模式 B：保真合成",
    ):
        check(marker not in active_listing, f"listing contains legacy marker: {marker}", errors)
    for marker in (
        "人物没问题",
        "选 1 生成",
        "视觉偏好",
        "16:9 横版",
        "默认整图生成",
        "严格保真",
        "不得整图重绘",
        "0.3.0",
    ):
        check(marker in active_listing, f"listing missing current marker: {marker}", errors)

    contract_path = ROOT / "parity" / "capabilities.json"
    check(contract_path.is_file(), "missing parity/capabilities.json", errors)
    if contract_path.is_file():
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        check(contract.get("public_overrides") == PUBLIC_OVERRIDES, "public override list changed", errors)
        expected_capabilities = {
            "two_confirmation_flow",
            "optional_visual_preference",
            "content_play_preflight",
            "whole_poster_default",
            "strict_fidelity_auto_route",
            "strict_fidelity_integration",
            "exact_post_edit",
            "landscape_default",
            "person_layout_routing",
            "prompt_information_budget",
            "actual_final_qa",
        }
        forbidden_capabilities = {
            "direction_mode_choice",
            "mode_a_fast_generation",
            "mode_b_protected_composite",
        }
        capability_ids = {item.get("id") for item in contract.get("capabilities", [])}
        check(expected_capabilities <= capability_ids, "missing novice whole-poster capability checks", errors)
        check(not (forbidden_capabilities & capability_ids), "legacy mode capabilities remain in parity contract", errors)

    benchmark = ROOT / "skills" / "create-ip-op-poster" / "examples" / "successful-prompt-benchmark.md"
    visual_library = ROOT / "skills" / "create-ip-op-poster" / "references" / "visual-case-library.md"
    packaged_readme = ROOT / "skills" / "create-ip-op-poster" / "README.md"
    check(packaged_readme.is_file(), "packaged Skill must include README.md", errors)
    check("完全虚构" in benchmark.read_text(encoding="utf-8"), "public benchmark must stay fictional", errors)
    visual_text = visual_library.read_text(encoding="utf-8")
    check("original anonymous layout diagrams" in visual_text, "public visual library must stay anonymous", errors)
    check("VC01" not in visual_text, "public visual library must not restore private case index", errors)
    release_builder = ROOT / "scripts" / "build_release.py"
    check(release_builder.is_file(), "missing reproducible release builder", errors)
    if release_builder.is_file():
        check('EXPECTED_VERSION = "0.3.0"' in release_builder.read_text(encoding="utf-8"), "release builder version must be 0.3.0", errors)

    public_text_files = [
        manifest_path,
        ROOT / "README.md",
        ROOT / "CHANGELOG.md",
        ROOT / "tests" / "openai-submission.md",
        contract_path,
    ]
    public_text_files.extend(
        path
        for path in (ROOT / "skills" / "create-ip-op-poster").rglob("*")
        if path.is_file() and path.suffix in {".md", ".json", ".yaml"}
    )
    for path in public_text_files:
        check("/Users/" not in path.read_text(encoding="utf-8"), f"local absolute path leaked: {path.relative_to(ROOT)}", errors)

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
