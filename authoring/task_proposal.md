# Task proposal: Certified Kronecker Structure of Singular Matrix Pencils

Identifier: certified-pencil-structure; version 0.1.0. Assigned field: mathematical-sciences/applied-mathematics. This is an original benchmark assembly using established mathematics, not a claim to a new mathematical theorem.

1. Background: exact structural analysis of singular polynomial pencils supports differential-algebraic systems, polynomial nullspaces, and descriptor models. Noferrini and Van Dooren study minimal bases and root polynomials (2023), DOI https://doi.org/10.1016/j.laa.2022.10.025.
2. Real problem: distinguish finite modes, infinite chains, and singular polynomial freedoms when ordinary numerical eigensolvers cannot determine the structure.
3. Formulation: for integer m-by-n A,B, recover the nonzero monic Smith factors of A-zB, the positive zero valuations of the reversed pencil B-zA, and minimal polynomial bases of both kernels over Q[z].
4. Assumptions: dimensions 1-18; entries bounded by 10^15; minimal indices at most 4; infinite sizes at most 6. See environment/spec.md for the authoritative schema.
5. Inputs: batches of at most four exact integer pencils. No attached scientific dataset is required.
6. Required properties: correct normal rank; polynomial divisibility order; all finite factors; infinite valuations; independent polynomial kernel generators of minimum degree. No particular algorithm is prescribed.
7. Output: a transferable Python analyzer and JSON exact rational invariants/certificates.
8. Dependencies: rank controls basis cardinality; convolution kernels determine minimal degrees; reversal separates infinity; the index-sum identity links all reported structures.
9. Edge cases: zero pencils, zero minimal indices, regular pencils, tall/wide pencils, repeated irreducible factors, finite zero versus infinity, large exact row/column scaling.
10. Environment: CPU Linux, Python 3.12, SymPy 1.14.0, mpmath 1.3.0; two CPUs, 4 GiB container RAM; offline verifier. Task agent budget 8 h. Per-invocation limits are stated in spec.md.
11. Accuracy: exact rational equality; no arbitrary numerical tolerance.
12. Verification: hidden pencils constructed from known canonical blocks and transformed by invertible constant matrices; expected invariants come from block construction, not the oracle. A stdlib Fraction checker verifies submitted polynomial identities and leading-coefficient independence exactly.
13. Oracle: polynomial Smith form over Q[z], reversed Smith form, and degree-filtered convolution kernels, with divisibility and index-sum invariant assertions. No known-block metadata is read.
14. Failure opportunities: sample-point rank in place of normal rank; determinant-only logic on singular pencils; diagonalization that erases Jordan sizes; reversing without removing identically zero factors; rational nullspaces with nonminimal degrees; numerical rank loss; left/right convention mistakes.
15. Originality: newly authored specification, schemas, code, adversarial mathematical combinations, certificate grading, and strict-equivalence transformations. Standard canonical blocks and Smith theory are explicitly credited. Search coverage and actual similarity measurements must be reported separately.
16. Difficulty: combines structural spectral algebra and exact minimal-basis construction. It is not certified extremely difficult until real calibration; SymPy reduces some work but does not produce the whole requested deliverable through one routine.
17. Expert estimate: 16 hours; junior estimate: 80 hours. Both are judgment estimates, not measured human completion times.
18. Comparison: satellite phenology requires multistage sensor interpretation; cilia segmentation couples object detection and geometry; fracture couples equilibrium and instability evidence. Here coupling is entirely mathematical and exact. We borrow the engineering pattern of independent artifact verification, not scientific data or algorithms.
19. Research candidates considered: certified parametric QP homotopy (risk of a standard active-set exercise); exact singular pencils (selected for structural depth and independent constructive testing); constrained spectral PDE inversion (higher environmental and tolerance burden).
20. Acceptance constraints: this local project uses the user's 40-60% goal, although the upstream proposal rubric targets 10-20%. No maintainer approval or upstream acceptance is claimed.
21. Proposal rubric: verifiable—promising but runtime evidence pending; well-specified—precise exact contract; solvable—general algorithm supplied, execution pending; difficult—uncertain until trials; scientifically grounded—established research workflow with synthetic instances, independent domain review pending; scope—pure computational mathematics; outcome-verified—arbitrary correct algorithms/bases accepted. Provisional decision: Uncertain.

Planning hierarchy was displayed before source creation. Configuration scaffolding was written before this detailed proposal file; record that ordering deviation rather than claim the requested proposal-first sequence was followed exactly.
