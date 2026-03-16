def validate_syzlang(dsl: str) -> tuple[bool, str]:
    if "(" not in dsl or ")" not in dsl:
        return False, "invalid call syntax"
    return True, "ok"
