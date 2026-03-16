from interface_profiler.syscall_parser import parse_syscall_tbl


def test_parse_syscall_tbl(tmp_path):
    tbl = tmp_path / "syscall.tbl"
    tbl.write_text("0 riscv openat2 sys_openat2\n1 common write sys_write\n", encoding="utf-8")
    rows = parse_syscall_tbl(tbl)
    assert len(rows) == 2
    assert rows[0].name == "sys_openat2"
    assert rows[0].riscv_specific is True
    assert rows[1].riscv_specific is False
