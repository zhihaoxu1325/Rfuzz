from models.data_models import InterfaceDefinition, SeedProgram
from dsl_constructor.type_reasoner import choose_placeholder


def build_seed(interface: InterfaceDefinition) -> SeedProgram:
    params = interface.params or ["arg0"]
    rendered = ", ".join(choose_placeholder(p) for p in params)
    dsl = f"{interface.name}({rendered})"
    return SeedProgram(interface=interface.name, dsl=dsl)
