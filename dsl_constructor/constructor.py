from dsl_constructor.opensyz_builder import build_seed
from models.data_models import InterfaceDefinition, SeedProgram


class DSLConstructor:
    def run(self, whitelist: list[InterfaceDefinition]) -> list[SeedProgram]:
        # Keep RISC-V-specific interfaces at the head to guarantee they are exercised early.
        ordered = sorted(whitelist, key=lambda item: (not item.riscv_specific, item.name))
        return [build_seed(interface) for interface in ordered]
