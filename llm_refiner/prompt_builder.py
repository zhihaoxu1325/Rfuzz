from models.data_models import RefinementCandidate


def build_prompt(candidate: RefinementCandidate) -> str:
    return (
        "Refine the following syzlang-like call for Linux RISC-V.\n"
        "Use precise syzlang-compatible types.\n"
        f"Interface: {candidate.interface}\n"
        f"Base: {candidate.base_dsl}\n"
        f"NewBlocks: {candidate.coverage.new_basic_blocks}\n"
        f"Errnos: {candidate.coverage.error_codes}\n"
        f"Traces: {candidate.coverage.traces}\n"
        "Return only refined call syntax."
    )
