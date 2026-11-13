"""Finish the held commencement revision against the supplied published main."""
import revise_1937 as revision
import collect_1927 as common
import ctypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.parse import urljoin

HERE = common.HERE
JOB = HERE.parent / 'gpt-workers/jobs/q-1937'
RUN = JOB / 'revision-02'
EVIDENCE = RUN / 'evidence'
SCRATCH = JOB / 'published'
DAY = '2026-11-13'
NAME = '1937-revision-02-session-laws-085-111-208.json'
common.JOB = JOB
common.EVIDENCE = EVIDENCE
revision.REV = RUN
revision.EVIDENCE = EVIDENCE
revision.fs.DRY = True
os.environ['GITLAW_NO_CHECKOUT'] = '1'


def save(name, obj):
    (EVIDENCE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def disk():
    free = shutil.disk_usage('C:\\').free
    if free < 40_000_000_000:
        raise RuntimeError('retry later: disk below 40 GB')
    return free


def setup():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    common.record(os.getpid())
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
    original = subprocess.Popen
    def tracked(*args, **kwargs):
        kwargs.setdefault('creationflags', 0x4000)
        process = original(*args, **kwargs)
        common.record(process.pid)
        return process
    subprocess.Popen = tracked
    disk()


def cli(args):
    import build
    previous = sys.argv
    try:
        sys.argv = ['build.py', *map(str, args)]
        try:
            build.main()
        except SystemExit as error:
            if error.code:
                raise RuntimeError('Builder CLI failed: ' + str(error.code))
    finally:
        sys.argv = previous


def checked(repo, source, name):
    import check
    result = check.check(repo, source)
    save(name, result)
    if not common.check_ok(result):
        raise RuntimeError('Checker errors: ' + name)
    print('CHECK', name, {k: v for k, v in result.items() if k != 'details'}, flush=True)
    return result


def run():
    setup()
    import build, private, published_parts
    if (EVIDENCE / 'completed.json').exists():
        print('Completed run already exists; inspect rather than mutate.', flush=True)
        return
    if (EVIDENCE / 'baseline.json').exists():
        raise RuntimeError('Incomplete run exists; inspect its checkpoint before resuming')
    baseline = common.git(SCRATCH, 'rev-parse', 'HEAD')
    origin = common.git(SCRATCH, 'rev-parse', 'origin/main')
    if baseline != origin or common.git(SCRATCH, 'status', '--porcelain'):
        raise RuntimeError('Supplied published clone must be clean and at origin/main')
    tags = dict(line.rsplit(' ', 1)[::-1] for line in common.git(
        SCRATCH, 'for-each-ref', '--format=%(objectname) %(refname)', 'refs/tags').splitlines())
    present = {a['slug'] for a in json.loads(common.git(SCRATCH, 'show', 'HEAD:data/acts.json'))['acts']}
    inherited = {}
    for path in sorted((HERE / 'corpus.d').glob('*.json')):
        marker = path.with_suffix('.PUBLISH')
        if not marker.exists():
            raise RuntimeError('Unexpected inherited unsigned part: ' + path.name)
        inherited[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        inherited[str(marker)] = hashlib.sha256(marker.read_bytes()).hexdigest()
    published_parts.required(SCRATCH, HERE, baseline)
    save('baseline.json', {'head': baseline, 'acts': len(present), 'tags': tags,
                           'inherited_hashes': inherited, 'free_bytes': disk()})
    save('host-stop-respected.json', {'record': json.loads((JOB / 'evidence/host-stop.json').read_text()),
                                     'live_requests_this_run': 0, 'scheduler_cache_only': True})
    for path in JOB.glob('report.md'):
        shutil.copyfile(path, EVIDENCE / 'prior-report.md')
    # Only shared scheduler cache is read; DRY prevents live contact with the stopped host.
    (RUN / 'empty-source-cache').mkdir()
    save('cache-initial-state.json', {'entries': [], 'network_disabled': True})
    listing_raw = revision.source('https://legis.delaware.gov/SessionLaws/Chapters?volume=166')
    page = common.BeautifulSoup(listing_raw.decode('utf-8'), 'lxml')
    rows = [{'label': a.get_text(' ', strip=True), 'url': a['href']}
            for a in page.find_all('a', href=True) if 'Chapter?id=' in a['href']]
    numbers = [int(r['label'].split()[-1]) for r in rows]
    if len(numbers) != len(set(numbers)) or len(numbers) != 420:
        raise RuntimeError('Official retained listing is unexpected')
    items = [r for r in rows if 111 <= int(r['label'].split()[-1]) <= 208]
    save('range-audit.json', {'listing_count': len(rows), 'candidates': len(items),
                             'already_published': sum(f'session-law-085-chapter-{int(r["label"].split()[-1]):03d}' in present for r in items)})
    acts, held, dates, proof, bodies = [], [], [], [], {}
    for item in items:
        disk()
        url = urljoin('https://legis.delaware.gov/', item['url'])
        raw = revision.source(url)
        try:
            act, audit = revision.revised(item, raw)
            if act is None:
                held.append(audit)
            elif act['slug'] not in present:
                again, second_audit = revision.revised(item, raw)
                if act != again or audit != second_audit:
                    raise ValueError('Two source parses differ')
                proof.append(common.compare_source(act, raw))
                acts.append(act)
                dates.append(audit)
                bodies[act['url']] = raw
        except ValueError as error:
            held.append({'chapter': item['label'], 'url': url, 'reason': str(error)})
        print(item['label'], 'accepted', len(acts), 'held', len(held), flush=True)
    save('date-audit.json', dates)
    save('held-acts.json', held)
    save('source-proof.json', proof)
    if len(acts) != 90 or len(held) != 8:
        raise RuntimeError('Revised candidate count differs; inspect source holds')
    part = common.part_for(acts)
    part['decisions'] = ['As-enacted instruments: explicit whole-Act commencement clauses take precedence over approval. Unknown commencement is labelled as an approval record. Conditional, sectional and future commencement instruments are held. Original source legal text and markup are unchanged.']
    part['sources'][0]['notes'] = 'As-enacted official instruments. Explicit commencement clauses take precedence over approval; approval records with unknown commencement are labelled separately.'
    text = json.dumps(part, ensure_ascii=False, indent=1) + '\n'
    stage = RUN / 'standalone-input'
    (stage / 'repo').mkdir(parents=True)
    descriptor = {'country': build.load(HERE)[0]['country'], 'laws': {}, 'applies': [], **part}
    (stage / 'corpus.json').write_text(json.dumps(descriptor, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    shutil.copyfile(HERE / 'repo/LICENSE', stage / 'repo/LICENSE')
    newrows = '\n'.join(f'| `{a["slug"]}/` | {a["short"]} | {a["enacted"]} | {a["versions"][0]["from"]} | {"Unknown; approval record" if a["versions"][0]["in_force_unknown"] else "Source commencement clause"} |' for a in acts)
    section = ('\n## Additional Laws of Delaware: as-enacted instruments\n\n'
               'The following instruments preserve the official legislative HTML, including inserted and deleted wording. '
               'Explicit whole-Act commencement dates take precedence over approval. Where no explicit commencement clause is stated, '
               'the record starts at official approval and commencement remains unknown. Later amendments are not reconstructed.\n\n'
               '| Folder | Instrument | Approval | Record start | Date basis |\n'
               '| --- | --- | --- | --- | --- |\n' + newrows + '\n\n'
               'Source: [Delaware General Assembly, Laws of Delaware](https://legis.delaware.gov/SessionLaws/Chapters?volume=166). '
               'Volume 85 coverage remains partial. Eight instruments with conditional, sectional or future commencement are not included in this addition.\n')
    (stage / 'repo/README.md').write_text('# Laws of Delaware\n' + section, encoding='utf-8')
    first, second = RUN / 'build-one', RUN / 'build-two'
    build.build(stage, first, DAY)
    checked(first, stage / 'corpus.json', 'standalone-check.json')
    cli([stage, '--repo', second, '--docs-date', DAY, '--compare', first])
    save('standalone-compare.json', json.loads((stage / 'verification.json').read_text())['rebuild'])
    save('standalone-built-source-proof.json', [common.compare_source(a, bodies[a['url']], first) for a in acts])
    # The unchanged local clone supplies all existing history to a second deterministic append.
    replica = RUN / 'build-append-compare'
    subprocess.run(['git', '-c', 'gc.auto=0', 'clone', '--local', '--no-checkout', str(SCRATCH), str(replica)], check=True)
    if common.git(replica, 'rev-parse', 'HEAD') != baseline:
        raise RuntimeError('Local compare clone baseline changed')
    live = HERE / 'corpus.d' / NAME
    if live.exists():
        raise RuntimeError('Refusing existing part overwrite')
    oldreadme = (HERE / 'repo/README.md').read_bytes()
    oldjurisdiction = (HERE / 'repo/jurisdiction.json').read_bytes()
    (EVIDENCE / 'source-readme-before.md').write_bytes(oldreadme)
    (EVIDENCE / 'source-jurisdiction-before.json').write_bytes(oldjurisdiction)
    live.write_text(text, encoding='utf-8', newline='\n')
    (HERE / 'repo/README.md').write_text(common.git(SCRATCH, 'show', baseline + ':README.md') + '\n' + section, encoding='utf-8', newline='\n')
    jurisdiction = json.loads(oldjurisdiction)
    jurisdiction['coverage'] = {'code': 'Constitution and all 31 Delaware Code titles; single consolidated versions',
                                'session_laws': 'Partial Volume 85 as-enacted instruments with source commencement or labelled approval records',
                                'excluded': ['Administrative Code', 'municipal charters', 'unrepresented session-law instruments and earlier history']}
    (HERE / 'repo/jurisdiction.json').write_text(json.dumps(jurisdiction, indent=2) + '\n', encoding='utf-8')
    errors = build.validate(build.load(HERE)[0])
    save('all-parts-validation.json', {'errors': errors})
    if errors:
        raise RuntimeError('Live corpus validation failed')
    disk()
    cli([HERE, '--repo', SCRATCH, '--docs-date', DAY, '--append'])
    save('appended-checkpoint.json', {'head': common.git(SCRATCH, 'rev-parse', 'HEAD'), 'pending_marker_written': False})
    full = checked(SCRATCH, HERE / 'corpus.json', 'full-check.json')
    builtproof = [common.compare_source(a, bodies[a['url']], SCRATCH) for a in acts]
    save('built-source-proof.json', builtproof)
    # Second append starts from the same unchanged published main; compare all history and tag objects.
    cli([HERE, '--repo', replica, '--docs-date', DAY, '--append', '--compare', SCRATCH])
    comparison = json.loads((HERE / 'verification.json').read_text())['rebuild']
    save('full-append-compare.json', comparison)
    if not comparison['identical']:
        raise RuntimeError('Full deterministic append comparison failed')
    head = common.git(SCRATCH, 'rev-parse', 'HEAD')
    findings = private.audit_push(SCRATCH, head, baseline)
    save('privacy-audit.json', findings)
    if findings:
        raise RuntimeError('Privacy audit failed')
    subprocess.run(['git', '-C', str(SCRATCH), 'merge-base', '--is-ancestor', baseline, head], check=True)
    beforepaths = set(common.git(SCRATCH, 'ls-tree', '-r', '--name-only', baseline).splitlines())
    changed = common.git(SCRATCH, 'diff', '--name-only', baseline, head).splitlines()
    changedlaws = [p for p in changed if p in beforepaths and p.endswith('.md') and '/' in p
                   and not p.endswith('/README.md') and not p.startswith('tools/')]
    nowtags = dict(line.rsplit(' ', 1)[::-1] for line in common.git(
        SCRATCH, 'for-each-ref', '--format=%(objectname) %(refname)', 'refs/tags').splitlines())
    if changedlaws or any(nowtags.get(k) != v for k, v in tags.items()):
        raise RuntimeError('Published law files or tag objects changed')
    if any(hashlib.sha256(Path(p).read_bytes()).hexdigest() != h for p, h in inherited.items()):
        raise RuntimeError('Inherited input or approved marker changed')
    digest = hashlib.sha256(live.read_bytes()).hexdigest()
    save('preservation.json', {'baseline': baseline, 'head': head, 'changed_existing_law_files': changedlaws,
                             'published_tags_preserved': len(tags), 'new_tags': len(nowtags) - len(tags),
                             'inherited_hashes_match': True, 'part_sha256': digest})
    markertext = ('q-1937 revision 02: 90/90 official source text and markup comparisons; '
                  'commencement audit; full check 0 errors; two published-main appends --compare identical; '
                  'audit clean. SHA-256 ' + digest + '. Independent review required.\n')
    for marker in (live.with_suffix('.PUBLISH.pending'), Path(str(live) + '.PUBLISH.pending')):
        if marker.exists():
            raise RuntimeError('Refusing existing marker overwrite')
        marker.write_text(markertext, encoding='utf-8')
    result = {'status': 'partial', 'reason': 'Added 90 source-verified revised Volume 85 instruments; eight commencement holds and 212 later chapters remain under recorded HTTP 403 host stop; other depth gaps remain.',
              'parts': ['corpus.d/' + NAME], 'scratch_path': str(SCRATCH), 'scratch_head': head,
              'acts_added': len(acts), 'held': len(held) + 212 + 8 + 52}
    (JOB / 'result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    save('completed.json', {'result': result, 'full_check': full, 'full_compare': comparison,
                          'source_compared': len(proof), 'explicit_commencement': sum(not d['in_force_unknown'] for d in dates),
                          'unknown_commencement': sum(d['in_force_unknown'] for d in dates),
                          'scheduler_responses': len(items) + 1, 'live_requests': 0, 'free_bytes': disk()})
    print('COMPLETED', json.dumps(result), flush=True)


if __name__ == '__main__':
    run()
