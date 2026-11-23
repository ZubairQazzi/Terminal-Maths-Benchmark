"""Author-only Harbor adapter; not a second benchmark task or model attempt."""
from pathlib import Path
from harbor.agents.base import BaseAgent
from harbor.agents.capabilities import AgentCapabilities


class PartialAgent(BaseAgent):
    capabilities = AgentCapabilities(windows=True)

    @staticmethod
    def name():
        return "partial-baseline"

    def version(self):
        return "0.1.0"

    async def setup(self, environment):
        return None

    async def run(self, instruction, environment, context):
        await environment.upload_dir(
            source_dir=Path(__file__).parent/"baselines"/"partial",
            target_dir="/app/submission",
        )
        (self.logs_dir/"partial-baseline.txt").write_text(
            "Uploaded exact finite Smith solver without infinite/minimal structure.\n"
            "This deterministic negative control makes no model calls.\n"
        )

class ExecutableHelperAgent(PartialAgent):
    """Mathematically identical oracle delivered as executable supporting source."""
    @staticmethod
    def name():
        return "executable-helper-oracle"

    def version(self):
        return "0.1.3"

    async def run(self, instruction, environment, context):
        await environment.upload_dir(
            source_dir=Path(__file__).parent/"alternative_helper",
            target_dir="/app/submission",
        )
        result=await environment.exec(
            command="chmod +x /app/submission/helper.py",user="root")
        if result.return_code!=0:
            raise RuntimeError("Could not prepare executable source helper")
        (self.logs_dir/"helper-oracle.txt").write_text(
            "Exact general oracle launched through supporting executable Python source.\n")
