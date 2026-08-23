# Release verification — 0.1.0

Date: 2026-08-23

## Local source

- Release commit tested: `b60c9ecdf9505ff19e53bdfb54205b456ad59f30`
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

Remote repository, tag, release asset, and final commit comparison are recorded after publication.
