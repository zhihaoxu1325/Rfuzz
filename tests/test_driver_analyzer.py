from interface_profiler.driver_analyzer import extract_ioctl_files


def test_extract_ioctl_files(tmp_path):
    c = tmp_path / "drv.c"
    c.write_text("int x = _IO('a', 1);", encoding="utf-8")
    files = extract_ioctl_files(tmp_path)
    assert str(c) in files
