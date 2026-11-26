from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,xml.etree.ElementTree as ET
OUT=Path(__file__).resolve().parent/'sources'
items=[
('labbe_bioc','https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC11436933/unicode','publication'),
('gdf15_bioc','https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC13493765/unicode','published_reanalysis'),
('labbe_europe','https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11436933/fullTextXML','publication'),
('gdf15_europe','https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13493765/fullTextXML','published_reanalysis')]
def f(item):
    name,url,kind=item
    try:
        req=Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urlopen(req,timeout=50) as r:data=r.read()
        tree=ET.fromstring(data)
        text='\n'.join(s.strip() for s in tree.itertext() if s.strip())
        if len(text)<20000:raise ValueError('Insufficient full text '+text[:120])
        (OUT/(name+'.xml')).write_bytes(data);(OUT/(name+'.txt')).write_text(text,encoding='utf-8')
        return dict(file=name+'.xml',text_file=name+'.txt',url=url,kind=kind,status='downloaded',sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
    except Exception as e:return dict(file=name+'.xml',url=url,kind=kind,status='unavailable',error=str(e))
rows=list(ThreadPoolExecutor(max_workers=4).map(f,items))
p=OUT/'corpus_manifest.json';manifest=json.loads(p.read_text());manifest['sources']=[r for r in manifest['sources'] if r['file'] not in {i[0]+'.xml' for i in items}]+rows;p.write_text(json.dumps(manifest,indent=2))
print(json.dumps(rows,indent=2))
