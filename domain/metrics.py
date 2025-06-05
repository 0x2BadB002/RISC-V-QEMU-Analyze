from dataclasses import dataclass, field


@dataclass
class VectorOps:
    total: int = 0
    rw: int = 0


@dataclass
class DataAlignment:
    aligned: int = 0
    misaligned: int = 0


@dataclass()
class Scarcity:
    last_seen: int
    mean_distance: int = 0


@dataclass
class Metrics:
    vectorization: VectorOps = field(default_factory=VectorOps)
    address_usage: dict[int, int] = field(default_factory=dict[int, int])
    address_scarcity: dict[int, Scarcity] = field(default_factory=dict[int, Scarcity])
    alignment: DataAlignment = field(default_factory=DataAlignment)
