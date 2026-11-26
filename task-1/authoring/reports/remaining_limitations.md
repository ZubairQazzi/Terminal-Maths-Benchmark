# Remaining limitations and approval gate

| Item | Status / required next step |
|---|---|
| Frontier-agent difficulty | NOT MEASURED. Obtain explicit approval, then one fresh graded smoke attempt followed by eight clean independent trials on one model/version/settings. Exclude infrastructure failures. |
| 40–60% target | Cannot assess with 0 valid model trials. Author oracle/negative/reviewer tests do not establish this rate. Do not tune to a desired count or fabricate outcomes. |
| External QC service | NOT RUN. Local scripts and one independent AI reviewer do not constitute external dashboard/panel approval. |
| Originality | Limited to the pinned 97-instruction corpus and one cached unrelated source task for token comparison; no global plagiarism or theorem-novelty guarantee. |
| Reference worst-case runtime | Algebraically complete fallback can be exponential. Measured shipped and extra inputs pass; no universal 180 s runtime theorem. |
| Reporting granularity | 12 batch-native CTRF tests plus separate per-pencil author/reviewer evidence. Numerical rank alone supplies no negative discrimination. |
| Human domain review /32-hour estimate | Human credentials, independent human expert review and expert-time estimate have not been independently validated. |
| Paid APIs / publication | Neither authorized for this phase; no provider calls, commits, pushes or publication performed. |

Confirmed package defects requiring correction:0. Independent reviewer findings W1–W5 are documented limitations, not silently closed defects. No independent post-fix recheck is pending because no active-package correction was requested.
