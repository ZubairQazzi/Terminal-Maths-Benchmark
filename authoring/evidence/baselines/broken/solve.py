import json,sys
from pathlib import Path
data=json.loads(Path(sys.argv[1]).read_text())
Path(sys.argv[2]).write_text(json.dumps({"cases":[{"id":c["id"],"normal_rank":0,
"smith_factors":[],"infinite_sizes":[],"right_indices":[],"left_indices":[],
"right_basis":[],"left_basis":[]} for c in data["cases"]]}))
