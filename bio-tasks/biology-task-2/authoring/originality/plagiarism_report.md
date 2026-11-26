# Biology Task2: separate plagiarism and originality report

**Verdict: PASS within the audited corpus.** Independent conceptual reviewer: `/root/qc_b`. Maximum substantive overlap **25%**, below the30% limit. The resulting **75% rubric nonoverlap** meets the requested70% target under this documented comparison only; it is not proof of absolute originality.

195 retrieved reference documents/code files were screened. Benchmark commit: `48c413db15e310527d11863967db9bec5c3085f0`. Sources include the original GSE273600 publication, the published GDF15 reanalysis and code, Bioconductor analyses, voom/tximport methods, SEQC and all available main/lite benchmark instructions plus biology solution/evaluator source. Supplied local math reference instructions were also included. Full provenance/hashes and failed download alternatives are in `bio/authoring/sources/corpus_manifest.json`; challenge pages were not scored as content.

## Methods and exclusions

Measured exact5-word-shingle Jaccard/directional containment; corpus-fitted unigram/bigram TF-IDF; localized300-token reference windows;12-token code fingerprints; and generic AST histogram diagnostics. The shared method definition is `bio/authoring/originality/METHOD.md`; implementation `originality_metrics.py`. Independent manual conceptual review uses six prespecified dimensions weighted25/10/25/20/10/10, with0/.25/.5/.75/1 ratings and per-dimension rationale. No embeddings, proprietary plagiarism service, Gemini or provider API was used.

Public dataset metadata/identifiers, biological terminology, established formulas and required Harbor boilerplate are excluded from substantive copying judgments. Raw text scores remain visible. Scientific objectives, task-specific statistical formulation, reasoning workflow, outputs and evaluation design are not excluded. Imports/docstrings are removed only in science-code fingerprinting.

## External-reference comparisons

| Reference / compared sections | Substantive rubric similarity |
|---|---:|
| Labbé et al. 2024, DOI 10.1038/s41467-024-52538-5 — authoring/sources/labbe_bioc.txt:78-154 (Results, Figures 1–3); biology-task-2/task/instruction.md:5-7,24-44; Same deposited matrices and treatment names excluded as required. | 0% |
| Smith et al. 2026 GDF15 reanalysis, DOI 10.1038/s42003-026-10312-x — authoring/sources/gdf15_europe.txt:292-365,580-650; authoring/sources/gdf15-code/ISRGDF15_index/Data Processing Scripts/Figure_1G_Process_Data.R:1-120; authoring/sources/gdf15-code/ISRGDF15_index/Main Figure Scripts/Figure_2G.R:1-60; Task 2 instruction:24-44; solution/solve.py:28-73 | 0% |
| Bioconductor tximport workflow and Soneson et al. transcript-to-gene method — authoring/sources/tximport.txt:218-310 (counts, abundance, length, countsFromAbundance); authoring/sources/soneson_2015.txt (gene-level inference and transcript usage); Task 2 instruction:13-28,32-44; https://bioconductor.org/packages/release/bioc/vignettes/tximport/inst/doc/tximport.html | 11.25% |
| Bioconductor RNA-seq / DESeq2 published workflow — authoring/sources/deseq2_workflow.txt:201-290 (unnormalized counts and transcript quantification), differential-expression pipeline sections; Task 2 instruction:24-44; https://bioconductor.org/packages/release/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html | 0% |
| Law et al. voom method, DOI 10.1186/gb-2014-15-2-r29 — authoring/sources/voom_full.txt:80,180-225 (method and Results); Task 2 instruction:26,32-44; no count likelihood or MTC required | 0% |
| SEQC/MAQC-III RNA-seq benchmark, PMC4321899 — authoring/sources/seqc_benchmark_pmc.txt:92-155 (design, Fig.1 A/B, C=3:1, D=1:3; ratio recovery); Task 2 instruction:14-15,24-44; https://pmc.ncbi.nlm.nih.gov/articles/PMC4321899/ | 25% |
| TBScience ont-tn-qc — authoring/sources/terminal-bench/tasks/life-sciences/biology/ont-tn-qc/instruction.md (problem, review_domain, aliases, confidence); same task solution/qc_oracle/{snp_pileup.py,manifest_resolution.py,carryover.py,purity.py,copy_number.py}; Task 2 instruction:24-44; solution/solve.py:28-73 | 25% |
| TBScience ambient-rna-correction — authoring/sources/terminal-bench/tasks/life-sciences/biology/ambient-rna-correction/instruction.md (inputs, output, verifier definitions); same task solution/solve.py:86-154,197-236; Task 2 instruction:15,32-44,54-58 | 18.75% |
| TBScience diag-chipseq — authoring/sources/terminal-bench/tasks/life-sciences/biology/diag-chipseq/instruction.md (reference status, global and peak outputs); same task solution/fit_peaks.R:25-110; Task 2 instruction:24-44 | 16.25% |
| TBScience clinical-metadata-recovery — authoring/sources/terminal-bench/tasks/life-sciences/medicine/clinical-metadata-recovery/instruction.md:3-13; Task 2 instruction:14-15,24-44 | 18.75% |
| TBScience xrd-multiphase-qpa — authoring/sources/terminal-bench/tasks/physical-sciences/materials-science/xrd-multiphase-qpa/instruction.md (candidate library, unknown, amorphous, scoring); Task 2 instruction:32-44 | 18.75% |
| TBScience hysteretic-aquifer-control (largest adjusted TF-IDF corpus match) — authoring/sources/terminal-bench/tasks/earth-sciences/environmental-sciences/hysteretic-aquifer-control/instruction.md (model, sensor calibration, closure, intervention); Task 2 instruction:24-44 | 13.75% |
| Biology Task 1 (same project) — biology-task-1/task/instruction.md:3-37; solution/solve.py:10-94; tests/test_outputs.py:16-181; biology-task-2/task/instruction.md:24-44,50-82; solution/solve.py:28-76; tests/checks.py:75-149; Shared GSE273600 metadata, fractional-count/floor facts and Harbor boilerplate excluded. | 2.5% |
| Kist et al. RNASeq_similarity_matrix, DOI 10.1093/bioinformatics/btz821 — https://academic.oup.com/bioinformatics/article/36/6/1940/5643758 (Abstract, Features, Results; primary article directly read in web tool); Task 2 instruction:24-44 | 25% |
| Huang et al. IDCheck, DOI 10.1093/bioinformatics/btt155 — https://pubmed.ncbi.nlm.nih.gov/23559639/ (primary abstract directly read; full implementation not audited); Task 2 instruction:7,24-44 | 25% |
| Supplied workspace math tasks: certified-qp-atlas, certified-padic-census, certified-pencil-structure — F:/rl/task-2/instruction.md; F:/rl/task-3/instruction.md; F:/rl/math-benchmark/tasks/mathematical-sciences/applied-mathematics/certified-pencil-structure/instruction.md | 0% |

Exact ratings, matched sections and reasoning are preserved in `conceptual_review.json`; each cached reference receives reproducible lexical scores and matched token-window coordinates in `external_similarity_scores.csv` and `lexical_metrics.json`. Reviewers also read additional primary identity-method articles/abstracts; those manual comparisons are outside the195-file lexical set, with the limited reading scope stated in their matched-section evidence. These measures answer different questions and are not interchangeable.

## Over30% diagnostic investigation

The unmodified pinned benchmark checker reports **37.233581% raw TF-IDF** against the other new task (its own upstream flag threshold is80%). Reverse-direction raw score is separately reported because its vocabulary/IDF are fitted on a different reference corpus. The earlier34.113431% run included a duplicate staged reference copy; its log is preserved, the duplicate was removed, and no task wording changed.

With declared standard-term/metadata/boilerplate exclusions, cross-task corpus-fitted TF-IDF is **8.217224%**, raw5-gram Jaccard **0.949504%**, adjusted5-gram Jaccard **0.146199%**. Distinctive scientific workflow was investigated directly rather than inferred from a low lexical score.

Generic AST node-count cosine is **98.914932% for solutions** and **99.302230% for evaluators**. A bag of common Python node types is non-discriminating: unrelated array-processing programs can have the same node proportions. Actual12-token science-code Jaccard is **0.203488% / 0.278087%**. Independent source inspection found different calculations and verification logic. These high diagnostic values were not concealed or relabeled as substantive copying.

No wording was changed to reduce similarity. No task-specific duplicated objective/workflow above30% was found, so no scientific redesign was triggered. The original-publication specificity motivation is explicitly counted where shared.

## Limits

Finite retrieved corpus only; web challenges are excluded rather than scored as zero. No proprietary plagiarism engine, embedding model, or paid API used. Percentages are defined similarity measures, not percentages of originality. Conceptual/methodological independent assessment is required. Conceptual percentage is a disclosed ordinal rubric judgment, not a learned semantic score. Rubric nonoverlap is not an absolute originality guarantee. Unseen/private/unretrieved work is outside the audit.

This audit and independent reviewer verdict are local project evidence, not a certification from an external plagiarism or QC service.
