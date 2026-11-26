"""DRAFT: OS-backed fixture draws with private exact replay; no accession seed.

This proposal module is not installed in any task or image. The draw record is
answer-bearing and must stay outside BOTH agent and verifier build contexts.
Frozen numerical fixture files, not a published seed, identify an instance.
"""
from pathlib import Path
import gzip,json,math,secrets
import numpy as np

class SecureRecordedRNG:
    def __init__(self, replay_record=None):
        self._system=secrets.SystemRandom()
        self._events=[]
        self._replay=None
        self._position=0
        if replay_record is not None:
            with gzip.open(replay_record,'rt',encoding='utf-8') as f:obj=json.load(f)
            if obj.get('format')!='private-secure-fixture-draws-v1':raise ValueError('Unknown private record format')
            self._replay=obj['events']

    def _draw(self, operation, parameters, producer):
        if self._replay is None:
            value=producer()
            if isinstance(value,np.ndarray):value=value.tolist()
            self._events.append({'operation':operation,'parameters':parameters,'value':value})
            return value
        if self._position>=len(self._replay):raise ValueError('Private replay exhausted')
        event=self._replay[self._position];self._position+=1
        if event['operation']!=operation or event['parameters']!=parameters:raise ValueError('Private replay does not match generator call sequence')
        return event['value']

    @staticmethod
    def _array_draw(size, scalar):
        if size is None:return scalar()
        shape=(int(size),) if isinstance(size,(int,np.integer)) else tuple(int(x) for x in size)
        return np.array([scalar() for _ in range(math.prod(shape))]).reshape(shape)

    def permutation(self,n):
        def produce():
            values=list(range(int(n)));self._system.shuffle(values);return values
        return np.asarray(self._draw('permutation',{'n':int(n)},produce),dtype=int)

    def uniform(self,low,high,size=None):
        shape=None if size is None else ([int(size)] if isinstance(size,(int,np.integer)) else list(size))
        value=self._draw('uniform',{'low':float(low),'high':float(high),'shape':shape},lambda:self._array_draw(size,lambda:self._system.uniform(low,high)))
        return float(value) if size is None else np.asarray(value,dtype=float)

    def integers(self,high):
        return int(self._draw('integers',{'high':int(high)},lambda:self._system.randrange(int(high))))

    def normal(self,loc,scale,size=None):
        shape=None if size is None else ([int(size)] if isinstance(size,(int,np.integer)) else list(size))
        value=self._draw('normal',{'loc':float(loc),'scale':float(scale),'shape':shape},lambda:self._array_draw(size,lambda:self._system.gauss(loc,scale)))
        return float(value) if size is None else np.asarray(value,dtype=float)

    def save_private_record(self,path,*,forbidden_roots):
        path=Path(path).resolve()
        if not forbidden_roots:raise ValueError('Explicit build-context exclusions required')
        for directory in forbidden_roots:
            if path.is_relative_to(Path(directory).resolve()):raise ValueError('Private draw record inside a build context')
        if path.exists():raise FileExistsError('Refuse to overwrite private randomness record')
        if self._replay is not None and self._position!=len(self._replay):raise ValueError('Unused private replay draws')
        events=self._events if self._replay is None else self._replay
        path.parent.mkdir(parents=True,exist_ok=True)
        # Exact IEEE float values round-trip through Python JSON in the pinned environment.
        with gzip.open(path,'xt',encoding='utf-8') as f:json.dump({'format':'private-secure-fixture-draws-v1','events':events},f,separators=(',',':'),allow_nan=False)

