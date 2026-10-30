"""Parse the cached Delaware Code Online pages into corpus.json. Reads only .cache; no network."""
import json
import os
import re
import sys

from bs4 import BeautifulSoup

from state_lib import Act, Fetcher, key, norm, sha, text_of, write_corpus

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://delcode.delaware.gov/'
F = Fetcher(HERE, 'x')
# The Code Online states: "...acts enacted as of October 01, 2026, up to and including 85 Del. Laws, c. 550."
CODE_DATE = '2026-10-01'
CONST_DATE = '2025-07-01'   # "with Amendments made subsequently thereto, through July 1, 2025"
RETRIEVED = '2026-10-30'


def soup(u):
    b = F.cached(u)
    return BeautifulSoup(b.decode('utf-8', 'replace'), 'lxml'), b


def roman(r):
    v = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    t = 0
    for i, ch in enumerate(r):
        t += -v[ch] if i + 1 < len(r) and v[ch] < v[r[i + 1]] else v[ch]
    return t


def constitution():
    man = json.load(open(os.path.join(HERE, '.cache', 'manifest.json')))
    acts = []
    for u in man['constitution']:
        s, b = soup(u)
        c = s.find(id='content')
        h2 = c.find('h2')
        title = norm(h2.find(string=True, recursive=False) or h2.get_text())
        n = re.search(r'constitution-(\d+)', u).group(1)
        if n == '01':
            slug, short = 'constitution-preamble', 'Del. Const. preamble'
        else:
            m = re.match(r'ARTICLE\s+([IVXLC]+)\b', title)
            num = roman(m.group(1)) if m else int(n)
            slug, short = f'constitution-art-{num:02d}', f'Del. Const. art. {m.group(1) if m else n}'
        a = Act(slug, short, 'Delaware Constitution of 1897, ' + title, u, CONST_DATE, sha256=sha(b))
        body = [p for p in c.find_all('p') if p.find_parent(id='content')]
        cur = None
        pre = []
        for p in body:
            cls = p.get('class') or []
            t = norm(p.get_text(' '))
            if 'section-label' in cls:
                if cur:
                    a.add(*cur_unit(cur))
                m = re.match(r'§+\s*([0-9A-Za-z]+(?:[-,\s]+[0-9A-Za-z]+)*?)\.\s*(.*)$', t)
                lab = m.group(1) if m else t
                cur = {'label': lab, 'lines': ['# ' + t]}
            elif cur is not None:
                if t:
                    cur['lines'].append(t)
            elif t and not p.find_parent(class_='row'):
                pre.append(t)
        if cur:
            a.add(*cur_unit(cur))
        if pre:
            a.add('preamble', 'Preamble', 'preamble', text_of(pre))
        acts.append(a)
    return acts


def cur_unit(cur):
    return (key('sec', cur['label']), '§ ' + cur['label'], 'section', text_of(cur['lines']))


def code_title(t, chapters, man_title_name):
    acts = []
    for ch in chapters:
        cid = ch['id']
        s0, _ = soup(ch['url'])
        h2 = s0.find('h2')
        ctitle = norm(h2.get_text(' ')) if h2 else ''
        n = int(cid[1:])
        a = Act(f'title-{t:02d}-chapter-{n:03d}', f'{t} Del. C. ch. {n}',
                f'Delaware Code, Title {t}, Chapter {n}' + (f': {ctitle}' if ctitle else ''), ch['url'], CODE_DATE)
        raw = b''
        for u in ch['pages']:
            s, b = soup(u)
            raw += b
            for sec in s.find_all('div', class_='Section'):
                head = sec.find('div', class_='SectionHead')
                if not head:
                    continue
                sid = norm(head.get('id') or '')
                htxt = norm(head.get_text(' '))
                htxt = re.sub(r'^§+\s*', '§ ', htxt)
                lines = ['# ' + htxt]
                for p in sec.find_all('p', recursive=False):
                    lines.append(norm(p.get_text(' ')))
                # the section's own source line: "11 Del. C. 1953, § 601; 58 Del. Laws, c. 497, § 1; ..."
                hist = []
                for el in head.next_siblings:
                    if getattr(el, 'name', None) == 'p':
                        continue
                    hist.append(el.get_text(' ') if hasattr(el, 'get_text') else str(el))
                h = norm(' '.join(hist))
                h = re.sub(r'\s+([;,.])', r'\1', h)
                if h:
                    lines.append(h)
                lab = sid or htxt
                a.add(key('sec', lab), '§ ' + lab, 'section', text_of(lines))
        a.sha256 = sha(raw)
        acts.append(a)
    return acts


def main():
    man = json.load(open(os.path.join(HERE, '.cache', 'manifest.json')))
    acts = constitution()
    for t in (11, 25, 8):
        acts += code_title(t, man['titles'][str(t)], None)
    country = {'code': 'US-DE', 'name': 'United States (Delaware)', 'slug': 'united-states-delaware', 'lang': 'en',
               'tz': 'America/New_York', 'future_branch': 'future',
               'publisher': {'name': 'The Delaware Code Online (Delaware General Assembly)', 'email': 'delcode@delcode.delaware.gov.invalid'},
               'default_in_force_rule': {'text': 'No dated history is published: each act is the oldest version available, dated by the source\'s own currency statement.',
                                         'source': SITE},
               'licence_note': 'Statute text is not copyrightable (Georgia v. Public.Resource.Org, 2020). Source: The Delaware Code Online, Delaware General Assembly.'}
    sources = [{'name': 'The Delaware Code Online', 'url': SITE, 'retrieved': RETRIEVED,
                'licence': 'Statute text carries no copyright (Georgia v. Public.Resource.Org, 2020). The site publishes the Code as the General Assembly\'s official text with a no-warranty disclaimer and no reuse restriction; it has no robots.txt.',
                'notes': 'Titles 8, 11 and 25 and the Constitution of 1897 as amended through July 1, 2025.'}]
    decisions = [
        'Each act is a single "oldest version available": the Delaware Code Online publishes only the current text, with no dated history.',
        f'Code acts are dated {CODE_DATE}, the date the site\'s home page gives ("acts enacted as of October 01, 2026, up to and including 85 Del. Laws, c. 550"); the Constitution acts are dated {CONST_DATE}, the date its index gives ("through July 1, 2025").',
        'One act per chapter of the Code and one per article of the Constitution; one unit per section, keyed by the number the site prints.',
        'The line after each section that cites the Delaware Code and the session laws (for example "58 Del. Laws, c. 497, § 1") is kept as the last line of the section; it is the Code\'s own source note, not an annotation.',
        'Sections the Code prints as ranges ("608-610") or lists ("623, 624") stay one unit under the range.']
    write_corpus(HERE, country, sources, acts, decisions)


if __name__ == '__main__':
    sys.path.insert(0, HERE)
    main()
