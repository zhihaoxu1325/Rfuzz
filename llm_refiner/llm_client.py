from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib import request
from urllib.error import HTTPError, URLError


class LLMClient:
    """OpenAI-compatible API client used by RFuzz refiner."""

    def __init__(self, config_path: str | Path = "config/llm_config.yaml") -> None:
        cfg = self._load_config(config_path)
        self.provider = cfg.get("provider", "openai_compatible")
        self.model = cfg.get("model", "")
        self.api_base = str(cfg.get("api_base", "")).rstrip("/")
        self.api_key = cfg.get("api_key", "") or ""
        self.temperature = float(cfg.get("temperature", 0.2))
        self.max_tokens = int(cfg.get("max_tokens", 1024))
        self.timeout_s = int(cfg.get("timeout_s", 60))

    @staticmethod
    def _load_config(config_path: str | Path) -> dict[str, Any]:
        path = Path(config_path)
        if not path.exists():
            return {}

        # Lightweight YAML parser for flat "key: value" config files.
        parsed: dict[str, Any] = {}
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            key, value = line.split(":", 1)
            parsed[key.strip()] = value.strip().strip('"').strip("'")
        return parsed

    def refine(self, prompt: str) -> str:
        if not self.api_base:
            raise RuntimeError("LLM API base is not configured")

        url = f"{self.api_base}/chat/completions"
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "messages": [
                {"role": "system", "content": "You are a syzlang expert for Linux RISC-V fuzzing."},
                {"role": "user", "content": prompt},
            ],
        }

        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = request.Request(url, data=data, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=self.timeout_s) as resp:
                body = resp.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore") if hasattr(exc, "read") else str(exc)
            raise RuntimeError(f"LLM API HTTP error: {exc.code} {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"LLM API connection error: {exc.reason}") from exc

        parsed = json.loads(body)
        choices = parsed.get("choices") or []
        if not choices:
            raise RuntimeError("LLM API returned empty choices")

        message = choices[0].get("message") or {}
        content = (message.get("content") or "").strip()
        if not content:
            raise RuntimeError("LLM API returned empty content")
        return content

    def estimate_coverage_gain(self, baseline: str, refined: str) -> int:
        score = 0
        if baseline != refined:
            score += 1
        if "int" in refined or "ptr[" in refined or "array[" in refined:
            score += 1
        return score
