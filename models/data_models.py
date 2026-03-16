from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(slots=True)
class InterfaceDefinition:
    name: str
    source: str
    params: List[str] = field(default_factory=list)
    requires_config: Optional[str] = None
    bound_device: Optional[str] = None
    riscv_specific: bool = False


@dataclass(slots=True)
class ProfileResult:
    whitelist: List[InterfaceDefinition]
    filtered_out: Dict[str, str]


@dataclass(slots=True)
class SeedProgram:
    interface: str
    dsl: str
    riscv_specific: bool = False


@dataclass(slots=True)
class CoverageRecord:
    interface: str
    new_basic_blocks: int
    error_codes: List[int] = field(default_factory=list)
    traces: List[str] = field(default_factory=list)


@dataclass(slots=True)
class RefinementCandidate:
    interface: str
    base_dsl: str
    coverage: CoverageRecord


@dataclass(slots=True)
class RefinementResult:
    interface: str
    refined_dsl: str
    accepted: bool
    reason: str
    coverage_gain: int = 0
