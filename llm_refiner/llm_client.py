class LLMClient:
    """Mockable LLM client abstraction."""

    def refine(self, prompt: str) -> str:
        # A deterministic placeholder implementation for early pipeline wiring.
        return prompt.split("Base:", 1)[1].splitlines()[0].strip().replace("const<?>", "int32")
