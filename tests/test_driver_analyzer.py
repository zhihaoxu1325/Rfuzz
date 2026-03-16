from interface_profiler.driver_analyzer import parse_driver_interfaces


def test_extract_ioctl_files(tmp_path):
    c = tmp_path / "drv.c"
    c.write_text(
        """
static const struct of_device_id ids[] = { { .compatible = \"riscv,uart\" }, {} };
int x = _IO('a', 1);
""",
        encoding="utf-8",
    )
    interfaces = parse_driver_interfaces(tmp_path)
    assert len(interfaces) == 1
    assert interfaces[0].name == "ioctl@drv"
    assert interfaces[0].bound_device == "riscv,uart"
