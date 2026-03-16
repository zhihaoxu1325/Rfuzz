from interface_profiler.dts_parser import parse_enabled_devices


def test_parse_enabled_devices(tmp_path):
    dts = tmp_path / "test.dts"
    dts.write_text('compatible = "riscv,uart";\n', encoding="utf-8")
    assert "riscv,uart" in parse_enabled_devices(dts)
