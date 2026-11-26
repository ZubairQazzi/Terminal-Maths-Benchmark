"""Finite-corpus screening, not a proof of plagiarism absence.
Raw metrics retained; narrowly specified boilerplate/metadata exclusions are
applied before adjusted text screening. Scientific objectives are never removed.
"""
from pathlib import Path
from collections import Counter
import ast,hashlib,io,json,math,re,tokenize
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
ROOT=Path(__file__).resolve().parents[1];SOURCES=ROOT/'authoring/sources'
OUT=ROOT/'authoring/originality';OUT.mkdir(parents=True,exist_ok=True)
EXCLUDED_TERMS=set('GSE273600 U2OS DmrPERK Dmr PERK Parental UT Dim Ars Tg RNA RNAseq seq TPM Salmon Ensembl GRCh38 ATF4 ISR eIF2 alpha arsenite thapsigargin dimerizer gene genes sample samples expression count counts replicate replicates untreated treatment treatments transcript transcripts biological biology scientific'.lower().split())
SUFFIX=re.compile(r'You have \d+ seconds to complete this task\. Do not cheat by using online solutions or hints specific to this task\.',re.I)
def norm(text,adjusted=True):
    text=re.sub(r'<!--.*?-->',' ',text,flags=re.S)
    text=re.sub(r'^.*harbor-canary.*$',' ',text,flags=re.M)
    if adjusted:
        text=SUFFIX.sub(' ',text)
        text=re.sub(r'GSM\d+|GSE\d+|ENSG\d+(?:\.\d+)?',' ',text,flags=re.I)
        text=re.sub(r'(?:/app|/root|/logs|/tests|/solution)/[A-Za-z0-9_./-]+',' ',text)
    tokens=re.findall(r'[a-z][a-z0-9_]*',text.lower())
    return [t for t in tokens if not adjusted or t not in EXCLUDED_TERMS]
def grams(tokens,n=5):return set(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))
def lexical(a,b):
    x,y=grams(a),grams(b);inter=x&y
    return {'fivegram_jaccard_pct':100*len(inter)/max(1,len(x|y)),'task_fivegram_containment_pct':100*len(inter)/max(1,len(x)),'reference_fivegram_containment_pct':100*len(inter)/max(1,len(y)),'matched_fivegrams':len(inter),'task_fivegrams':len(x),'reference_fivegrams':len(y),'example_matches':[' '.join(g) for g in sorted(inter)[:2]]}
def code_tokens(text):
    try:
        tree=ast.parse(text)
        # Remove imports and standalone documentation strings from science-code screen.
        ranges=[]
        for n in ast.walk(tree):
            if isinstance(n,(ast.Import,ast.ImportFrom)) or (isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str)):
                ranges.extend(range(n.lineno,n.end_lineno+1))
        text='\n'.join(line for i,line in enumerate(text.splitlines(),1) if i not in ranges)
        toks=[t.string for t in tokenize.generate_tokens(io.StringIO(text).readline) if t.type not in (tokenize.COMMENT,tokenize.NL,tokenize.NEWLINE,tokenize.INDENT,tokenize.DEDENT,tokenize.ENCODING,tokenize.ENDMARKER)]
        return toks,Counter(type(n).__name__ for n in ast.walk(tree))
    except (SyntaxError,tokenize.TokenError,IndentationError):return re.findall(r'\w+|[^\s\w]',text),Counter()
manifest=json.loads((SOURCES/'corpus_manifest.json').read_text())
refs=[]
for row in manifest['sources']:
    if row['status']!='downloaded':continue
    p=SOURCES/row.get('text_file',row['file'])
    if p.suffix.lower() not in ('.txt','.md','.py','.r','.rmd','.sh'):continue
    text=p.read_text(encoding='utf-8',errors='replace')
    # Article reference lists are not task objectives; use abstract/body rather than citations.
    if row['kind'] in ('publication','published_reanalysis','rna_seq_method','public_bioinformatics_benchmark'):
        for marker in ('\nReferences\n','\nREFERENCES\n'):
            if marker in text:text=text.split(marker)[0]
    refs.append(dict(row,text=text,path=str(p)))
# User-provided local reference tasks: compare scientific instructions, not reports or keys.
for name in ('task-2','task-3','math-benchmark'):
    p=ROOT.parent/name/'instruction.md'
    if p.exists():refs.append({'file':'local-reference/'+name+'/instruction.md','url':'local supplied workspace example','kind':'supplied_reference','text':p.read_text(encoding='utf-8',errors='replace'),'path':str(p)})
tasks=[]
for i in (1,2):
    base=ROOT/f'biology-task-{i}'
    p=base/'task/instruction.md'
    if not p.exists():raise RuntimeError('Task not implemented: '+str(p))
    tasks.append({'name':f'biology-task-{i}','base':base,'instruction':p.read_text(encoding='utf-8'),'solution': '\n'.join(p.read_text(encoding='utf-8') for p in (base/'task/solution').glob('*.py')),'tests':'\n'.join(p.read_text(encoding='utf-8') for p in (base/'task/tests').glob('*.py'))})
documents=[' '.join(norm(t['instruction'])) for t in tasks]+[' '.join(norm(r['text'])) for r in refs]
vec=TfidfVectorizer(ngram_range=(1,2),stop_words='english',sublinear_tf=True)
m=vec.fit_transform(documents);cos=(m[:2]@m.T).toarray()*100
pair={'tasks':[t['name'] for t in tasks],'raw':lexical(norm(tasks[0]['instruction'],False),norm(tasks[1]['instruction'],False)),'adjusted':lexical(norm(tasks[0]['instruction']),norm(tasks[1]['instruction'])),'adjusted_tfidf_cosine_pct':float(cos[0,1]),'code':{}}
for label in ('solution','tests'):
    a,sa=code_tokens(tasks[0][label]);b,sb=code_tokens(tasks[1][label]);ga,gb=grams(a,12),grams(b,12)
    keys=sa.keys()|sb.keys();dot=sum(sa[k]*sb[k] for k in keys);den=math.sqrt(sum(v*v for v in sa.values())*sum(v*v for v in sb.values()))
    pair['code'][label]={'twelve_token_jaccard_pct':100*len(ga&gb)/max(1,len(ga|gb)),'task1_token_containment_pct':100*len(ga&gb)/max(1,len(ga)),'task2_token_containment_pct':100*len(ga&gb)/max(1,len(gb)),'ast_node_histogram_cosine_pct':100*dot/den if den else None,'note':'AST histogram records generic structural similarity; it is not substantive copying.'}
for i,t in enumerate(tasks):
    rows=[]
    ta=norm(t['instruction']);raw=norm(t['instruction'],False)
    for j,r in enumerate(refs):
        row={'source':r['file'],'url':r['url'],'kind':r['kind'],'raw':lexical(raw,norm(r['text'],False)),'adjusted':lexical(ta,norm(r['text'])),'adjusted_tfidf_cosine_pct':float(cos[i,j+2])}
        # Localized overlap prevents a long paper from diluting copied sections.
        rt=norm(r['text']);best=(0,0,0)
        for start in range(0,len(rt),150):
            segment=rt[start:start+300];score=lexical(ta,segment)['task_fivegram_containment_pct']
            if score>best[0]:best=(score,start,min(start+300,len(rt)))
        row['most_matched_reference_window']={'task_fivegram_containment_pct':best[0],'normalized_token_start':best[1],'normalized_token_end':best[2]}
        if r['kind']=='reanalysis_code' or r['file'].endswith('.py'):
            a,_=code_tokens(t['solution']);b,_=code_tokens(r['text']);ga,gb=grams(a,12),grams(b,12)
            row['solution_code_twelve_token_containment_pct']=100*len(ga&gb)/max(1,len(ga))
        rows.append(row)
    task_hashes={p.relative_to(t['base']/'task').as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (t['base']/'task').rglob('*') if p.is_file() and (p.suffix in ('.py','.md','.toml','.sh') or p.name=='Dockerfile')}
    data={'task':t['name'],'task_text_code_sha256':task_hashes,'method':'normalized5gram Jaccard/directional containment; corpus-fitted1–2gram TF-IDF cosine;12-token science-code fingerprints; localized300-token windows; separate conceptual rubric required','exclusions':{'standard_terms':sorted(EXCLUDED_TERMS),'other':'canary, exact Harbor closing suffix, accession identifiers, absolute runtime paths; imports/docstrings excluded only from code screen. Raw values retained.'},'corpus_commit':manifest['terminal_bench_commit'],'compared_sources':len(rows),'rows':rows,'cross_task':pair,'scope_limitations':'Finite retrieved corpus only; web challenges are excluded rather than scored as zero. No proprietary plagiarism engine, embedding model, or paid API used. Percentages are defined similarity measures, not percentages of originality. Conceptual/methodological independent assessment is required.'}
    dest=t['base']/'authoring/originality';dest.mkdir(parents=True,exist_ok=True)
    (dest/'lexical_metrics.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(t['name'],'sources',len(rows),'topTFIDF',sorted(((r['adjusted_tfidf_cosine_pct'],r['source']) for r in rows),reverse=True)[:5])
(OUT/'cross_task_metrics.json').write_text(json.dumps(pair,indent=2),encoding='utf-8')
(OUT/'METHOD.md').write_text('''# Reproducible originality screening

Run `originality_metrics.py` with scikit-learn after both task packages exist. Full source hashes and URL snapshots are in `../sources/corpus_manifest.json`. Counts and metadata are excluded from document comparisons: reusing public data is disclosed rather than mislabeled as copied task design.

Report raw and adjusted exact5-word-shingle Jaccard and both directional containment ratios. Adjusted text excludes only the explicit standard-terminology list, accessions, runtime paths, canary and exact required closing paragraph. Scientific objective, method, output schema meaning and evaluator design remain assessable. TF-IDF uses sublinear term frequency, English stopwords and1–2grams across the complete frozen corpus. It measures lexical proximity, not semantic plagiarism. A300-token window search with150-token stride records localized exact overlap, avoiding dilution by long papers. Science code uses12-token shingles after removing imports and standalone docstrings; AST histogram similarity is disclosed as a generic structural diagnostic, not a plagiarism fraction.

Substantive overlap is separately judged with a predeclared six-dimension rubric: objective25%, hypothesis/claim10%, statistical formulation25%, reasoning workflow20%, output design10%, evaluation design10%. Reviewer assigns0=distinct, .25=only high-level purpose shared, .5=several task-specific elements shared, .75=mostly same design,1=equivalent substantive requirement. Sum(weight×rating) is the rubric percentage, not a probability or learned semantic score. Established formulas, biological vocabulary, public dataset metadata and Harbor boilerplate do not increase this conceptual score. Similarity above30% requires examination/redesign of duplicated substantive elements; no wording-only reduction is permitted. A low metric does not establish absolute originality. Reviewer must explicitly explain each overlap and conceptual differences.
''',encoding='utf-8')
