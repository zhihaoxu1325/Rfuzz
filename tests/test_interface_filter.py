from interface_profiler.interface_filter import filter_interfaces
from models.data_models import InterfaceDefinition


def test_filter_interfaces_marks_enosys_when_config_missing():
    interfaces = [InterfaceDefinition(name="sys_foo", source="syscall.tbl", requires_config="CONFIG_FOO")]
    whitelist, filtered = filter_interfaces(interfaces, enabled_features={}, enabled_devices=set())
    assert not whitelist
    assert "sys_foo" in filtered
    assert "-ENOSYS" in filtered["sys_foo"]
