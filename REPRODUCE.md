# How this repository was made (United States (Delaware))

This file is written by the build on 2026-11-13, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Laws of Delaware, Volume 85 | <https://legis.delaware.gov/SessionLaws/Chapters?volume=166> | 2026-11-13 | Official legislative instruments of the Delaware General Assembly; website copyright notice retained in source evidence. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `session-law-085-chapter-044` | AN ACT TO AMEND TITLE 26 OF THE DELAWARE CODE RELATING TO PUBLIC UTILITIES. | 1 | 2025-06-30 to 2025-06-30 |
| `session-law-085-chapter-050` | AN ACT TO AMEND TITLE 14 OF THE DELAWARE CODE RELATING TO SCHOOL BOARD MEMBERS. | 1 | 2025-06-30 to 2025-06-30 |
| `session-law-085-chapter-084` | AN ACT TO AMEND TITLES 3, 7, AND 16 OF THE DELAWARE CODE RELATING TO THE ENVIRONMENT. WHEREAS, the Delaware General Assembly seeks to modernize penalties imposed on commercial polluters; and WHEREAS, the General Assembly sees the need to divert a higher percentage of fines collected to impacted communities; and WHEREAS, some commercial heavy industrial polluters are chronic violators who engage in a pattern of wilful neglect or reckless disregard of the permits or regulatory programs of the Delaware Department of Natural Resources and Environmental Control. NOW, THEREFORE: | 1 | 2025-07-16 to 2025-07-16 |
| `session-law-085-chapter-097` | AN ACT TO AMEND TITLE 24 OF THE DELAWARE CODE RELATING TO PHARMACY. | 1 | 2025-07-21 to 2025-07-21 |

The build made 4 commits:

| Commits | Kind |
| ---: | --- |
| 4 | baseline texts where the record starts |
| 0 | named laws, court decisions and treaties |
| 0 | changes no amendment note explains, credited to the publisher |
| 0 | corrections to the existing record |
| 0 | printing or layout changes |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-11-13.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 0 laws in the record.
- 4 tags.

## Dates

Each commit is dated at noon (America/New_York) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: No dated history is published: each act is the oldest version available, dated by the source's own currency statement. https://delcode.delaware.gov/

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `36f2145bc0dfd779dcf095bac560257a6e9c5c69ffed12bed609a2fd861bb28f` (80654 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `63170edd89e92292ac248dae17d79e486e4e9f19`, `check.py` `e340718c28cd5b0edbe37bdeab1aac31427ada66`, `on.py` `4a8aa1c9a5e6bd8cc831b90a6e68c5a6f448a13c`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Session-law instruments are as enacted, with one HTML document per chapter. Source approval dates are record dates with in_force_unknown true: no uniform commencement or consolidated Code reconstruction is asserted. All source insertion/deletion formatting and textual tables are retained.

## What AI did and did not do

The source readers and builders were developed under Lexifina's direction with coding assistants, including Claude Code and Codex.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- A model wrote extraction and verification code. Legal wording and amendment formatting were extracted from official HTML without model edits.
