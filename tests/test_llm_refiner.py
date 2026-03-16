from llm_refiner.refiner import LLMRefiner
from models.data_models import CoverageRecord, RefinementCandidate


class StubLLMClient:
    def refine(self, prompt: str) -> str:
        assert "Errnos:" in prompt
        assert "Traces:" in prompt
        return "foo(int32, ptr[in, array[int8, 64]])"

    def estimate_coverage_gain(self, baseline: str, refined: str) -> int:
        return 2 if baseline != refined else 0


def test_refiner_accepts_candidate_with_gain_and_no_placeholder():
    candidate = RefinementCandidate(
        interface="foo",
        base_dsl="foo(const<?>, buffer<any, 64>)",
        coverage=CoverageRecord(interface="foo", new_basic_blocks=2, error_codes=[-22], traces=["t1"]),
    )
    result = LLMRefiner(client=StubLLMClient(), min_coverage_gain=1).refine(candidate)
    assert result.accepted is True
    assert "<?>" not in result.refined_dsl
    assert result.coverage_gain >= 1
