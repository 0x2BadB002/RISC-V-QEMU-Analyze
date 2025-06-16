from dataclasses import dataclass


@dataclass
class Command:
    cpu_index: int
    command: str
    address: int | None = None
