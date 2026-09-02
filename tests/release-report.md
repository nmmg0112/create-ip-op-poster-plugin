# Release verification — 0.3.0

Date: 2026-09-02
Source commit: `e8df476d1730698d30a92c3e07fa7d6f81cd8685` (`e8df476d1730`)
Build method: clean-tree `git archive`

## Archives

| Archive | Bytes | SHA-256 | Members | Inspection |
|---|---:|---|---:|---|
| `create-ip-op-poster-plugin-0.3.0.zip` | 83,721 | `d89c7f805d2880002c0911e6415c055ac0981caa7827a5addab352f79cd70eea` | 34 | PASS |
| `create-ip-op-poster-skill-0.3.0.zip` | 64,423 | `c3ea6a02bfd8ac66773208e0543ed37979bca25ad0cbb4ce038d5e8453c90cd1` | 23 | PASS |

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
