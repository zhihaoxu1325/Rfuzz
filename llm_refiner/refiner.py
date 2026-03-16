from llm_refiner.llm_client import LLMClient
from llm_refiner.prompt_builder import build_prompt
from llm_refiner.response_parser import parse_refined_dsl
from llm_refiner.validator import validate_syzlang
from models.data_models import RefinementCandidate, RefinementResult


class LLMRefiner:
    def __init__(self, client: LLMClient | None = None, min_coverage_gain: int = 1) -> None:
        self.client = client or LLMClient()
        self.min_coverage_gain = min_coverage_gain

    def refine(self, candidate: RefinementCandidate) -> RefinementResult:
        prompt = build_prompt(candidate)
        raw = self.client.refine(prompt)
        refined = parse_refined_dsl(raw)

        valid, reason = validate_syzlang(refined)
        if not valid:
            return RefinementResult(
                interface=candidate.interface,
                refined_dsl=refined,
                accepted=False,
                reason=f"syz-check failed: {reason}",
            )

        gain = self.client.estimate_coverage_gain(candidate.base_dsl, refined)
        accepted = gain >= self.min_coverage_gain
        return RefinementResult(
            interface=candidate.interface,
            refined_dsl=refined,
            accepted=accepted,
            reason="ok" if accepted else "coverage gain below threshold",
            coverage_gain=gain,
        )
