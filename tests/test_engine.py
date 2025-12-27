import pytest
from dice.engine import parse_dice_string, roll_dice


def test_parse_dice_string():
    assert parse_dice_string("1d20") == (1, 20, 0)
    assert parse_dice_string("2d6+1") == (2, 6, 1)
    assert parse_dice_string("3d10-2") == (3, 10, -2)


def test_parse_dice_string_invalid():
    with pytest.raises(ValueError):
        parse_dice_string("invalid")


def test_roll_dice():
    result = roll_dice(2, 6, 1)
    assert len(result.rolls) == 2
    assert 2 <= result.total <= 12
    assert result.modifier == 1
    assert result.grand_total == result.total + 1
    for roll in result.rolls:
        assert 1 <= roll.result <= 6
        assert roll.sides == 6
