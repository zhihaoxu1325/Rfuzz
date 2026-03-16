from pathlib import Path

from interface_profiler.interface_filter import filter_interfaces
from interface_profiler.kconfig_checker import parse_kconfig
from interface_profiler.syscall_parser import parse_syscall_tbl
from models.data_models import ProfileResult


class InterfaceProfiler:
    def run(self, syscall_tbl: str | Path, kconfig: str | Path) -> ProfileResult:
        interfaces = parse_syscall_tbl(syscall_tbl)
        enabled = parse_kconfig(kconfig)
        whitelist, filtered = filter_interfaces(interfaces, enabled)
        return ProfileResult(whitelist=whitelist, filtered_out=filtered)
