# How this repository was made (United States (Delaware))

This file is written by the build on 2026-11-13, the day the source data was retrieved.

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
| 5 | baseline texts where the record starts |
| 0 | named laws, court decisions and treaties |
| 0 | changes no amendment note explains, credited to the publisher |
| 0 | corrections to the existing record |
| 0 | printing or layout changes |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-11-13.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 0 laws in the record.
- 5 tags.

## Dates

Each commit is dated at noon (America/New_York) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: No dated history is published: each act is the oldest version available, dated by the source's own currency statement. https://delcode.delaware.gov/

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `6edbb35714fdea2af2440440bc8d2ec30815b15e99d1b5751bf21fea9fdc00ec` (38246 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `63170edd89e92292ac248dae17d79e486e4e9f19`, `check.py` `e340718c28cd5b0edbe37bdeab1aac31427ada66`, `on.py` `4a8aa1c9a5e6bd8cc831b90a6e68c5a6f448a13c`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Additional Title 11 chapters are current consolidated text, first_law null, dated by the official Code currency statement of October 1, 2026. The printed section source citations are retained; no historical wording or amendment attribution is inferred.

## What AI did and did not do

The source readers and builders were developed under Lexifina's direction with coding assistants, including Claude Code and Codex.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- A model wrote extraction and verification code; all law text and punctuation come from the official HTML.
