"""Deterministic artifact-upload controls; never calls a model provider."""
from pathlib import Path
import os
from harbor.agents.base import BaseAgent
from harbor.agents.capabilities import AgentCapabilities
class FixtureAgent(BaseAgent):
    capabilities=AgentCapabilities(windows=True)
    @classmethod
    def name(cls):return 'local-biology-fixture'
    def version(self):return '0.1.0'
    async def setup(self,environment):return None
    async def run(self,instruction,environment,context):
        source=Path(os.environ['BIO_FIXTURE_DIR'])
        await environment.upload_dir(source_dir=source,target_dir=os.environ['BIO_FIXTURE_TARGET'])
        (self.logs_dir/'fixture.txt').write_text('Local deterministic control: '+os.environ.get('BIO_FIXTURE_LABEL','unknown')+'\nNo model or provider API invoked.\n')
