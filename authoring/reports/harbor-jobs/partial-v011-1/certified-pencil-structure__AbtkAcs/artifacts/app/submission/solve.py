"""Plausible but incomplete: exact finite Smith form, no singular/infinite analysis."""
import json,sys
from pathlib import Path
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
z=s.Symbol("z")
out=[]
for c in json.loads(Path(sys.argv[1]).read_text())["cases"]:
    A,B=s.Matrix(c["A"]),s.Matrix(c["B"])
    D=smith_normal_form(A-z*B,domain=s.QQ.poly_ring(z))
    polys=[s.Poly(D[i,i],z,domain=s.QQ).monic() for i in range(min(D.shape)) if D[i,i]!=0]
    out.append({"id":c["id"],"normal_rank":len(polys),
                "smith_factors":[[str(p.nth(j)) for j in range(p.degree()+1)] for p in polys],
                "infinite_sizes":[],"right_indices":[],"left_indices":[],
                "right_basis":[],"left_basis":[]})
Path(sys.argv[2]).write_text(json.dumps({"cases":out}))
