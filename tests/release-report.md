# Release verification — 0.2.0

Date: 2026-08-31
Source commit: `76e381d6ad3f8e38bb2389188e4571ba96f7e735` (`76e381d6ad3f`)
Build method: clean-tree `git archive`

## Archives

| Archive | Bytes | SHA-256 | Members | Inspection |
|---|---:|---|---:|---|
| `create-ip-op-poster-plugin-0.2.0.zip` | 84,382 | `5eb1f4892ed59a22aa65378c9e6ffe8615ec0ae028040eecfe0242da4d314347` | 34 | PASS |
| `create-ip-op-poster-skill-0.2.0.zip` | 66,308 | `32b28e0424e7690820eb981724d2a5c521244f203ac81e6c8eb2b765244da2fd` | 23 | PASS |

## Validation results

- Working Plugin contract and parity checks: `PASS plugin`; all 18 capability checks passed.
- Clean extracted Plugin contract and parity checks: `PASS plugin`; all 18 capability checks passed.
- Clean extracted Skill behavioral validator: `PASS workflow`, `PASS production`, `PASS visual`, `PASS integrity`, `PASS prompt`, `PASS docs`.
- Plugin Creator structural validation passed for the working Plugin and clean extracted Plugin.
- Skill Creator structural validation passed for the source Skill, Plugin Skill, and clean extracted Skill.
- Independent SHA-256 output matched both archive hashes above.

## Package boundary

- Both archives were generated from the commit above; no working-tree file was copied.
- Archive members passed the parity forbidden-pattern and sensitive-path inspection.
- The Skill archive contains no tests, design documents, private visual-case rasters, or nested release artifacts.
- Plugin, Skill, parity, structural, checksum, and clean-extraction smoke tests were completed before publication; only direct results are recorded above.
