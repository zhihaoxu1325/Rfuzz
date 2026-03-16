from models.data_models import InterfaceDefinition


def filter_interfaces(
    interfaces: list[InterfaceDefinition],
    enabled_features: dict[str, str],
    enabled_devices: set[str],
) -> tuple[list[InterfaceDefinition], dict[str, str]]:
    filtered: dict[str, str] = {}
    whitelist: list[InterfaceDefinition] = []

    for interface in interfaces:
        if interface.requires_config:
            state = enabled_features.get(interface.requires_config, "n")
            if state not in {"y", "m"}:
                filtered[interface.name] = "predicted -ENOSYS (feature disabled)"
                continue

        if interface.bound_device and interface.bound_device not in enabled_devices:
            filtered[interface.name] = "predicted -ENODEV (device not present)"
            continue

        whitelist.append(interface)

    return whitelist, filtered
