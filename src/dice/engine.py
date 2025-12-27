import random
import re
from typing import Tuple
from dice.models import DieRoll, RollResult


def parse_dice_string(dice_str: str) -> Tuple[int, int, int]:
    """Parse a string like '2d6+1' into (count, sides, modifier)."""
    match = re.match(r"(\d+)d(\d+)([+-]\d+)?", dice_str.lower())
    if not match:
        raise ValueError(f"Invalid dice string: {dice_str}")

    count = int(match.group(1))
    sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0

    return count, sides, modifier


def roll_dice(count: int, sides: int, modifier: int = 0) -> RollResult:
    """Roll the specified dice and return a RollResult."""
    rolls = []
    for _ in range(count):
        result = random.randint(1, sides)
        rolls.append(DieRoll(sides=sides, result=result))

    total = sum(r.result for r in rolls)
    return RollResult(rolls=rolls, total=total, modifier=modifier)
