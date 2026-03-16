def classify_param(param_name: str) -> str:
    lowered = param_name.lower()
    if "fd" in lowered:
        return "fd"
    if "ptr" in lowered or "buf" in lowered:
        return "ptr"
    if "struct" in lowered:
        return "struct"
    return "int"
