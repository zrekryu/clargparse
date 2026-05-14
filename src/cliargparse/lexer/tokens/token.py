from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    argument: str

    def __str__(self) -> str:
        return self.argument
