from llm_refiner.llm_client import LLMClient
from llm_refiner.prompt_builder import build_prompt
from llm_refiner.response_parser import parse_refined_dsl
from llm_refiner.validator import validate_syzlang
from models.data_models import RefinementCandidate, RefinementResult


class LLMRefiner:
    def __init__(self, client: LLMClient | None = None) -> None:
        self.client = client or LLMClient()

    def refine(self, candidate: RefinementCandidate) -> RefinementResult:
        prompt = build_prompt(candidate)
        raw = self.client.refine(prompt)
        refined = parse_refined_dsl(raw)
        accepted, reason = validate_syzlang(refined)
        return RefinementResult(interface=candidate.interface, refined_dsl=refined, accepted=accepted, reason=reason)
