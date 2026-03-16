from interface_profiler.syscall_parser import parse_syscall_tbl


def test_parse_syscall_tbl(tmp_path):
    tbl = tmp_path / "syscall.tbl"
    tbl.write_text("0 common read sys_read\n", encoding="utf-8")
    rows = parse_syscall_tbl(tbl)
    assert len(rows) == 1
    assert rows[0].name == "sys_read"
