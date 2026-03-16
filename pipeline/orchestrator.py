from pathlib import Path

from dsl_constructor.constructor import DSLConstructor
from fuzzer.corpus_manager import save_seed
from fuzzer.fuzzer_engine import FuzzerEngine
from interface_profiler.profiler import InterfaceProfiler
from llm_refiner.coverage_analyzer import pick_candidates
from llm_refiner.llm_client import LLMClient
from llm_refiner.refiner import LLMRefiner
from utils.file_utils import ensure_dir
from utils.metrics import PipelineMetrics


class Orchestrator:
    def __init__(self, min_coverage_gain: int = 1, llm_client: LLMClient | None = None) -> None:
        self.profiler = InterfaceProfiler()
        self.constructor = DSLConstructor()
        self.fuzzer = FuzzerEngine()
        self.refiner = LLMRefiner(client=llm_client, min_coverage_gain=min_coverage_gain)

    def run(
        self,
        syscall_tbl: str | Path,
        kconfig: str | Path,
        refined_out_dir: str | Path,
        dts: str | Path | None = None,
        driver_root: str | Path | None = None,
        corpus_dir: str | Path | None = None,
    ) -> PipelineMetrics:
        metrics = PipelineMetrics()
        profile = self.profiler.run(syscall_tbl, kconfig, dts=dts, driver_root=driver_root)
        metrics.interfaces_profiled = len(profile.whitelist)

        seeds = self.constructor.run(profile.whitelist)
        metrics.seeds_generated = len(seeds)

        coverage = self.fuzzer.fuzz(seeds)
        candidates = pick_candidates(seeds, coverage)
        metrics.candidates_refined = len(candidates)

        outdir = ensure_dir(refined_out_dir)
        corpus = ensure_dir(corpus_dir) if corpus_dir else None
        for candidate in candidates:
            result = self.refiner.refine(candidate)
            if result.accepted:
                metrics.accepted_refinements += 1
                Path(outdir, f"{result.interface}.syz").write_text(result.refined_dsl + "\n", encoding="utf-8")
                if corpus:
                    save_seed(corpus, result.interface, result.refined_dsl, suffix=".refined")
        return metrics
