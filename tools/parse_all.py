"""Wave 3 (2026-11-03, private): the whole Delaware Code. parse.py's main() rules: the Constitution and Titles 8, 11
and 25 from the first-build manifest (byte for byte as first published), every other title from manifest_all.json,
same section rules, one act per chapter, dated by the Code Online's currency notice. Reads .cache only."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parse as P
from state_lib import Act, key, norm, sha, text_of, write_corpus

FIRST = (11, 25, 8)
# Home page, re-read 2026-11-03: "This version includes all acts enacted as of October 01, 2026, up to and including 85 Del. Laws, c. 550."
P.CODE_DATE = '2026-10-01'


def chapter_act(t, ch):
    cid = ch['id']
    s0, _ = P.soup(ch['url'])
    h2 = s0.find('h2')
    ctitle = norm(h2.get_text(' ')) if h2 else ''
    m = re.fullmatch(r'c(\d+)([a-z]*)', cid)
    n, suf = int(m.group(1)), m.group(2)
    a = Act(f'title-{t:02d}-chapter-{n:03d}{suf}', f'{t} Del. C. ch. {n}{suf.upper()}',
            f'Delaware Code, Title {t}, Chapter {n}{suf.upper()}' + (f': {ctitle}' if ctitle else ''), ch['url'], P.CODE_DATE)
    raw = b''
    for u in ch['pages']:
        s, b = P.soup(u)
        raw += b
        for sec in s.find_all('div', class_='Section'):
            head = sec.find('div', class_='SectionHead')
            if not head:
                continue
            sid = norm(head.get('id') or '')
            htxt = re.sub(r'^§+\s*', '§ ', norm(head.get_text(' ')))
            lines = ['# ' + htxt]
            for p in sec.find_all('p', recursive=False):
                lines.append(norm(p.get_text(' ')))
            hist = []
            for el in head.next_siblings:
                if getattr(el, 'name', None) == 'p':
                    continue
                hist.append(el.get_text(' ') if hasattr(el, 'get_text') else str(el))
            h = re.sub(r'\s+([;,.])', r'\1', norm(' '.join(hist)))
            if h:
                lines.append(h)
            lab = sid or htxt
            a.add(key('sec', lab), '§ ' + lab, 'section', text_of(lines))
    a.sha256 = sha(raw)
    return a


def main():
    man = json.load(open(os.path.join(HERE, '.cache', 'manifest.json')))
    alln = json.load(open(os.path.join(HERE, '.cache', 'manifest_all.json')))
    acts = P.constitution()
    for t in FIRST:
        acts += P.code_title(t, man['titles'][str(t)], None)
    for t in sorted(int(x) for x in alln['titles']):
        if t in FIRST:
            continue
        for ch in alln['titles'][str(t)]:
            a = chapter_act(t, ch)
            if a.units:
                acts.append(a)
    # same country/sources/decisions as parse.main(), widened
    import inspect
    src = inspect.getsource(P.main)
    ns = {}
    import textwrap
    exec(textwrap.dedent(src[src.index("    country = "):src.index("    write_corpus(")]), {**P.__dict__}, ns)
    sources, decisions = ns['sources'], ns['decisions']
    sources[0]['notes'] = 'Every title of the Delaware Code (Titles 8, 11 and 25 retrieved 2026-10-30, the rest 2026-11-03) and the Constitution of 1897 as amended through July 1, 2025.'
    decisions.append('Wave 3 (2026-11-03): every other title of the Code was added, one act per chapter, by the same rules and the same date (the site\'s currency notice still read "as of October 01, 2026, up to and including 85 Del. Laws, c. 550" on 2026-11-03). Reserved or repealed chapters with no section text are left out.')
    write_corpus(HERE, ns['country'], sources, acts, decisions)
    print(len(acts), 'acts')


if __name__ == '__main__':
    main()
