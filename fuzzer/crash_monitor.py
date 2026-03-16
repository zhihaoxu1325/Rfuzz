def dedup_signature(stacktrace: str) -> str:
    return stacktrace.strip().splitlines()[0] if stacktrace.strip() else "unknown"
