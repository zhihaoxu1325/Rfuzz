from llm_refiner.refiner import LLMRefiner
from models.data_models import CoverageRecord, RefinementCandidate


def test_refiner_accepts_candidate_with_gain_and_no_placeholder():
    candidate = RefinementCandidate(
        interface="foo",
        base_dsl="foo(const<?>, buffer<any, 64>)",
        coverage=CoverageRecord(interface="foo", new_basic_blocks=2, error_codes=[-22], traces=["t1"]),
    )
    result = LLMRefiner(min_coverage_gain=1).refine(candidate)
    assert result.accepted is True
    assert "<?>" not in result.refined_dsl
    assert result.coverage_gain >= 1
