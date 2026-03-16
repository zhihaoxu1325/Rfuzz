class LLMClient:
    """Mockable LLM client abstraction."""

    def refine(self, prompt: str) -> str:
        # A deterministic placeholder implementation for early pipeline wiring.
        base = prompt.split("Base:", 1)[1].splitlines()[0].strip()
        refined = base.replace("const<?>", "int32").replace("buffer<any, 64>", "ptr[in, array[int8, 64]]")
        return refined

    def estimate_coverage_gain(self, baseline: str, refined: str) -> int:
        score = 0
        if baseline != refined:
            score += 1
        if "int32" in refined or "ptr[" in refined or "struct<auto>" not in refined:
            score += 1
        return score
