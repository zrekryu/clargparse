from __future__ import annotations

from typing import Any, override


class ParsedValues(dict[str, Any]):
    @override
    def __repr__(self) -> str:
        values_repr = ", ".join(f"{key}={value!r}" for key, value in self.items())
        return f"{type(self).__name__}({values_repr})"
