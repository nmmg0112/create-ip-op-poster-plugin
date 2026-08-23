# Release verification — 0.1.0

Date: 2026-08-23

## Local source

- Release commit tested: `b60c9ecdf9505ff19e53bdfb54205b456ad59f30`
- Local release tag: `v0.1.0`
- Release archive: `create-ip-op-poster-plugin-0.1.0.zip`
- Archive size: `63,836 bytes`
- SHA-256: `f72d791829b95c910033558f3ec1e458a1030986085bf4dcec35b14d5417fcea`

## Validation results

- Plugin feature-parity test: `PASS plugin`
- Required capabilities: `15/15 PASS`
- Plugin Creator validator: `Plugin validation passed`
- Skill Creator validator: `Skill is valid!`
- Clean archive extraction: `PASS`
- Feature parity, Plugin validation, and Skill validation rerun from extracted archive: `PASS`

## Distribution checks

- The archive contains `.codex-plugin/plugin.json` and `skills/create-ip-op-poster/SKILL.md` under the root folder `create-ip-op-poster/`.
- All required Markdown references and examples resolve from the extracted archive.
- No tests, internal design documents, `.DS_Store`, contact sheets, or third-party visual-case raster files are present.
- Six original anonymous SVG layout guides replace non-public poster originals without removing the visual-retrieval workflow.
- Version `0.1.0` declares no MCP server, App, Hook, external login, or independent data collection.

## Remote verification

- Feishu tutorial updated and read back at revision `18`.
- Plugin ZIP attached to the tutorial as `create-ip-op-poster-plugin-0.1.0.zip`; attachment size is `63,836 bytes`.
- Public GitHub Plugin repository creation remains pending because the available GitHub connector cannot create repositories and the browser requires action-time confirmation before publishing a new public repository.
- The existing public Skill repository was deliberately not overwritten: its public anonymous case library differs from local internal reference materials, and preserving that boundary is required for safe publication.
- After the public Plugin repository exists, publish release commit `b60c9ecdf9505ff19e53bdfb54205b456ad59f30`, tag `v0.1.0`, attach the verified ZIP above, and compare the remote tree against the clean extracted archive.
