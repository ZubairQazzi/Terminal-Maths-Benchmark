"""Download public primary sources for a finite, reproducible originality audit.
No credentials or model providers are used. Failures remain in the manifest.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import json,hashlib,re,time,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent/'sources'
ROOT.mkdir(parents=True,exist_ok=True)
def get(url):
    url=quote(url,safe=':/?=&%#')
    request=Request(url,headers={'User-Agent':'local-biology-benchmark-audit/1.0','Accept':'application/vnd.github+json' if 'api.github' in url else '*/*'})
    with urlopen(request,timeout=45) as f:return f.read()
def save_one(item):
    name,url,kind=item
    dest=ROOT/name;dest.parent.mkdir(parents=True,exist_ok=True)
    try:
        data=dest.read_bytes() if dest.is_file() and dest.stat().st_size else get(url)
        dest.write_bytes(data)
        return {'file':name,'url':url,'kind':kind,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'status':'downloaded'}
    except Exception as e:return {'file':name,'url':url,'kind':kind,'status':'unavailable','error':str(e)}
items=[]
tree=json.loads(get('https://api.github.com/repos/harbor-framework/terminal-bench-science/git/trees/main?recursive=1'))
(ROOT/'terminal_bench_tree.json').write_text(json.dumps(tree,indent=2))
sha=tree['sha']
for obj in tree['tree']:
    p=obj['path']
    if obj['type']!='blob':continue
    if (p.startswith(('tasks/','lite/')) and p.endswith('/instruction.md')) or (p.startswith(('tasks/life-sciences/biology/','lite/life-sciences/biology/')) and ('/solution/' in p or '/tests/' in p) and p.endswith(('.py','.R','.r','.sh','.md'))):
        items.append(('terminal-bench/'+p,f'https://raw.githubusercontent.com/harbor-framework/terminal-bench-science/{sha}/{p}','benchmark'))
items.extend([
 ('labbe_2024_pmc.html','https://pmc.ncbi.nlm.nih.gov/articles/PMC11436933/','publication'),
 ('gdf15_2026_pmc.html','https://pmc.ncbi.nlm.nih.gov/articles/PMC13493765/','published_reanalysis'),
 ('soneson_2015.html','https://pmc.ncbi.nlm.nih.gov/articles/PMC4712774/','rna_seq_method'),
 ('tximport.html','https://bioconductor.org/packages/release/bioc/vignettes/tximport/inst/doc/tximport.html','rna_seq_workflow'),
 ('deseq2_workflow.html','https://bioconductor.org/packages/release/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html','published_rna_seq_analysis'),
 ('voom_2014_pmc.html','https://pmc.ncbi.nlm.nih.gov/articles/PMC4053721/','rna_seq_method'),
 ('seqc_benchmark_pmc.html','https://pmc.ncbi.nlm.nih.gov/articles/PMC4321899/','public_bioinformatics_benchmark')])
items.extend((name+'.xml','https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmc+'/fullTextXML',kind) for name,pmc,kind in [('labbe_full','PMC11436933','publication'),('gdf15_full','PMC13493765','published_reanalysis'),('voom_full','PMC4053721','rna_seq_method')])
try:
    reuse_tree=json.loads(get('https://api.github.com/repos/mitopsychobio/2025_ISR_GDF15_JS_v2/git/trees/main?recursive=1'))
    (ROOT/'gdf15_code_tree.json').write_text(json.dumps(reuse_tree,indent=2))
    for obj in reuse_tree['tree']:
        p=obj['path']
        if obj['type']=='blob' and p.endswith(('.R','.r','.Rmd','.md')):
            items.append(('gdf15-code/'+p,f"https://raw.githubusercontent.com/mitopsychobio/2025_ISR_GDF15_JS_v2/{reuse_tree['sha']}/{p}",'reanalysis_code'))
except Exception as e:items.append(('unavailable-gdf15-code','https://github.com/mitopsychobio/2025_ISR_GDF15_JS_v2','reanalysis_code'))
rows=list(ThreadPoolExecutor(max_workers=6).map(save_one,items))
class Text(HTMLParser):
    def __init__(self):super().__init__();self.s=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ('script','style','nav'):self.skip+=1
    def handle_endtag(self,t):
        if t in ('script','style','nav'):self.skip=max(self.skip-1,0)
    def handle_data(self,s):
        if not self.skip and s.strip():self.s.append(s.strip())
for row in rows:
    if row['status']=='downloaded' and row['file'].endswith('.html'):
        p=ROOT/row['file'];parser=Text();parser.feed(p.read_text(encoding='utf-8',errors='replace'))
        plain=p.with_suffix('.txt');plain.write_text('\n'.join(parser.s),encoding='utf-8');row['text_file']=plain.relative_to(ROOT).as_posix()
        if len(parser.s)<40 or 'Client Challenge' in '\n'.join(parser.s):row['status']='challenge_page_not_content'
    if row['status']=='downloaded' and row['file'].endswith('.xml'):
        p=ROOT/row['file'];root=ET.fromstring(p.read_bytes());plain=p.with_suffix('.txt')
        plain.write_text('\n'.join(t.strip() for t in root.itertext() if t.strip()),encoding='utf-8');row['text_file']=plain.relative_to(ROOT).as_posix()
manifest={'retrieved_date':'2026-11-25','terminal_bench_commit':sha,'tree_truncated':tree.get('truncated'),'sources':rows}
(ROOT/'corpus_manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'commit':sha,'sources':len(rows),'downloaded':sum(r['status']=='downloaded' for r in rows),'failures':[r for r in rows if r['status']!='downloaded']},indent=2))
