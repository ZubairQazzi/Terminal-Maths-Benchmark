# Dataset permissions and acquisition/packaging strategy

Reviewed 26 November 2026. **Unrestricted redistribution is not established.** This is a bounded source/packaging investigation, not a legal clearance. No rights inquiry was sent and no material was published.

## Primary-source findings

The study's data-availability statement identifies GSE273600 among its RNA-seq deposits. Its article license is CC BY-NC-ND 4.0; that license must not automatically be assigned to separately deposited numerical matrices. No article figures or adapted article text are needed in the benchmark. [Publication and rights](https://www.nature.com/articles/s41467-024-52538-5).

NCBI's molecular-data policy encourages reuse and places no repository restriction on distribution, while stating that submitter rights are not transferred to NCBI and that NCBI cannot grant unrestricted third-party permission. Public deposition therefore supports access but is not proof of an unrestricted matrix-specific grant. [NCBI policy](https://www.ncbi.nlm.nih.gov/home/about/policies/). The GEO-specific disclaimer was also found in official search results, but opening it and the accession page hit a browser challenge; the full general policy was readable. The FTP listing failed in the web tool. These access limitations are recorded, not silently treated as licensing evidence.

The complete cached official family SOFT was scanned for license/licence/copyright/permission/redistribution/commercial terms; none appeared. Its recorded SHA-256 matches the previous official acquisition. Absence of a license keyword is not a license. No explicit matrix-specific unrestricted grant or contrary dataset-specific restriction was established in the reviewed material. `geo_rights_keyword_scan.json` preserves the method and exact supplementary-file links.

## Recommended distribution boundary

Prepare a **source-only** release: original benchmark code/instructions, minimal attribution, source URLs/accession, SHA-256 and file sizes, pinned dependency requirements and a local preparation recipe. Exclude raw count/TPM data, gene annotation tables derived from them, anonymous/scaled atlas and query matrices, truth/replay records, article PDFs/figures/abstracts, model logs containing expression values, prebuilt images and vendored wheels from any public archive until their respective rights are cleared. Existing private working copies can remain on F; do not publish them as part of this proposal.

At setup time, the benchmark operator obtains the two matrices directly from the depositor's official GEO HTTPS endpoint, or supplies already lawfully acquired local files. Verify hashes and sizes before parsing; never silently accept changed files. Keep originals read-only on F and record access date/source attribution. A host-side, separately permissioned builder produces local runtime fixtures before image construction. Agent and verifier runs then need no downloader and can use local data only. Downloading locally avoids redistributing these matrices in our source archive; it does not itself establish the operator's rights to every intended use, derivative or external API transfer.

The acquisition manifest contains dataset-specific hashes already verified against the user originals. Proposed source URLs:

- [Estimated counts](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE273nnn/GSE273600/suppl/GSE273600_Control_Conditions_Raw_Counts.txt.gz)
- [TPMs](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE273nnn/GSE273600/suppl/GSE273600_Control_Conditions_TPMs.txt.gz)
- [Family SOFT](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE273nnn/GSE273600/soft/GSE273600_family.soft.gz)

These endpoints are grounded in cached official metadata; a new full download was unnecessary and was not performed. A future bootstrap should use bounded retries, HTTPS, an identified client and NCBI retrieval guidance, and stop on a hash mismatch or terms change. Do not spoof an access-control challenge.

For software, install pinned, hash-verified dependencies from their original distributors during host setup; carry applicable notices if a later release bundles them. A previous pytest-json-ctrf notice gap means vendored-wheel/image redistribution is not fully cleared. A source-only recipe reduces bundled third-party material but does not replace license compliance.

## Clearance path for a self-contained redistributed benchmark

Obtain an explicit grant from the appropriate data rights holders covering these exact two matrix files, public redistribution, transformed/scaled mixtures and gene metadata, public benchmark use, commercial use if intended, and third-party model/API processing. Record attribution and conditions. A permissive data license such as CC BY or CC0, if validly granted, would simplify packaging; the project must not assign one itself. The inquiry should distinguish numerical data from the licensed article and identify any third-party annotations.

Draft inquiry, **unsent**: “We are developing two computational benchmarks from GSE273600's Control Conditions raw-count and TPM matrices. May we redistribute the original numerical tables and deterministic/synthetic derivatives with source attribution for public and commercial benchmark use, including evaluation through external model APIs? Please specify the applicable data license, attribution and any third-party limits. We will not reproduce article figures or adapted article text under this permission.”

No email or other external message is authorized or sent by this investigation. If permissive redistribution cannot be established, retain source-only/local-acquisition operation subject to the operator's applicable rights, or propose a separately versioned dataset with an explicit suitable license. Replacing the biological dataset would require fresh scientific validation and user approval; it must not be done merely to make models fail.

## Calibration-specific processing

The existing Gemini model has a public free tier. Google's pricing documentation states that free-tier content may be used to improve products; account-specific tier/terms must be checked. Model interaction can send selected terminal excerpts and expression values to the provider even when full matrices stay in a local container. This approval proposal does not call that purely local processing or assume a zero bill. No bulk data upload, publication, billing upgrade, paid-only fallback or broad public release is proposed. [Gemini pricing and data use](https://aistudio.google.com/docs/pricing#gemini-3.5-flash-lite).
