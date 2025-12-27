import random
import re
from typing import Tuple, List
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


def _roll_set(count: int, sides: int) -> List[DieRoll]:
    """Helper to roll a set of dice."""
    return [DieRoll(sides=sides, result=random.randint(1, sides)) for _ in range(count)]


def roll_dice(
    count: int,
    sides: int,
    modifier: int = 0,
    advantage: bool = False,
    disadvantage: bool = False,
) -> RollResult:
    """
    Roll dice with optional advantage or disadvantage.

    If advantage/disadvantage is set, we roll the set twice and compare totals.
    """
    if advantage and disadvantage:
        # cancel out
        advantage = False
        disadvantage = False

    rolls1 = _roll_set(count, sides)
    total1 = sum(r.result for r in rolls1)

    if not advantage and not disadvantage:
        return RollResult(rolls=rolls1, total=total1, modifier=modifier)

    rolls2 = _roll_set(count, sides)
    total2 = sum(r.result for r in rolls2)

    # Determine winner
    keep_set1 = True
    if advantage:
        if total2 > total1:
            keep_set1 = False
        method = "advantage"
    else:  # disadvantage
        if total2 < total1:
            keep_set1 = False
        method = "disadvantage"

    if keep_set1:
        return RollResult(
            rolls=rolls1,
            total=total1,
            modifier=modifier,
            dropped_rolls=rolls2,
            method=method,
        )
    else:
        return RollResult(
            rolls=rolls2,
            total=total2,
            modifier=modifier,
            dropped_rolls=rolls1,
            method=method,
        )
