from pathlib import Path

from interface_profiler.driver_analyzer import parse_driver_interfaces
from interface_profiler.dts_parser import parse_enabled_devices
from interface_profiler.interface_filter import filter_interfaces
from interface_profiler.kconfig_checker import parse_kconfig
from interface_profiler.syscall_parser import parse_syscall_tbl
from models.data_models import InterfaceDefinition, ProfileResult


class InterfaceProfiler:
    def run(
        self,
        syscall_tbl: str | Path,
        kconfig: str | Path,
        dts: str | Path | None = None,
        driver_root: str | Path | None = None,
    ) -> ProfileResult:
        interfaces: list[InterfaceDefinition] = parse_syscall_tbl(syscall_tbl)

        if driver_root:
            interfaces.extend(parse_driver_interfaces(driver_root))

        enabled = parse_kconfig(kconfig)
        enabled_devices = parse_enabled_devices(dts) if dts else set()
        whitelist, filtered = filter_interfaces(interfaces, enabled, enabled_devices)
        return ProfileResult(whitelist=whitelist, filtered_out=filtered)
