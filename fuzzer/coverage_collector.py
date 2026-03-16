from models.data_models import CoverageRecord, SeedProgram


def collect_mock_coverage(seeds: list[SeedProgram]) -> list[CoverageRecord]:
    records: list[CoverageRecord] = []
    for idx, seed in enumerate(seeds):
        blocks = 2 if idx % 2 == 0 else 0
        errno = [-22] if "ioctl" in seed.interface else [0]
        traces = [f"kcov:{seed.interface}:bb{n}" for n in range(blocks)]
        records.append(
            CoverageRecord(
                interface=seed.interface,
                new_basic_blocks=blocks,
                error_codes=errno,
                traces=traces,
            )
        )
    return records
