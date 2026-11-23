# Mathematical research review

Selected area: exact structural linear algebra for singular rectangular pencils. This is computational mathematics; there is no reinforcement learning or model training in the task itself.

Candidate comparison:

| Candidate | Depth and verification | Decision |
|---|---|---|
| Parametric convex quadratic-program homotopy | Exact KKT certificates are attractive; a small active-set problem risks becoming a course exercise | Not selected |
| Complete pencil structure with polynomial certificates | Finite and infinite spectra, module minimality, exact ranks, and left/right duality interact; canonical constructions support independent grading | Selected |
| Constrained inverse spectral PDE problem | Strong research depth, but more difficult discretization-error and identifiability validation | Not selected |

The selection is a design judgment, not empirical evidence that the problem is sufficiently difficult.

Primary research consulted:
- [Noferrini and Van Dooren, On computing root polynomials and minimal bases of matrix pencils, Linear Algebra and its Applications 658 (2023)](https://doi.org/10.1016/j.laa.2022.10.025).
- [Hochstenbach, Mehl, and Plestenjak, singular generalized eigenvalue problems via rank-completing perturbations](https://hochsten.win.tue.nl/pdf/simax-singgep.pdf).
- [Christou, Mitrouli, and Triantafyllou, rank-updating computation of pencil minimal indices](https://doi.org/10.1016/j.apnum.2024.01.015).
- [SymPy 1.14 normal-form API](https://docs.sympy.org/latest/modules/matrices/normalforms.html).

The papers establish that minimal bases and singular spectral structures are actual research concerns, and that block Toeplitz nullity sequences reveal structural indices. We do not reproduce their algorithms or claim novel canonical-form theory. The oracle independently implements a small exact degree-filtration construction and uses the documented Smith-form library.

## Independent mathematical justification

Let r be the rank over Q(z). Smith reduction over the PID Q[z] gives r nonzero invariant factors with d_i dividing d_(i+1). Normalizing each to monic fixes unit ambiguity. Applying the same definition to the grade-one reversal B-zA and retaining only positive zero valuations gives the infinite block sizes. Identically zero Smith entries describe singular structure and must not be counted as infinite blocks.

Write v(z)=v_0+...+v_k z^k. Comparing coefficients in (A-zB)v=0 gives A v_0=0, A v_j-B v_(j-1)=0, and B v_k=0. The oracle assembles exactly this finite-dimensional rational convolution system. For minimal degrees e_i, its kernel dimension is sum_i max(0,k-e_i+1). Consequently nullity increments count generators of degree at most k. At each degree we quotient out shifts of earlier generators and select independent new directions. This recovers degree-minimal generators without assuming canonical coordinates.

For a proposed basis, the evaluator recomputes every coefficient identity with Fraction arithmetic. Independent highest-degree coefficient columns give polynomial independence. Once cardinalities and degrees match the independently constructed minimal indices, these certificates attain the minimum possible total degree, so an arbitrary correct basis is accepted. Rational rescaling has already been checked locally.

The pencil index-sum identity is r = sum deg(d_i) + sum infinite_sizes + sum right_indices + sum left_indices. The oracle asserts it; the generator derives it separately from block dimensions. The zero pencil is covered by independent degree-zero coordinate directions.

Canonical generation uses: companion(q)-zI for a monic primary power q; I-zN for a nilpotent Jordan block N; and [-zI, shifted I] rectangular blocks and their transposes. Invertible constant row and column operations preserve all structural invariants. The evaluator builds expected factors by combining primary powers in divisibility order, not by calling the oracle's Smith routine. Transposition swaps minimal-index sides; translation A -> A+cB substitutes z-c in the finite factors.

All arithmetic is rational, so the numerical tolerance is exactly zero. Large row/column scales test structural reasoning without introducing uncertain numerical reference values. Instance sizes are bounded to make coefficient growth manageable. The current oracle completed all 32 hidden instances within seconds locally; container limits and model difficulty remain to be measured.
