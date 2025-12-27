import pytest
from dice.engine import parse_dice_string, roll_dice


def test_parse_dice_string():
    assert parse_dice_string("1d20") == (1, 20, 0)
    assert parse_dice_string("2d6+1") == (2, 6, 1)
    assert parse_dice_string("3d10-2") == (3, 10, -2)


def test_parse_dice_string_invalid():
    with pytest.raises(ValueError):
        parse_dice_string("invalid")


def test_roll_dice_basic():
    result = roll_dice(2, 6, 1)
    assert len(result.rolls) == 2
    assert 2 <= result.total <= 12
    assert result.modifier == 1
    assert result.grand_total == result.total + 1
    assert result.method == "normal"
    assert len(result.dropped_rolls) == 0


def test_roll_dice_advantage():
    # It's hard to test randomness deterministically without mocking,
    # but we can verify structure and basic logic properties.
    result = roll_dice(1, 20, 0, advantage=True)
    assert result.method == "advantage"
    assert len(result.rolls) == 1
    assert len(result.dropped_rolls) == 1

    kept_val = result.rolls[0].result
    dropped_val = result.dropped_rolls[0].result
    assert kept_val >= dropped_val


def test_roll_dice_disadvantage():
    result = roll_dice(1, 20, 0, disadvantage=True)
    assert result.method == "disadvantage"
    assert len(result.rolls) == 1
    assert len(result.dropped_rolls) == 1

    kept_val = result.rolls[0].result
    dropped_val = result.dropped_rolls[0].result
    assert kept_val <= dropped_val


def test_roll_dice_cancel():
    result = roll_dice(1, 20, 0, advantage=True, disadvantage=True)
    assert result.method == "normal"
    assert len(result.dropped_rolls) == 0
