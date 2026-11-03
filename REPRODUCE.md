# How this repository was made (United States (Delaware))

This file is written by the build on 2026-11-03, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| The Delaware Code Online | <https://delcode.delaware.gov/> | 2026-11-03 | Statute text carries no copyright (Georgia v. Public.Resource.Org, 2020). The site publishes the Code as the General Assembly's official text with a no-warranty disclaimer and no reuse restriction. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `title-11-chapter-084a` | Delaware Code, Title 11, CHAPTER 84A. Body-Worn Cameras for Law-Enforcement Officers | 1 | 2026-10-01 to 2026-10-01 |
| `title-11-chapter-084b` | Delaware Code, Title 11, CHAPTER 84B. Prohibited Police Practices | 1 | 2026-10-01 to 2026-10-01 |
| `title-11-chapter-087a` | Delaware Code, Title 11, CHAPTER 87A. Reporting and Review of Deaths of Individuals in Custody of Law Enforcement Agencies | 1 | 2026-10-01 to 2026-10-01 |
| `title-11-chapter-089a` | Delaware Code, Title 11, CHAPTER 89A. The Delaware Sentencing Guidelines and Accountability Commission | 1 | 2026-10-01 to 2026-10-01 |
| `title-11-chapter-089b` | Delaware Code, Title 11, CHAPTER 89B. Call Location Information | 1 | 2026-10-01 to 2026-10-01 |

The build made 5 commits:

| Commits | Kind |
| ---: | --- |
| 5 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-11-03.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 0 laws in the record.
- 5 tags.

## Dates

Each commit is dated at noon (America/New_York) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: No dated history is published: each act is the oldest version available, dated by the source's own currency statement. https://delcode.delaware.gov/

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `76dae39cb66fc405fa07bad82307cec716a62fcbfc799f3a706d45f7464b0c21` (38116 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `3024ff164c261807dfc4d5b7b1b4a2cde4357da1`, `check.py` `5d719354ea4c62d240c93d2cae446307d81d9e81`, `on.py` `aff48cf1b68d50c7ba8f399ca32261871c301824`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Additional Title 11 chapters are current consolidated text, first_law null, dated by the official Code currency statement of October 1, 2026. The printed section source citations are retained; no historical wording or amendment attribution is inferred.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- A model wrote extraction and verification code; all law text and punctuation come from the official HTML.
