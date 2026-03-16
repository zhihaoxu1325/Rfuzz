from models.data_models import CoverageRecord, SeedProgram


def collect_mock_coverage(seeds: list[SeedProgram]) -> list[CoverageRecord]:
    records: list[CoverageRecord] = []
    for idx, seed in enumerate(seeds):
        blocks = 1 if idx % 2 == 0 else 0
        records.append(CoverageRecord(interface=seed.interface, new_basic_blocks=blocks, error_codes=[0], traces=[]))
    return records
