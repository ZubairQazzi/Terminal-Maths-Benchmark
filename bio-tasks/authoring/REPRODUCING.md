# Coordinator reproduction

Use Python 3.12, Docker with Linux/amd64 containers, and Harbor 0.27.0. The scientific tasks use bundled pinned wheels and inputs; no model provider is needed. The tested host Python and Docker executable paths appear in the preserved native logs. Scripts locate the project relative to themselves; native_validation.py contains the installed Windows executable locations.

From the bio folder, for each task N=1 or2, choose a new suffix such as `fresh1` so original logs are not overwritten:

```text
python authoring/native_validation.py stage --task N --suffix fresh1
python authoring/native_validation.py build --task N --suffix fresh1
python authoring/native_validation.py static --task N --suffix fresh1 --image-tag fresh1
python authoring/final_static_reports.py --task N --suffix fresh1
python authoring/native_validation.py harbor --task N --suffix fresh1 --agents oracle,nop
python authoring/isolation_probes.py --task N --suffix fresh1
python authoring/summarize_native.py --task N --final-prefix fresh1
```

Replace N with the actual task number; the examples are templates, not literal shell variables. Run heavy Docker/Harbor commands sequentially. Baseline names and artifact sources are recorded in each task's authoring reports and in native_validation.py. The final validated historical job prefixes are `v010` for Task1 and `v011` for Task2; native_summary.json distinguishes infrastructure errors and historical superseded Task2 trials. Generic upload controls never call a model API. Regenerate local baseline artifacts using the per-task authoring REPRODUCING.md instructions if they are removed.

Original matrix provenance, all120GSM mappings and immutable originals are under shared-inputs/ and authoring/. QC scripts are bundled under authoring/qc_profile; their exact hashes are in qc_profile_manifest.json. No other task in the parent workspace is required by either runnable package or by current coordinator staging.

The original project final report describes the measured release. Fresh reproduction should use its own summary prefix; final_project_report.py intentionally expects the original version/image labels and complete independent reviewer evidence, rather than silently substituting a new unreviewed run. Authoring scripts for source fetching/originality need network or installed scientific/scikit-learn packages; benchmark trials do not. Gemini and external model-judge QC remain separate approval-gated activities.
