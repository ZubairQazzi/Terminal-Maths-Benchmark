# Independent conceptual originality review

Reviewer `/root/qc_b`, distinct from the creator. This is a manual local review, not external approval. The prescribed ordinal weights are objective 25, hypothesis 10, statistical formulation 25, workflow 20, output 10, evaluation 10. Ratings are 0/.25/.5/.75/1; each dimension's rationale and matched source sections are in `conceptual_review.json`.

The largest substantive overlap is **25%**, shared with SEQC, ONT QC and established RNA sample-identity work at a broad integrity-audit level. Task 2 does not assert that sample identity or linear mixtures are new inventions. It combines a distinct count–TPM library-bijection problem, expression-scale sparse source identification and feature-held-out rejection. The reviewed scope supports PASS against the requested 30% substantive threshold; it does not prove absolute originality.

| Comparison | Weighted substantive overlap |
|---|---:|
| Labbé et al. 2024, DOI 10.1038/s41467-024-52538-5 | 0% |
| Smith et al. 2026 GDF15 reanalysis, DOI 10.1038/s42003-026-10312-x | 0% |
| Bioconductor tximport workflow and Soneson et al. transcript-to-gene method | 11.25% |
| Bioconductor RNA-seq / DESeq2 published workflow | 0% |
| Law et al. voom method, DOI 10.1186/gb-2014-15-2-r29 | 0% |
| SEQC/MAQC-III RNA-seq benchmark, PMC4321899 | 25% |
| TBScience ont-tn-qc | 25% |
| TBScience ambient-rna-correction | 18.75% |
| TBScience diag-chipseq | 16.25% |
| TBScience clinical-metadata-recovery | 18.75% |
| TBScience xrd-multiphase-qpa | 18.75% |
| TBScience hysteretic-aquifer-control (largest adjusted TF-IDF corpus match) | 13.75% |
| Biology Task 1 (same project) | 2.5% |
| Kist et al. RNASeq_similarity_matrix, DOI 10.1093/bioinformatics/btz821 | 25% |
| Huang et al. IDCheck, DOI 10.1093/bioinformatics/btt155 | 25% |
| Supplied workspace math tasks: certified-qp-atlas, certified-padic-census, certified-pencil-structure | 0% |

The raw pinned TF-IDF screen is **37.233581% Task 2→Task 1** and **35.690629% Task 1→Task 2**, above the user's 30% investigation threshold. The initially reported 34.113431% is preserved in the coordinator's initial-duplicate-reference report. Correcting a duplicate staged reference changed the reference corpus, not task text. `reports/upstream_similarity_v011.json` records the final Task 2 score. The upstream static threshold is 80%; that threshold does not replace the separate substantive investigation.

Direct comparison of Task 1's data/estimand/audit sections with Task 2 instruction lines 7, 13–18 and 60–82 shows shared deposited-study facts, representation caveats, data audit and interpretation flags. Their main objectives and implementations differ: Task 1 uses four-group Welch contrasts, TOST, a joint-null BY family and early-control sensitivity regions; Task 2 uses sample fingerprints, assignment, bounded convex source fits and disjoint-gene residuals. Their primary tables use different units of analysis and scientific outputs. Shared data facts, established formulas, standard terminology and Harbor boilerplate were excluded by the stipulated conceptual rubric. No surface wording was changed to reduce a score.

The custom adjusted full-corpus TF-IDF is 8.217224%; adjusted 5-gram Jaccard is 0.146199%. Science-code 12-token Jaccard is 0.203488% for solution and 0.283072% for evaluator. Conversely, generic AST node histograms are 98.914932% and 99.193649%. These raw structural values are retained: histogram agreement of Python node categories is not evidence of a shared scientific algorithm. Neither low lexical metrics nor a low conceptual rating alone proves originality.

Primary content directly inspected includes the Labbé BioC fulltext Results/Methods, the 2026 GDF15 fulltext and relevant source code, tximport/DESeq2/voom documentation, and SEQC's mixture design. The corpus is frozen at commit `48c413db15e310527d11863967db9bec5c3085f0`: 96 main plus one lite instruction and 53 biology code files were programmatically screened; closest instructions and relevant scientific code were directly read. No unavailable/challenge page was treated as article content. The supplied mathematical tasks were also checked and show only standard packaging/certificate vocabulary.

Two additional primary sources confirm that sample-integrity analysis is established prior art: [RNASeq_similarity_matrix](https://academic.oup.com/bioinformatics/article/36/6/1940/5643758) uses RNA-derived genomic SNP similarity; [IDCheck](https://pubmed.ncbi.nlm.nih.gov/23559639/) uses genotype/read likelihood concordance. Their scientific formulations differ from this expression-representation task. IDCheck was reviewed at abstract level only.

Limitations: finite corpus; unequal manual depth across unrelated code; ordinal judgments; no comprehensive proof of absence from literature. No external LLM QC, provider calibration or Gemini API was run.

