from models.data_models import InterfaceDefinition, SeedProgram
from dsl_constructor.opensyz_builder import build_seed


class DSLConstructor:
    def run(self, whitelist: list[InterfaceDefinition]) -> list[SeedProgram]:
        return [build_seed(interface) for interface in whitelist]
