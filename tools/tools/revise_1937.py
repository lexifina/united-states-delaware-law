"""Source-based commencement revision; no live requests to the stopped host."""
import collect_1927 as common
import ctypes
from datetime import date, datetime, timedelta
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HERE = common.HERE
JOB = HERE.parent / 'gpt-workers/jobs/q-1937'
REV = JOB / 'revision-01'
EVIDENCE = REV / 'evidence'
common.JOB = REV
common.EVIDENCE = EVIDENCE
fs = common.fs
fs.DRY = True
os.environ['GITLAW_NO_CHECKOUT'] = '1'
HELD = {
    140: 'Known commencement 18 months after approval (2027-02-20) lies after this bounded current-head batch; future record held separately.',
    142: 'Different provisions commence immediately or after an unverified Register of Regulations funding notice; no single document commencement date.',
    145: 'Section 1 commencement depends on House Bill 36 passage and enactment; the necessary official event has not been verified.',
    167: 'Sections 1-3 commence on the earlier of 2026-01-01 or a regulatory notice; notice date not verified and other sections differ.',
    174: 'Compact commencement depends on enactment in a seventh member state; official triggering event not verified.',
    176: 'Effective-date section applies the Act to policies after 2026-12-31; other implementation duties differ, so no single whole-document commencement is asserted.',
    186: 'Separate commencement clauses govern different section groups; held for a provision-level commencement representation.',
    188: 'Act commences on seventh-state compact enactment; required official notice/event not verified.',
}

def save(name, obj):
    (EVIDENCE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def setup():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
    with (JOB / 'pids.txt').open('a') as stream: stream.write(str(os.getpid()) + '\n')
    original = subprocess.Popen
    def tracked(*args, **kwargs):
        kwargs.setdefault('creationflags', 0x4000)
        process = original(*args, **kwargs)
        with (JOB / 'pids.txt').open('a') as stream: stream.write(str(process.pid) + '\n')
        return process
    subprocess.Popen = tracked

def source(url):
    raw = fs.get(url, cache=REV / 'empty-source-cache', wait=False, tries=1)
    if not raw or fs.last_status() in (403,429):
        raise RuntimeError('Stopped or absent official cached response: ' + url)
    digest = hashlib.sha256(raw).hexdigest()
    (EVIDENCE / (digest + '.html')).write_bytes(raw)
    with (EVIDENCE / 'fresh-source-provenance.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps({'url':url,'sha256':digest,'bytes':len(raw),'scheduler_dry':True,'status':fs.last_status()})+'\n')
    return raw

def revised(item, raw):
    act = common.parse(item, raw)
    number = int(act['slug'].rsplit('-',1)[1])
    dom = common.law_node(raw)
    text = ' '.join(dom.get_text(' ',strip=True).split())
    paragraphs = [p.get_text(' ',strip=True) for p in dom.find_all('p')
                  if re.search(r'\beffective\b|takes? effect|\bin force\b|\bcommenc|retroactiv',p.get_text(),re.I)]
    if number in HELD:
        return None, {'act':act['slug'],'url':act['url'],'reason':HELD[number],'source_paragraphs':paragraphs}
    approved = date.fromisoformat(act['enacted'])
    clause = re.search(r'This Act\s+(?:(?:shall\s+)?(?:become|becomes|is)\s+effective|takes? effect)\s+([^.]*)\.',text,re.I)
    mode = 'approval record; no explicit Act commencement clause'
    commencement = approved
    quote = None
    if clause:
        quote = clause.group(0)
        tail = clause.group(1).strip()
        absolute = re.match(r'(?:on\s+)?([A-Z][a-z]+\s+\d{1,2},\s+\d{4})\b',tail)
        days = re.match(r'(\d+)\s+days?\s+(?:following|after)\s+(?:its\s+)?enactment(?:\s+into law)?\b',tail,re.I)
        if absolute:
            commencement = datetime.strptime(absolute[1],'%B %d, %Y').date()
            mode = 'explicit Act commencement date'
        elif days:
            commencement = approved + timedelta(days=int(days[1]))
            mode = 'approval plus source-stated day interval'
        elif re.match(r'immediately\b|upon\s+(?:its\s+)?enactment(?:\s+into law)?\b',tail,re.I):
            mode = 'explicit immediate/enactment commencement'
        elif re.match(r'on January 1 following its enactment into law\b',tail,re.I):
            commencement = date(approved.year + 1,1,1)
            mode = 'January 1 following source approval'
        else:
            return None, {'act':act['slug'],'url':act['url'],'reason':'Unsupported or conditional Act commencement clause','quote':quote}
    # Catch a non-Act sectional commencement clause rather than treating it as absent.
    elif re.search(r'(?:Section[s]?\s+\d|This Compact)[^.]{0,120}\b(?:takes? effect|effective|come into effect)',text,re.I):
        return None, {'act':act['slug'],'url':act['url'],'reason':'Sectional/compact commencement requires separate evidence','source_paragraphs':paragraphs}
    version = act['versions'][0]
    version['from'] = commencement.isoformat()
    version['text_as_of'] = commencement.isoformat()
    version['retrieved'] = '2026-11-13'
    version['in_force_unknown'] = clause is None
    version['in_force_basis'] = (f'Official commencement clause: {quote} Approval: {approved.isoformat()}; {mode}.' if clause else
        f'As-enacted instrument recorded on official approval {approved.isoformat()}; no explicit Act commencement clause located. Commencement remains unknown; the approval record is not asserted as an in-force date.')
    version['note'] = 'As-enacted session-law instrument; official insertion/deletion HTML preserved. ' + ('Source-stated commencement used.' if clause else 'Approval record with commencement unknown.')
    if clause:
        act['in_force'] = commencement.isoformat()
    if commencement > date(2026,11,13):
        return None, {'act':act['slug'],'url':act['url'],'reason':'Known future commencement outside bounded current-head batch','date':commencement.isoformat(),'quote':quote}
    return act, {'act':act['slug'],'approved':approved.isoformat(),'from':commencement.isoformat(),
                 'in_force_unknown':version['in_force_unknown'],'mode':mode,'quote':quote,'source_paragraphs':paragraphs}

def prepare():
    setup()
    cache = REV / 'empty-source-cache'
    if cache.exists():
        raise RuntimeError('Fresh-source cache must not exist before preparation')
    cache.mkdir()
    save('cache-initial-state.json',{'path':str(cache),'entries':[],'network_disabled':True})
    listing_raw = source('https://legis.delaware.gov/SessionLaws/Chapters?volume=166')
    page = common.BeautifulSoup(listing_raw.decode('utf-8'),'lxml')
    listing = [{'label':a.get_text(' ',strip=True),'url':a['href']} for a in page.find_all('a',href=True) if 'Chapter?id=' in a['href']]
    items = [i for i in listing if 111 <= int(i['label'].split()[-1]) <= 208]
    if len(items) != 98:
        raise RuntimeError('Official bounded listing count changed')
    acts, held, dates, proof, bodies = [], [], [], [], {}
    for item in items:
        url = 'https://legis.delaware.gov' + item['url'] if item['url'].startswith('/') else item['url']
        raw = source(url)
        act, audit = revised(item, raw)
        if act is None:
            held.append(audit)
        else:
            again, _ = revised(item, raw)
            if act != again: raise RuntimeError('Two revised parses differ')
            acts.append(act); dates.append(audit); proof.append(common.compare_source(act,raw)); bodies[act['url']] = raw
        print(item['label'],'accepted',len(acts),'held',len(held),flush=True)
    part = common.part_for(acts)
    part['decisions'] = ['Explicit Act commencement dates and source-stated intervals take precedence over approval. Approval records remain in_force_unknown only when no commencement clause is stated. Conditional, sectional and future commencement instruments are held. Source HTML remains as enacted; no consolidated Code reconstruction.']
    part['sources'][0]['notes'] = 'As-enacted instruments. Explicit commencement clauses take precedence; approval-record dates with unknown commencement are labelled separately.'
    (REV/'held').mkdir(exist_ok=True)
    candidate = REV/'held/1937-revision-01-session-laws-085-111-208.json'
    candidate.write_text(json.dumps(part,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    save('held-acts.json',held); save('date-audit.json',dates);save('source-proof.json',proof)
    import build, check, private
    stage = REV/'standalone-input'
    (stage/'repo').mkdir(parents=True)
    descriptor = {'country':build.load(HERE)[0]['country'],'laws':{},'applies':[],**part}
    (stage/'corpus.json').write_text(json.dumps(descriptor,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    (stage/'repo/LICENSE').write_bytes((HERE/'repo/LICENSE').read_bytes())
    rows = '\n'.join(f'| `{a["slug"]}/` | {a["short"]} | {a["enacted"]} | {a["versions"][0]["from"]} | {"Unknown; approval record" if a["versions"][0]["in_force_unknown"] else "Explicit source clause"} |' for a in acts)
    (stage/'repo/README.md').write_text('# Laws of Delaware: as-enacted instruments\n\nOfficial legislative HTML includes insertion/deletion styling. Explicit commencement takes precedence over approval; records without stated commencement remain unknown.\n\n| Folder | Instrument | Approval | Record start | Date basis |\n| --- | --- | --- | --- | --- |\n'+rows+'\n',encoding='utf-8')
    d1,d2 = REV/'standalone-one',REV/'standalone-two'
    build.build(stage,d1,'2026-11-13')
    checked=check.check(d1,stage/'corpus.json')
    save('standalone-check.json',checked)
    if not common.check_ok(checked): raise RuntimeError('Standalone check errors')
    old=sys.argv
    try:
        sys.argv=['build.py',str(stage),'--repo',str(d2),'--docs-date','2026-11-13','--compare',str(d1)]
        try: build.main()
        except SystemExit as error:
            if error.code: raise RuntimeError('Standalone compare failed')
    finally: sys.argv=old
    comparison=json.loads((stage/'verification.json').read_text(encoding='utf-8'))['rebuild']
    save('standalone-compare.json',comparison)
    builtproof=[common.compare_source(a,bodies[a['url']],d1) for a in acts]
    save('built-source-proof.json',builtproof)
    save('prepare-summary.json',{'accepted':len(acts),'held':len(held),'candidate':str(candidate),
                               'cache_initially_empty':True,'scheduler_responses':len(items)+1,
                               'standalone_compare':comparison,'current_head_gate_pending':True})
    print('PREPARED',len(acts),'held',len(held),'current-head gate still required',flush=True)

if __name__ == '__main__': prepare()
