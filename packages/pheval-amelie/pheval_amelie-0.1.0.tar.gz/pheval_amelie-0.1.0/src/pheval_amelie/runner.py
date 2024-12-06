"""Runner."""

from dataclasses import dataclass
from pathlib import Path

from pheval.runners.runner import PhEvalRunner

from pheval_amelie.post_process.post_process import post_process_results_format
from pheval_amelie.run.run import run


@dataclass
class AmeliePhEvalRunner(PhEvalRunner):
    """Runner class implementation."""

    input_dir: Path
    testdata_dir: Path
    tmp_dir: Path
    output_dir: Path
    config_file: Path
    version: str

    def prepare(self):
        """Prepare."""
        print("preparing")

    def run(self):
        """Run."""
        print("running")
        run(
            testdata_dir=self.testdata_dir,
            tool_input_commands_dir=self.tool_input_commands_dir,
            raw_results_dir=self.raw_results_dir,
        )

    def post_process(self):
        """Post Process."""
        print("post processing")
        post_process_results_format(raw_results_dir=self.raw_results_dir, output_dir=self.output_dir)
