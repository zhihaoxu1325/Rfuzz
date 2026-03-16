from dsl_constructor.constructor import DSLConstructor
from models.data_models import InterfaceDefinition


def test_constructor_generates_seed_and_prioritizes_riscv():
    seeds = DSLConstructor().run(
        [
            InterfaceDefinition(name="sys_write", source="x", params=["fd", "buf"]),
            InterfaceDefinition(name="sys_riscv_flush_icache", source="x", riscv_specific=True),
        ]
    )
    assert seeds[0].interface == "sys_riscv_flush_icache"
    assert seeds[1].dsl.startswith("sys_write(")
    assert "const<?>" in seeds[1].dsl
    assert "buffer<any, 64>" in seeds[1].dsl
