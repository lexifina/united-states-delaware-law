"""Writes repo/README.md, LICENSE, jurisdiction.json from corpus.json."""
import json
import os

from state_lib import write_docs

HERE = os.path.dirname(os.path.abspath(__file__))
c = json.load(open(os.path.join(HERE, 'corpus.json'), encoding='utf-8'))
groups = {}
for a in c['acts']:
    g = a['slug'].rsplit('-chapter-', 1)[0] if '-chapter-' in a['slug'] else 'constitution'
    groups.setdefault(g, []).append(a)
rows = []
for g, acts in groups.items():
    n = sum(len(a['versions'][0]['units']) for a in acts)
    if g == 'constitution':
        rows.append(('constitution-*/', 'Delaware Constitution of 1897 as amended, one folder per article and the preamble', 1,
                     f'{n} provisions, text through July 1, 2025'))
    else:
        t = int(g.split('-')[1])
        name = {11: 'Crimes and Criminal Procedure', 25: 'Property', 8: 'Corporations'}[t]
        rows.append((f'{g}-chapter-*/', f'Delaware Code, Title {t}: {name}, one folder per chapter', 1,
                     f'{len(acts)} chapters, {n} sections, text as of 2026-10-01'))
write_docs(HERE, {
    'name': 'United States (Delaware)', 'state': 'Delaware', 'code': 'US-DE', 'slug': 'delaware',
    'domain': 'delcode.delaware.gov', 'acts_table': rows,
    'source': 'The [Delaware Code Online](https://delcode.delaware.gov/), published by the Delaware General Assembly: the Constitution of 1897 as amended, and Titles 8 (Corporations), 11 (Crimes and Criminal Procedure) and 25 (Property) of the Delaware Code. English. Only the statute text and the Code\'s own section source lines (the "Del. Laws" citations) are taken.',
    'dates': 'The Delaware Code Online publishes only the current text. Each act is therefore one version, "oldest version available". The Code titles are dated 2026-10-01, the currency the site states ("acts enacted as of October 01, 2026, up to and including 85 Del. Laws, c. 550"); the Constitution is dated 2025-07-01, the date its index gives ("through July 1, 2025"). The session laws that made earlier changes are named in each section\'s last line but are not yet history here: later builds will add later versions on top.',
    'limits': 'A first build: the Constitution and three titles of the Delaware Code. The other titles, the Laws of Delaware and the Administrative Code are not included. There is no history before the dates above.',
    'license': """Source: The Delaware Code Online, Delaware General Assembly, https://delcode.delaware.gov/ (retrieved 2026-10-30).

Statute text is not copyrightable: under the government edicts doctrine, as the Supreme Court applied it in Georgia v.
Public.Resource.Org, Inc., 590 U.S. 255 (2020), no one holds copyright in the laws that legislators make in their official
capacity. The site carries only a disclaimer of warranty ("neither the State of Delaware nor any of its employees makes any
warranty ...") and states no restriction on reuse; it has no robots.txt. No annotations are used.""",
})
