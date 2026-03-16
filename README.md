# RFuzz

RFuzz is an LLM-driven, self-evolving interface fuzzing framework for the **Linux RISC-V kernel**.

It is built around a three-stage closed loop:

1. **Interface Profiler**: statically discovers interfaces and filters out unreachable ones on the current board.
2. **DSL Constructor**: automatically generates OpenSyz/syzlang seeds with placeholders.
3. **LLM Refiner**: refines only high-value interfaces based on coverage feedback and feeds accepted results back into the corpus.

---

## Current Implementation Status

This repository already provides a runnable minimal scaffold with the following capabilities:

- `syscall.tbl` parsing with RISC-V interface tagging.
- DTS parsing for `compatible` / `status` fields.
- Driver ioctl interface extraction with device-binding metadata.
- Interface filtering based on `.config` and DTS, including predicted `-ENOSYS` and `-ENODEV` paths.
- Placeholder-based seed construction (`const<?>`, `buffer<any, 64>`, `struct<auto>`).
- API-based LLM invocation (OpenAI-compatible `POST /chat/completions`).
- Refinement acceptance logic based on new basic blocks and minimum coverage-gain threshold.
- Refined output persistence to `data/syzlang_output/refined` plus corpus write-back.

> Note: QEMU/Syzkaller runtime managers are still stubs and are intended to be replaced by real integrations.

---

## Project Layout

```text
rfuzz/
├── config/
│   ├── rfuzz_config.yaml
│   └── llm_config.yaml
├── interface_profiler/
├── dsl_constructor/
├── llm_refiner/
├── fuzzer/
├── pipeline/
├── models/
├── utils/
├── scripts/
├── tests/
└── main.py
```

---

## Three-Stage Workflow

### 1) Interface Profiler

Inputs:

- `syscall.tbl`
- Kernel `.config`
- (Optional) board DTS
- (Optional) driver source directory

Outputs:

- `whitelist`: reachable interfaces
- `filtered_out`: filtered interfaces with reasons (for example `predicted -ENOSYS` / `predicted -ENODEV`)

### 2) DSL Constructor

- Builds placeholder calls for interfaces in the whitelist.
- Prioritizes RISC-V-specific interfaces so they are exercised early during initial fuzzing.

### 3) LLM Refiner

- Selects only interfaces that triggered new KCOV basic blocks.
- Sends interface/base DSL/error codes/traces as context to the LLM API.
- Validates refined output (syntax + placeholder cleanup) and applies coverage-gain gating.
- Writes accepted refinements to refined output and feeds them back into the corpus.

---

## Quick Start

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure LLM API

Edit `config/llm_config.yaml`:

```yaml
provider: openai_compatible
model: gpt-5.2-codex
api_base: http://localhost:8000/v1
api_key: ""
temperature: 0.2
max_tokens: 1024
timeout_s: 60
```

- `api_key` is intentionally empty by default.
- `api_base` must point to a service compatible with `/chat/completions`.

### 3. Run tests

```bash
pytest -q
```

### 4. Run the entrypoint example

```bash
python main.py
```

By default, it tries to read:

- `data/kernel_source/arch/riscv/kernel/syscalls/syscall.tbl`
- `data/kernel_source/.config`

Prepare these inputs before running.

---

## Key Configuration

### `config/rfuzz_config.yaml`

- `paths.*`: corpus, coverage, logs, and output directories.
- `pipeline.min_coverage_gain`: acceptance threshold for refinement.
- `pipeline.max_refine_rounds`: max iteration rounds (reserved for future use).

### `config/llm_config.yaml`

- `api_base`: LLM gateway endpoint.
- `api_key`: API token (can be empty).
- `model`: model identifier.
- `temperature` / `max_tokens`: generation settings.

---

## Test Coverage

Current tests cover:

- syscall parsing
- DTS parsing
- driver ioctl extraction
- interface filtering (`ENOSYS` / `ENODEV`)
- DSL construction (including RISC-V prioritization)
- LLM refiner behavior
- end-to-end pipeline smoke path (including corpus write-back)

---

## Next Steps

- Integrate real `syz-check` execution instead of lightweight validation.
- Replace mock coverage collector with real KCOV-driven collection.
- Upgrade QEMU/Syzkaller managers from stubs to managed runtime controllers.
- Improve parameter type reasoning and syscall semantic constraints.

---

## License

Not specified yet (you can add MIT / Apache-2.0 / internal policy license as needed).
