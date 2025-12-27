from pydantic import BaseModel, Field
from typing import List


class DieRoll(BaseModel):
    sides: int
    result: int


class RollResult(BaseModel):
    rolls: List[DieRoll]
    total: int
    modifier: int = 0
    # New fields for Advantage/Disadvantage context
    dropped_rolls: List[DieRoll] = Field(default_factory=list)
    method: str = "normal"  # normal, advantage, disadvantage

    @property
    def grand_total(self) -> int:
        return self.total + self.modifier


class Theme(BaseModel):
    name: str
    description: str
    icons: dict[int, str] = Field(default_factory=dict)
