# Release verification — 0.4.0

Date: 2026-09-09
Source commit: `f4fb8d664feb47010c6a4c509c5d19d4ad27d7eb` (`f4fb8d664feb`)
Build method: clean-tree `git archive`

## Archives

| Archive | Bytes | SHA-256 | Members | Inspection |
|---|---:|---|---:|---|
| `create-ip-op-poster-plugin-0.4.0.zip` | 98,729 | `cda834cd62699a4029d25ac9bdc0712a1c2f85860a511a58d6fe0c8993bae6c8` | 40 | PASS |
| `create-ip-op-poster-skill-0.4.0.zip` | 77,948 | `01db20bc4f9cb54fde88eab0220613307d68b5f769762f28c8e30fe9badeef22` | 29 | PASS |

## Package boundary

- Both archives were generated from the commit above; no working-tree file was copied.
- Archive members passed the parity forbidden-pattern and sensitive-path inspection.
- The Skill archive contains no tests, design documents, private visual-case rasters, or nested release artifacts.
- Run Plugin, Skill, parity, and clean-extraction smoke tests before publication; record only direct results.
