from interface_profiler.profiler import InterfaceProfiler
from pipeline.orchestrator import Orchestrator


def test_interface_profiler_filters_enodev(tmp_path):
    syscall_tbl = tmp_path / "syscall.tbl"
    syscall_tbl.write_text("0 common read sys_read\n", encoding="utf-8")
    config = tmp_path / ".config"
    config.write_text("CONFIG_TEST=y\n", encoding="utf-8")
    dts = tmp_path / "board.dts"
    dts.write_text('uart0 { compatible = "riscv,uart"; status = "okay"; };\n', encoding="utf-8")

    driver_dir = tmp_path / "drivers"
    driver_dir.mkdir()
    (driver_dir / "spi_drv.c").write_text(
        'static const struct of_device_id ids[] = { { .compatible = "vendor,spi" }, {} };\nint x = _IO(\'a\', 1);\n',
        encoding="utf-8",
    )

    profile = InterfaceProfiler().run(syscall_tbl, config, dts=dts, driver_root=driver_dir)
    assert "ioctl@spi_drv" in profile.filtered_out
    assert "-ENODEV" in profile.filtered_out["ioctl@spi_drv"]


def test_pipeline_runs_end_to_end_with_corpus_feedback(tmp_path):
    syscall_tbl = tmp_path / "syscall.tbl"
    syscall_tbl.write_text("0 riscv foo sys_riscv_flush_icache\n1 common write sys_write\n", encoding="utf-8")
    config = tmp_path / ".config"
    config.write_text("CONFIG_TEST=y\n", encoding="utf-8")

    refined = tmp_path / "refined"
    corpus = tmp_path / "corpus"

    metrics = Orchestrator().run(syscall_tbl, config, refined, corpus_dir=corpus)
    assert metrics.interfaces_profiled == 2
    assert metrics.seeds_generated == 2
    assert metrics.accepted_refinements >= 1
    assert any(corpus.glob("*.refined.syz"))
