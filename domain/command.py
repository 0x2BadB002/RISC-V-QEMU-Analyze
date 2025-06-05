from dataclasses import dataclass


@dataclass
class Command:
    command: str
    address: int | None = None
