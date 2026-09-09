# Release verification — 0.4.0

Date: 2026-09-09
Source commit: `8e8e6e21be4a03b585303c065fa6c337d0d4408f` (`8e8e6e21be4a`)
Build method: clean-tree `git archive`

## Archives

| Archive | Bytes | SHA-256 | Members | Inspection |
|---|---:|---|---:|---|
| `create-ip-op-poster-plugin-0.4.0.zip` | 98,729 | `6ec76c565931c6c10e503d8c7cdf0af2fb02d924110e35bfca3ca90d28125f9e` | 40 | PASS |
| `create-ip-op-poster-skill-0.4.0.zip` | 77,948 | `cd0d25bed11005afd8fdd56b3fa1e2f6e077f6a2d85c8f37e964d446de0886b0` | 29 | PASS |

## Package boundary

- Both archives were generated from the commit above; no working-tree file was copied.
- Archive members passed the parity forbidden-pattern and sensitive-path inspection.
- The Skill archive contains no tests, design documents, private visual-case rasters, or nested release artifacts.
- Run Plugin, Skill, parity, and clean-extraction smoke tests before publication; record only direct results.
