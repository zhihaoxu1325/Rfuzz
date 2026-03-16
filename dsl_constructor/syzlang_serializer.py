from models.data_models import SeedProgram


def serialize_seed(seed: SeedProgram) -> str:
    return seed.dsl + "\n"
