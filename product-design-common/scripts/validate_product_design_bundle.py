#!/usr/bin/env python3
from pathlib import Path
import re, sys

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
source_mode = root.name == 'product-design-skills' or (root / 'references' / 'community-github.md').exists()
refs_dir = root / 'product-design-common' / 'references'
errors = []
EXPECTED_SKILLS = {
    'product-design-workflow','product-design-router','market-context-reader','product-concept-brief','opportunity-framing',
    'journey-flow-mapper','concept-page-spec-writer','stitch-concept-generator','concept-review-gate',
    'product-design-handoff'
}
EXPECTED_REFS = {
    'product-design-workflow': {'product-design-contract.md','industry-quality-bar.md','e2e-artifact-contract.md','phase-orchestration.md','karpathy-product-design-rules.md','standards-and-sources.md','stitch-concept-rules.md','safety-boundaries.md'},
    'product-design-router': {'product-design-contract.md','routing-matrix.md','industry-quality-bar.md','safety-boundaries.md'},
    'market-context-reader': {'product-design-contract.md','market-context-rules.md','safety-boundaries.md','output-shapes.md','standards-and-sources.md'},
    'product-concept-brief': {'product-design-contract.md','market-context-rules.md','output-shapes.md','safety-boundaries.md'},
    'opportunity-framing': {'product-design-contract.md','opportunity-framing-rules.md','market-context-rules.md','output-shapes.md','safety-boundaries.md'},
    'journey-flow-mapper': {'product-design-contract.md','journey-flow-rules.md','output-shapes.md','safety-boundaries.md'},
    'concept-page-spec-writer': {'product-design-contract.md','concept-page-spec-rules.md','journey-flow-rules.md','output-shapes.md','industry-quality-bar.md','safety-boundaries.md'},
    'stitch-concept-generator': {'product-design-contract.md','stitch-concept-rules.md','concept-page-spec-rules.md','safety-boundaries.md','output-shapes.md','industry-quality-bar.md'},
    'concept-review-gate': {'product-design-contract.md','ux-quality-gates.md','positioning-marketing-risk.md','output-shapes.md','industry-quality-bar.md','standards-and-sources.md','safety-boundaries.md'},
    'product-design-handoff': {'product-design-contract.md','handoff-packet.md','output-shapes.md','e2e-artifact-contract.md','safety-boundaries.md'},
}
REQUIRED_REFS = set().union(*EXPECTED_REFS.values())
MAX_SKILL_LINES = 50
MAX_REF_WORDS = 320
MAX_TOTAL_MD_WORDS = 7600
OUTPUT_TERMS = {'assumptions','evidence','risks'}

def fm(text, skill):
    if not text.startswith('---\n'):
        errors.append(f'{skill}/SKILL.md missing frontmatter'); return {}
    parts=text.split('---\n',2)
    if len(parts)<3:
        errors.append(f'{skill}/SKILL.md malformed frontmatter'); return {}
    data={}
    for line in parts[1].splitlines():
        if ':' in line:
            k,v=line.split(':',1); data[k.strip()]=v.strip().strip('"')
    return data

def read_first(text):
    m=re.search(r'(?im)^Read first:\s*$', text)
    if not m: return ''
    lines=[]; started=False
    for line in text[m.end():].splitlines():
        if not started and not line.strip(): continue
        if not line.strip(): break
        started=True; lines.append(line)
    return '\n'.join(lines)

def output_block(text):
    m=re.search(r'(?im)^Output:\s*$', text)
    if not m: return ''
    rest=text[m.end():]
    n=re.search(r'(?m)^#{1,6}\s+', rest)
    return rest[:n.start()] if n else rest

def links(text):
    # Markdown refs in code spans, Markdown links, and bare relative paths.
    # Capture .md plus optional #fragment or ?query so bypasses cannot hide refs.
    pat=r'([^`\s)]+\.md(?:[#?][^`\s)]*)?)'
    out=set(re.findall(r'`'+pat+r'`', text))
    out.update(re.findall(r'\[[^\]]+\]\('+pat+r'\)', text))
    out.update(re.findall(r'(?<![\w`(])(\.\./[^\s`)]+\.md(?:[#?][^\s`)]*)?)', text))
    return out

def normalize_link(link):
    return re.split(r'[#?]', link, 1)[0]

def ref_name(link):
    link=normalize_link(link)
    prefix='../product-design-common/references/'
    if not link.startswith(prefix): return None
    r=link[len(prefix):]
    if '/' in r or '\\' in r or '..' in r or Path(r).name != r: return None
    return r

skill_dirs=[root/name for name in sorted(EXPECTED_SKILLS) if (root/name/'SKILL.md').exists()]
names={p.name for p in skill_dirs}
if source_mode:
    top_names={p.name for p in sorted(root.iterdir()) if p.is_dir() and (p/'SKILL.md').exists()}
    if top_names != EXPECTED_SKILLS:
        errors.append(f'skill set mismatch: missing={sorted(EXPECTED_SKILLS-top_names)} extra={sorted(top_names-EXPECTED_SKILLS)}')
else:
    if names != EXPECTED_SKILLS:
        errors.append(f'installed product-design skill set missing={sorted(EXPECTED_SKILLS-names)}')
    # Installed layouts must be hermetic too: archived/snapshot/temp copies of
    # known skills can confuse skill discovery even when canonical dirs exist.
    for p in root.rglob('SKILL.md'):
        rel = p.relative_to(root)
        if '.git' in p.parts:
            continue
        parent = p.parent.name
        if parent in EXPECTED_SKILLS and p != root / parent / 'SKILL.md':
            errors.append(f'duplicate installed product-design skill: {rel}')
        if parent.startswith('product-design-') and parent not in EXPECTED_SKILLS:
            errors.append(f'extra installed product-design-like skill: {rel}')
        if 'product-design-common' in rel.parts or 'references' in rel.parts:
            errors.append(f'nested support/reference SKILL.md in installed layout: {rel}')
if (root/'product-design-common'/'SKILL.md').exists():
    errors.append('product-design-common must not contain SKILL.md')
refs=set(p.name for p in refs_dir.glob('*.md'))
if refs != REQUIRED_REFS:
    errors.append(f'ref set mismatch: missing={sorted(REQUIRED_REFS-refs)} extra={sorted(refs-REQUIRED_REFS)}')
expected_skill_paths = {Path(name) / 'SKILL.md' for name in EXPECTED_SKILLS}
if source_mode:
    actual_skill_paths = {p.relative_to(root) for p in root.rglob('SKILL.md') if '.git' not in p.parts}
    if actual_skill_paths != expected_skill_paths:
        errors.append(f'recursive SKILL.md set mismatch: missing={sorted(str(p) for p in expected_skill_paths-actual_skill_paths)} extra={sorted(str(p) for p in actual_skill_paths-expected_skill_paths)}')
else:
    for name in EXPECTED_SKILLS:
        nested = [p for p in (root/name).rglob('SKILL.md') if p != root/name/'SKILL.md']
        for p in nested:
            errors.append(f'nested SKILL.md in installed skill: {p.relative_to(root)}')
for d in skill_dirs:
    text=(d/'SKILL.md').read_text()
    meta=fm(text,d.name)
    if meta.get('name') != d.name: errors.append(f'{d.name}/SKILL.md name mismatch')
    if not meta.get('description'): errors.append(f'{d.name}/SKILL.md missing description')
    elif len(meta['description'].split()) > 24: errors.append(f'{d.name}/SKILL.md description too long')
    if len(text.splitlines()) > MAX_SKILL_LINES: errors.append(f'{d.name}/SKILL.md too long')
    low=text.lower()
    for sec in ('read first:','workflow:','output:'):
        if sec not in low: errors.append(f'{d.name}/SKILL.md missing {sec}')
    rf=read_first(text)
    rf_links=links(rf)
    outside=text.replace(rf,'',1)
    for link in links(outside):
        if ref_name(link) is not None:
            errors.append(f'{d.name}/SKILL.md common ref outside Read first: {link}')
        elif normalize_link(link).endswith('.md') and not normalize_link(link).startswith('../product-design-common/references/'):
            errors.append(f'{d.name}/SKILL.md invalid md link: {link}')
    got=set()
    for link in rf_links:
        rn=ref_name(link)
        if rn is None: errors.append(f'{d.name}/SKILL.md invalid ref path: {link}')
        else: got.add(rn)
    exp=EXPECTED_REFS.get(d.name)
    if exp is None:
        errors.append(f'{d.name}/SKILL.md has no expected ref contract')
        continue
    if got != exp: errors.append(f'{d.name}/SKILL.md refs mismatch missing={sorted(exp-got)} extra={sorted(got-exp)}')
    out=output_block(text).lower()
    for term in OUTPUT_TERMS:
        if term not in out:
            errors.append(f'{d.name}/SKILL.md Output missing {term}')
for p in refs_dir.glob('*.md'):
    words=len(p.read_text().split())
    if words > MAX_REF_WORDS: errors.append(f'{p.name} too long: {words}')
# Sentinels for boundary regression.
sentinels={
    refs_dir/'product-design-contract.md':['Stitch','design-skills','Coding skills','Marketing/GTM','product-design-workflow','launch region/beachhead','strongest direct opponent','novelty delta'],
    refs_dir/'industry-quality-bar.md':['WCAG 2.2','UI concept','degraded','HTML','screenshots','whole user problem','success criteria','ui_concept_artifact_present','ui_concept_verdict','launch region/beachhead','AI wrapper','Visual-region gate'],
    refs_dir/'e2e-artifact-contract.md':['00-run-manifest.md','13-artifact-check.txt','09-ui-concept','scorecard table','ui_concept_artifact_present','beachhead','strongest direct opponent','novelty delta','geography drift','check_phase_status.py'],
    refs_dir/'phase-orchestration.md':['orchestrator','router','context packet','file manager','Leaf responsibilities','resume','final_audit','WBS phases','pd-bootstrap','pd-market','pd-opportunity','pd-screen','pd-previsual','pd-visuals','pd-ui','pd-final-audit','Gate proof rule'],
    refs_dir/'karpathy-product-design-rules.md':['evidence before confidence','verify before saying done'],
    refs_dir/'standards-and-sources.md':['Double Diamond','NN/g','WCAG 2.2','GOV.UK Design System','GOV.UK Service Standard/Manual','Empathize','Australian Government Style Manual','Australian Digital Experience Policy','Digital Service Standard','NSW Design System','Queensland Government Design System','US Web Design System','Canada GC Design System','18F Methods','Apple HIG','Material Design','Atlassian Design System','IBM Carbon','not copied layouts','component source','Canvas Planner/API','MyStudyLife','TigerPath'],
    refs_dir/'market-context-rules.md':['source claim','signal','inference','assumption','Canvas student planner','launch region/beachhead','strongest direct opponent','kill_or_pivot_condition'],
    refs_dir/'opportunity-framing-rules.md':['success measure','smallest useful concept'],
    refs_dir/'ux-quality-gates.md':['persona/scenario/goal','WCAG 2.2','action items'],
    refs_dir/'handoff-packet.md':['artifact inventory','degraded/blocked reason'],
    refs_dir/'positioning-marketing-risk.md':['misleading','campaign plans'],
    refs_dir/'stitch-concept-rules.md':['UI concept evidence','not source truth'],
    refs_dir/'safety-boundaries.md':['credentials','external Stitch','Generated UI concept artifacts'],
}
for p,terms in sentinels.items():
    if not p.exists():
        errors.append(f'missing sentinel file: {p.relative_to(root)}')
        continue
    hay=p.read_text().lower()
    for term in terms:
        if term.lower() not in hay: errors.append(f'{p.relative_to(root)} missing sentinel {term}')
word_count=sum(len(p.read_text(errors='ignore').split()) for p in list(root.glob('*.md')) + list(refs_dir.glob('*.md')) + [p/'SKILL.md' for p in skill_dirs])
if word_count > MAX_TOTAL_MD_WORDS: errors.append(f'total markdown word count too high: {word_count}')
if errors:
    print('FAIL')
    for e in errors: print('-', e)
    sys.exit(1)
print(f'OK: {len(skill_dirs)} skills, {len(refs)} references, {word_count} markdown words')
