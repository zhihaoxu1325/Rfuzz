from interface_profiler.dts_parser import parse_enabled_devices


def test_parse_enabled_devices(tmp_path):
    dts = tmp_path / "test.dts"
    dts.write_text(
        'uart0 { compatible = "riscv,uart"; status = "okay"; };\n'
        'spi0 { compatible = "vendor,spi"; status = "disabled"; };\n',
        encoding="utf-8",
    )
    enabled = parse_enabled_devices(dts)
    assert "riscv,uart" in enabled
    assert "vendor,spi" not in enabled
