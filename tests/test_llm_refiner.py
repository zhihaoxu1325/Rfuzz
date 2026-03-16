from llm_refiner.refiner import LLMRefiner
from models.data_models import CoverageRecord, RefinementCandidate


def test_refiner_accepts_simple_candidate():
    candidate = RefinementCandidate(
        interface="foo",
        base_dsl="foo(const<?>)",
        coverage=CoverageRecord(interface="foo", new_basic_blocks=2),
    )
    result = LLMRefiner().refine(candidate)
    assert result.accepted is True
    assert "int32" in result.refined_dsl
