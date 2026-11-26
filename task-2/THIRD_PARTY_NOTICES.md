# Third-party notices

The offline dependency wheels in `environment/wheels/` and `tests/wheels/` are redistributed unchanged. Their original license files remain embedded where supplied. Complete notices are also reproduced in `THIRD_PARTY_LICENSES/`.

| Dependency | Bundled version | License / notices |
|---|---|---|
| mpmath | 1.3.0 | BSD-3-Clause |
| SymPy | 1.14.0 | BSD-3-Clause and additional bundled notices in its complete LICENSE; latex2sympy MIT notice in LICENSE.txt |
| colorama | 0.4.6 | BSD-3-Clause |
| iniconfig | 2.3.1 | MIT |
| packaging | 26.4 | Apache-2.0 OR BSD-2-Clause; both notices supplied |
| pluggy | 1.7.0 | MIT |
| Pygments | 2.21.0 | BSD-2-Clause |
| pytest | 8.4.1 | MIT |
| pytest-json-ctrf | 0.3.5 | MIT; omitted standalone notice supplied separately as described below |

The pytest-json-ctrf 0.3.5 wheel declares the MIT license in its distribution metadata and the release's [PyPI page](https://pypi.org/project/pytest-json-ctrf/0.3.5/), but omits a standalone license file. Its official maintained successor repository supplies the complete MIT notice, copyright 2024 Oleksii Ostapov. That notice is included unmodified from [license commit c6c8072eb15b48a62e27167ba3a549e8b5d927e4](https://github.com/qamania/pytest-common-test-report-json/blob/c6c8072eb15b48a62e27167ba3a549e8b5d927e4/LICENSE). No dependency code, wheel hash or evaluator logic was changed to add these notices.

The Dockerfiles reference the digest-pinned official `python:3.12-slim` image. Container image layers, CPython binaries and operating-system packages are not included in the task ZIP; Docker obtains that image from its upstream registry at build time. The image's components retain their respective licenses. Python image build recipes are maintained in [docker-library/python](https://github.com/docker-library/python); the [official image documentation](https://github.com/docker-library/docs/tree/master/python#license) describes licensing of image contents. This task's own license does not replace any dependency or base-image license.

Harbor and the selected agent/provider are installed separately by the user and are not bundled here. Provider use is subject to the user's own account and applicable terms.

Only the current runtime task, its generated mathematical data and necessary publication documentation are included. Third-party research comparison snapshots, unrelated public task corpora, local environments, credentials and historical trajectories are preserved in the author's local project and are not part of this public distribution.
