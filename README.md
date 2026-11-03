# United States (Delaware): law history in git

The law of Delaware as a git history: one file per provision, with `git blame` and `git log` working line by line. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution-*/` | Delaware Constitution of 1897 as amended, one folder per article and the preamble | 1 | 207 provisions, text through July 1, 2025 |
| `title-11-chapter-*/` | Delaware Code, Title 11: Crimes and Criminal Procedure, one folder per chapter | 1 | 47 chapters, 1356 sections, text as of 2026-10-01 |
| `title-25-chapter-*/` | Delaware Code, Title 25: Property, one folder per chapter | 1 | 44 chapters, 689 sections, text as of 2026-10-01 |
| `title-08-chapter-*/` | Delaware Code, Title 8: Corporations, one folder per chapter | 1 | 3 chapters, 241 sections, text as of 2026-10-01 |
| `title-01-chapter-*/` | Delaware Code, Title 1: General Provisions, one folder per chapter | 1 | 8 chapters, 54 sections, text as of 2026-10-01 |
| `title-02-chapter-*/` | Delaware Code, Title 2: Transportation, one folder per chapter | 1 | 13 chapters, 213 sections, text as of 2026-10-01 |
| `title-03-chapter-*/` | Delaware Code, Title 3: Agriculture, one folder per chapter | 1 | 51 chapters, 743 sections, text as of 2026-10-01 |
| `title-04-chapter-*/` | Delaware Code, Title 4: Alcoholic Liquors and Marijuana, one folder per chapter | 1 | 9 chapters, 244 sections, text as of 2026-10-01 |
| `title-05-chapter-*/` | Delaware Code, Title 5: Banking, one folder per chapter | 1 | 30 chapters, 740 sections, text as of 2026-10-01 |
| `title-06-chapter-*/` | Delaware Code, Title 6: Commerce and Trade, one folder per chapter | 1 | 89 chapters, 1818 sections, text as of 2026-10-01 |
| `title-07-chapter-*/` | Delaware Code, Title 7: Conservation, one folder per chapter | 1 | 68 chapters, 1118 sections, text as of 2026-10-01 |
| `title-09-chapter-*/` | Delaware Code, Title 9: Counties, one folder per chapter | 1 | 65 chapters, 1349 sections, text as of 2026-10-01 |
| `title-10-chapter-*/` | Delaware Code, Title 10: Courts and Judicial Procedure, one folder per chapter | 1 | 65 chapters, 1204 sections, text as of 2026-10-01 |
| `title-12-chapter-*/` | Delaware Code, Title 12: Decedents' Estates and Fiduciary Relations, one folder per chapter | 1 | 34 chapters, 742 sections, text as of 2026-10-01 |
| `title-13-chapter-*/` | Delaware Code, Title 13: Domestic Relations, one folder per chapter | 1 | 21 chapters, 679 sections, text as of 2026-10-01 |
| `title-14-chapter-*/` | Delaware Code, Title 14: Education, one folder per chapter | 1 | 86 chapters, 1149 sections, text as of 2026-10-01 |
| `title-15-chapter-*/` | Delaware Code, Title 15: Elections, one folder per chapter | 1 | 39 chapters, 653 sections, text as of 2026-10-01 |
| `title-16-chapter-*/` | Delaware Code, Title 16: Health and Safety, one folder per chapter | 1 | 144 chapters, 1834 sections, text as of 2026-10-01 |
| `title-17-chapter-*/` | Delaware Code, Title 17: Highways, one folder per chapter | 1 | 19 chapters, 279 sections, text as of 2026-10-01 |
| `title-18-chapter-*/` | Delaware Code, Title 18: Insurance Code, one folder per chapter | 1 | 84 chapters, 1734 sections, text as of 2026-10-01 |
| `title-19-chapter-*/` | Delaware Code, Title 19: Labor, one folder per chapter | 1 | 25 chapters, 461 sections, text as of 2026-10-01 |
| `title-20-chapter-*/` | Delaware Code, Title 20: Military and Civil Defense, one folder per chapter | 1 | 12 chapters, 147 sections, text as of 2026-10-01 |
| `title-21-chapter-*/` | Delaware Code, Title 21: Motor Vehicles, one folder per chapter | 1 | 44 chapters, 862 sections, text as of 2026-10-01 |
| `title-22-chapter-*/` | Delaware Code, Title 22: Municipalities, one folder per chapter | 1 | 16 chapters, 187 sections, text as of 2026-10-01 |
| `title-23-chapter-*/` | Delaware Code, Title 23: Navigation and Waters, one folder per chapter | 1 | 10 chapters, 115 sections, text as of 2026-10-01 |
| `title-24-chapter-*/` | Delaware Code, Title 24: Professions and Occupations, one folder per chapter | 1 | 58 chapters, 1396 sections, text as of 2026-10-01 |
| `title-26-chapter-*/` | Delaware Code, Title 26: Public Utilities, one folder per chapter | 1 | 11 chapters, 220 sections, text as of 2026-10-01 |
| `title-27-chapter-*/` | Delaware Code, Title 27: Religion, one folder per chapter | 1 | 4 chapters, 24 sections, text as of 2026-10-01 |
| `title-28-chapter-*/` | Delaware Code, Title 28: Sports and Amusements, one folder per chapter | 1 | 11 chapters, 213 sections, text as of 2026-10-01 |
| `title-29-chapter-*/` | Delaware Code, Title 29: State Government, one folder per chapter | 1 | 116 chapters, 1925 sections, text as of 2026-10-01 |
| `title-30-chapter-*/` | Delaware Code, Title 30: State Taxes, one folder per chapter | 1 | 41 chapters, 627 sections, text as of 2026-10-01 |
| `title-31-chapter-*/` | Delaware Code, Title 31: Welfare, one folder per chapter | 1 | 34 chapters, 496 sections, text as of 2026-10-01 |

**Source.** The [Delaware Code Online](https://delcode.delaware.gov/), published by the Delaware General Assembly: the Constitution of 1897 as amended, and every title (1 to 31) of the Delaware Code. English. Only the statute text and the Code's own section source lines (the "Del. Laws" citations) are taken.

## Dates

The Delaware Code Online publishes only the current text. Each act is therefore one version, "oldest version available". The Code titles are dated 2026-10-01, the currency the site states ("acts enacted as of October 01, 2026, up to and including 85 Del. Laws, c. 550"); the Constitution is dated 2025-07-01, the date its index gives ("through July 1, 2025"). The session laws that made earlier changes are named in each section's last line but are not yet history here: later builds will add later versions on top.

## How it is checked

Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`) and must match `corpus.json`; the results are in `REPRODUCE.md`.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist (`<law key>@delcode.delaware.gov.invalid`). No dated history is available, so every commit is credited to the publisher as "oldest version available". The committer is always Lexifina.

## Limits

The Constitution and the whole Delaware Code (all 31 titles; reserved and repealed chapters with no text are left out). The Laws of Delaware, municipal charters and the Administrative Code are not included. There is no history before the dates above.
