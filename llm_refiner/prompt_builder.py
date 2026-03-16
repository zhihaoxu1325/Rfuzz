from models.data_models import RefinementCandidate


def build_prompt(candidate: RefinementCandidate) -> str:
    return (
        "Refine the following syzlang-like call for Linux RISC-V.\n"
        f"Interface: {candidate.interface}\n"
        f"Base: {candidate.base_dsl}\n"
        f"NewBlocks: {candidate.coverage.new_basic_blocks}\n"
        f"Errnos: {candidate.coverage.error_codes}\n"
        "Return only refined call syntax."
    )
