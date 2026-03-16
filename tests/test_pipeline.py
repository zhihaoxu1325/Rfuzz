from pipeline.orchestrator import Orchestrator


def test_pipeline_runs_end_to_end(tmp_path):
    syscall_tbl = tmp_path / "syscall.tbl"
    syscall_tbl.write_text("0 common read sys_read\n1 common write sys_write\n", encoding="utf-8")
    config = tmp_path / ".config"
    config.write_text("CONFIG_TEST=y\n", encoding="utf-8")

    metrics = Orchestrator().run(syscall_tbl, config, tmp_path / "refined")
    assert metrics.interfaces_profiled == 2
    assert metrics.seeds_generated == 2
    assert metrics.accepted_refinements >= 1
