from dataclasses import dataclass


@dataclass(slots=True)
class PipelineMetrics:
    interfaces_profiled: int = 0
    seeds_generated: int = 0
    candidates_refined: int = 0
    accepted_refinements: int = 0
