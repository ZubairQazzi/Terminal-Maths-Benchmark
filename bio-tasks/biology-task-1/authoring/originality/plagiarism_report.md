# Biology Task1: separate plagiarism and originality report

**Verdict: PASS within the audited corpus.** Independent conceptual reviewer: `/root/qc_a`. Maximum substantive overlap **25%**, below the30% limit. The resulting **75% rubric nonoverlap** meets the requested70% target under this documented comparison only; it is not proof of absolute originality.

195 retrieved reference documents/code files were screened. Benchmark commit: `48c413db15e310527d11863967db9bec5c3085f0`. Sources include the original GSE273600 publication, the published GDF15 reanalysis and code, Bioconductor analyses, voom/tximport methods, SEQC and all available main/lite benchmark instructions plus biology solution/evaluator source. Supplied local math reference instructions were also included. Full provenance/hashes and failed download alternatives are in `bio/authoring/sources/corpus_manifest.json`; challenge pages were not scored as content.

## Methods and exclusions

Measured exact5-word-shingle Jaccard/directional containment; corpus-fitted unigram/bigram TF-IDF; localized300-token reference windows;12-token code fingerprints; and generic AST histogram diagnostics. The shared method definition is `bio/authoring/originality/METHOD.md`; implementation `originality_metrics.py`. Independent manual conceptual review uses six prespecified dimensions weighted25/10/25/20/10/10, with0/.25/.5/.75/1 ratings and per-dimension rationale. No embeddings, proprietary plagiarism service, Gemini or provider API was used.

Public dataset metadata/identifiers, biological terminology, established formulas and required Harbor boilerplate are excluded from substantive copying judgments. Raw text scores remain visible. Scientific objectives, task-specific statistical formulation, reasoning workflow, outputs and evaluation design are not excluded. Imports/docstrings are removed only in science-code fingerprinting.

## External-reference comparisons

| Reference / compared sections | Substantive rubric similarity |
|---|---:|
| Labbé et al. 2024, Specific activation of the integrated stress response uncovers regulation of central carbon metabolism and lipid droplet biogenesis — Results: Dmr-PERK provides specific and tunable control of ISR activation, lines 86-94; Fig. 1 e-g and Supplementary Fig. 1g, lines 62,94; Transcriptomics data analysis and time course analysis, lines 498-514 | 25% |
| 2026 ISRGDF15 published reanalysis — Development of ISR index, lines 248-338; Validation with targeted/time-resolved ISR activation, lines 500-643; Limitations on specificity, lines 1027-1044; DmrPERK score methods, lines 1193-1199; gdf15-code/ISRGDF15_index/Data Processing Scripts/Figure_1G_Process_Data.R | 8.75% |
| Bioconductor tximport vignette — Estimated counts and effective lengths, lines 230-237; Original counts and offset versus bias-corrected counts, lines 880-932 | 0% |
| Published RNA-seq gene workflow (rnaseqGene) — Starting from count matrices and transcript quantification, lines 201-348; Count/abundance/effective-length assays, lines 811-879 | 0% |
| Law et al. 2014 voom — Abstract and methods: log-count mean-variance weights and limma empirical Bayes | 0% |
| SEQC Consortium 2014 RNA-seq accuracy/reproducibility benchmark — Abstract; Study design and Figure 1: known RNA mixtures and ERCC controls | 0% |
| TBScience diag-chipseq, pinned commit 48c413db15e310527d11863967db9bec5c3085f0 — Externally corrected global/peak-level perturbation effects; Unchanged is not proof of equality paragraph; Three result tables and hidden fixture scoring | 8.75% |
| TBScience genomic-model-ranking and other biology tasks, pinned commit 48c413db15e310527d11863967db9bec5c3085f0 — genomic-model-ranking: context/homology transfer ranking, calibration and sandboxed predictor; ont-tn-qc: alias identity, contamination and batch QC; ambient-rna-correction: native-count recovery; protein-active-learning: assay rounds and variant prediction; cell-lineage-reconstruction, cilia-segmentation, nis3d-hard-volume and betalactam-multimodal-transfer task contracts | 0% |
| TBScience small-area-equivalence — Synthetic four-wave survey and joint predictive draws | 0% |
| Biology Task 2: Recover transcriptomic provenance across expression representations — lines 5-7: synthetic provenance and technical aliquots; lines 20-28: compositional normalization and residualized identity correlations; lines 32-44: sparse mixture fitting and split validation | 0% |

Exact ratings, matched sections and reasoning are preserved in `conceptual_review.json`; each cached reference receives reproducible lexical scores and matched token-window coordinates in `external_similarity_scores.csv` and `lexical_metrics.json`. Reviewers also read additional primary identity-method articles/abstracts; those manual comparisons are outside the195-file lexical set, with the limited reading scope stated in their matched-section evidence. These measures answer different questions and are not interchangeable.

## Over30% diagnostic investigation

The unmodified pinned benchmark checker reports **35.690629% raw TF-IDF** against the other new task (its own upstream flag threshold is80%). Reverse-direction raw score is separately reported because its vocabulary/IDF are fitted on a different reference corpus. The earlier34.113431% run included a duplicate staged reference copy; its log is preserved, the duplicate was removed, and no task wording changed.

With declared standard-term/metadata/boilerplate exclusions, cross-task corpus-fitted TF-IDF is **8.217224%**, raw5-gram Jaccard **0.949504%**, adjusted5-gram Jaccard **0.146199%**. Distinctive scientific workflow was investigated directly rather than inferred from a low lexical score.

Generic AST node-count cosine is **98.914932% for solutions** and **99.302230% for evaluators**. A bag of common Python node types is non-discriminating: unrelated array-processing programs can have the same node proportions. Actual12-token science-code Jaccard is **0.203488% / 0.278087%**. Independent source inspection found different calculations and verification logic. These high diagnostic values were not concealed or relabeled as substantive copying.

No wording was changed to reduce similarity. No task-specific duplicated objective/workflow above30% was found, so no scientific redesign was triggered. The original-publication specificity motivation is explicitly counted where shared.

## Limits

Finite retrieved corpus only; web challenges are excluded rather than scored as zero. No proprietary plagiarism engine, embedding model, or paid API used. Percentages are defined similarity measures, not percentages of originality. Conceptual/methodological independent assessment is required. Conceptual percentage is a disclosed ordinal rubric judgment, not a learned semantic score. Rubric nonoverlap is not an absolute originality guarantee. Unseen/private/unretrieved work is outside the audit.

This audit and independent reviewer verdict are local project evidence, not a certification from an external plagiarism or QC service.
