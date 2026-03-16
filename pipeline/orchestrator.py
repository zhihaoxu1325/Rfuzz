from pathlib import Path

from dsl_constructor.constructor import DSLConstructor
from fuzzer.fuzzer_engine import FuzzerEngine
from interface_profiler.profiler import InterfaceProfiler
from llm_refiner.coverage_analyzer import pick_candidates
from llm_refiner.refiner import LLMRefiner
from utils.file_utils import ensure_dir
from utils.metrics import PipelineMetrics


class Orchestrator:
    def __init__(self) -> None:
        self.profiler = InterfaceProfiler()
        self.constructor = DSLConstructor()
        self.fuzzer = FuzzerEngine()
        self.refiner = LLMRefiner()

    def run(self, syscall_tbl: str | Path, kconfig: str | Path, refined_out_dir: str | Path) -> PipelineMetrics:
        metrics = PipelineMetrics()
        profile = self.profiler.run(syscall_tbl, kconfig)
        metrics.interfaces_profiled = len(profile.whitelist)

        seeds = self.constructor.run(profile.whitelist)
        metrics.seeds_generated = len(seeds)

        coverage = self.fuzzer.fuzz(seeds)
        candidates = pick_candidates(seeds, coverage)
        metrics.candidates_refined = len(candidates)

        outdir = ensure_dir(refined_out_dir)
        for candidate in candidates:
            result = self.refiner.refine(candidate)
            if result.accepted:
                metrics.accepted_refinements += 1
                Path(outdir, f"{result.interface}.syz").write_text(result.refined_dsl + "\n", encoding="utf-8")
        return metrics
