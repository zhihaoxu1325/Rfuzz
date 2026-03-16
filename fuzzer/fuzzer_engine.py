from fuzzer.coverage_collector import collect_mock_coverage
from models.data_models import CoverageRecord, SeedProgram


class FuzzerEngine:
    def fuzz(self, seeds: list[SeedProgram]) -> list[CoverageRecord]:
        return collect_mock_coverage(seeds)
