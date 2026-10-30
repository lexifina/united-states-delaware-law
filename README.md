# United States (Delaware): law history in git

The law of Delaware as a git history: one file per provision, with `git blame` and `git log` working line by line. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now (a first build, not complete)**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution-*/` | Delaware Constitution of 1897 as amended, one folder per article and the preamble | 1 | 207 provisions, text through July 1, 2025 |
| `title-11-chapter-*/` | Delaware Code, Title 11: Crimes and Criminal Procedure, one folder per chapter | 1 | 47 chapters, 1356 sections, text as of 2026-10-01 |
| `title-25-chapter-*/` | Delaware Code, Title 25: Property, one folder per chapter | 1 | 44 chapters, 689 sections, text as of 2026-10-01 |
| `title-08-chapter-*/` | Delaware Code, Title 8: Corporations, one folder per chapter | 1 | 3 chapters, 241 sections, text as of 2026-10-01 |

**Source.** The [Delaware Code Online](https://delcode.delaware.gov/), published by the Delaware General Assembly: the Constitution of 1897 as amended, and Titles 8 (Corporations), 11 (Crimes and Criminal Procedure) and 25 (Property) of the Delaware Code. English. Only the statute text and the Code's own section source lines (the "Del. Laws" citations) are taken.

## Dates

The Delaware Code Online publishes only the current text. Each act is therefore one version, "oldest version available". The Code titles are dated 2026-10-01, the currency the site states ("acts enacted as of October 01, 2026, up to and including 85 Del. Laws, c. 550"); the Constitution is dated 2025-07-01, the date its index gives ("through July 1, 2025"). The session laws that made earlier changes are named in each section's last line but are not yet history here: later builds will add later versions on top.

## How it is checked

Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`) and must match `corpus.json`; the results are in `REPRODUCE.md`.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist (`<law key>@delcode.delaware.gov.invalid`). In this first build no dated history is available, so every commit is credited to the publisher as "oldest version available". The committer is always Lexifina.

## Limits

A first build: the Constitution and three titles of the Delaware Code. The other titles, the Laws of Delaware and the Administrative Code are not included. There is no history before the dates above.
