# Data and source provenance

Task runtime data consist solely of three newly authored small examples in environment/data/examples.json. Hidden inputs are constructed mathematically at grade time by tests/cases.py from standard canonical blocks, independent fixed seeds, and invertible constant transformations. No reference benchmark datasets or answers are used.

The user-supplied geometry.json describes silicon crack geometry; it was inspected as a reference. healthy_reference.npz is a supplied binary reference asset and is not used. The large data_checksums.sha256 lists satellite-imagery paths; the underlying rasters are not supplied by that file and were not downloaded. The existing research-paper PDF and recordings in F:/rl were not used as mathematical input or claimed as reviewed research sources.

No public reference repository snapshot or third-party implementation source was vendored. Public source windows were retrieved through browser tools for analysis and in-memory similarity computation; only hashes, counts, links, and numerical comparisons were saved. The SymPy library is an explicitly installed, pinned dependency, not hidden copied code. Standard canonical-form mathematics is credited in math_research_review.md.

A related public implementation was found during the later originality audit: [tensor-rank-toolkit](https://github.com/Tewf/tensor-rank-toolkit), whose pencil strand includes exact structural analysis. This is substantive conceptual overlap in a classical mathematical goal, not evidence of copied code. Our independently written analyzer and certificate grader were already implemented before that library was inspected. The comparison is included in the scoped report, and global conceptual novelty remains a WARNING.

There is no claim of a new mathematical theorem, exclusive ownership of standard algorithms, external domain-expert authorship, or maintainer approval. No identity/profile credentials have been invented.
