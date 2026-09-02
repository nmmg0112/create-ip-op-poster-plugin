# Release verification — 0.3.0

Date: 2026-09-02
Source commit: `f87122b32cbeb54690892bacaab72475d4149838` (`f87122b32cbe`)
Build method: clean-tree `git archive`

## Archives

| Archive | Bytes | SHA-256 | Members | Inspection |
|---|---:|---|---:|---|
| `create-ip-op-poster-plugin-0.3.0.zip` | 83,721 | `32c992a75106d607aa0358a46d2cbef0b3433548cf3f770efdbca92d5e45dcd4` | 34 | PASS |
| `create-ip-op-poster-skill-0.3.0.zip` | 64,423 | `3d81522e1169ea9ed6e6180bebdb631fa0e1d469ef1e5c9465e601ed57189041` | 23 | PASS |

## Validation results

- Canonical Skill behavioral validator: `PASS workflow`, `PASS production`, `PASS visual`, `PASS integrity`, `PASS prompt`, `PASS docs`, `PASS all`.
- Working Plugin contract and parity checks: `PASS plugin`; all 23 capability checks passed against the canonical Skill.
- Clean extracted Plugin parity checks: `PASS parity`; all 23 capability checks passed.
- Clean extracted Skill smoke test: required runtime files and current two-wait, strict-integration, and no-sensitive-file markers passed.
- Independent SHA-256 output matched both archive hashes above.
- Official PyYAML-based quick validators were not run because the available host Python runtimes do not provide `yaml`; this is recorded as an environment limitation, not a pass.

## Package boundary

- Both archives were generated from the commit above; no working-tree file was copied.
- Archive members passed the parity forbidden-pattern and sensitive-path inspection.
- The Skill archive contains no tests, design documents, private visual-case rasters, or nested release artifacts.
- Plugin, Skill, parity, checksum, and clean-extraction smoke tests were completed before publication; only direct results are recorded above.
