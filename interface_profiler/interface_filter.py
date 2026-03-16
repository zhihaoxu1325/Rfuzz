from models.data_models import InterfaceDefinition


def filter_interfaces(interfaces: list[InterfaceDefinition], enabled_features: dict[str, str]) -> tuple[list[InterfaceDefinition], dict[str, str]]:
    filtered: dict[str, str] = {}
    whitelist: list[InterfaceDefinition] = []
    for interface in interfaces:
        if interface.name.startswith("unused_"):
            filtered[interface.name] = "matched static unsupported rule"
            continue
        whitelist.append(interface)
    return whitelist, filtered
