from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    lexeme: str

    def __str__(self) -> str:
        return self.lexeme
