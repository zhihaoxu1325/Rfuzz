from models.data_models import CoverageRecord, RefinementCandidate, SeedProgram


def pick_candidates(seeds: list[SeedProgram], coverage: list[CoverageRecord]) -> list[RefinementCandidate]:
    by_if = {c.interface: c for c in coverage if c.new_basic_blocks > 0}
    candidates: list[RefinementCandidate] = []
    for seed in seeds:
        if seed.interface in by_if:
            candidates.append(
                RefinementCandidate(interface=seed.interface, base_dsl=seed.dsl, coverage=by_if[seed.interface])
            )
    return candidates
