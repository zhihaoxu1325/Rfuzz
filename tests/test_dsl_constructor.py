from dsl_constructor.constructor import DSLConstructor
from models.data_models import InterfaceDefinition


def test_constructor_generates_seed():
    seeds = DSLConstructor().run([InterfaceDefinition(name="foo", source="x", params=["fd", "buf"])])
    assert seeds[0].dsl.startswith("foo(")
    assert "const<?>" in seeds[0].dsl
