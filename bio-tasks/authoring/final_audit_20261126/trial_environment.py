"""F-drive caches for new authoring/model runs; existing installations untouched."""
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[2]
CACHE=ROOT/'runtime-cache'
def configure():
    values={
      'TEMP':str(CACHE/'tmp'),'TMP':str(CACHE/'tmp'),'TMPDIR':str(CACHE/'tmp'),
      'XDG_CACHE_HOME':str(CACHE/'xdg'),'UV_CACHE_DIR':str(CACHE/'uv'),
      'PIP_CACHE_DIR':str(CACHE/'pip'),'HF_HOME':str(CACHE/'huggingface'),
      'HUGGINGFACE_HUB_CACHE':str(CACHE/'huggingface/hub'),
      'PYTHONPYCACHEPREFIX':str(CACHE/'pycache'),'MPLCONFIGDIR':str(CACHE/'matplotlib'),
      'NUMBA_CACHE_DIR':str(CACHE/'numba'),'LITELLM_CACHE_DIR':str(CACHE/'litellm'),
      'TIKTOKEN_CACHE_DIR':str(CACHE/'tiktoken'),
      'LITELLM_LOCAL_MODEL_COST_MAP':'True','PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8',
      'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','HF_HUB_DISABLE_TELEMETRY':'1',
      'DO_NOT_TRACK':'1'
    }
    for key,value in values.items():
        if key not in ('PYTHONUTF8','PYTHONIOENCODING','LITELLM_LOCAL_MODEL_COST_MAP','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','HF_HUB_DISABLE_TELEMETRY','DO_NOT_TRACK'):Path(value).mkdir(parents=True,exist_ok=True)
        os.environ[key]=value
    import tempfile
    tempfile.tempdir=str(CACHE/'tmp')
    return values
def redirect_harbor_cache():
    # Harbor0.27 uses Path.home and platformdirs without an env override for all caches.
    # Patch only cache locations in this launcher process, before importing CLI modules.
    import harbor.constants as c
    c.CACHE_DIR=CACHE/'harbor';c.TASK_CACHE_DIR=c.CACHE_DIR/'tasks';c.PACKAGE_CACHE_DIR=c.TASK_CACHE_DIR/'packages';c.DATASET_CACHE_DIR=c.CACHE_DIR/'datasets';c.NOTIFICATIONS_PATH=c.CACHE_DIR/'notifications.json'
    from harbor.environments.docker import utils
    def build_cache():
        path=CACHE/'harbor/docker_build';path.mkdir(parents=True,exist_ok=True);return path
    utils._docker_build_cache_dir=build_cache
    for path in (c.CACHE_DIR,c.TASK_CACHE_DIR,c.PACKAGE_CACHE_DIR,c.DATASET_CACHE_DIR):path.mkdir(parents=True,exist_ok=True)
