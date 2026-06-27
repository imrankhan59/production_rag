from dataclasses import dataclass


@dataclass(frozen=True)
class IngestedDocument:
    content: str
    source: str
