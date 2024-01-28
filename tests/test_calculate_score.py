import pytest

from src.calculate_score import CalculateScore


@pytest.mark.parametrize("frame_index, rolls, next_rolls, expected_score", [
    (0, ['X'], ['7', '/'], 20),
    (0, ['X'], ['7', '2'], 19),
    (4, ['4', '/'], ['5'], 15),
    (4, ['4', '/'], [], 10),
    (3, ['3', '4'], [], 7),
    (9, ['X', 'X', 'X'], [], 30),
    (9, ['9', '/'], [], 10),
    (9, ['3', '4'], [], 7)
])
def test_calculate_score_for_frame(frame_index, rolls, next_rolls, expected_score):
    assert CalculateScore.calculate_score_for_frame(frame_index, rolls, next_rolls) == expected_score


@pytest.mark.parametrize("rolls, expected_score", [
    (['X', 'X', 'X'], 30),
    (['9', '/'], 10),
    (['3', '4'], 7)
])
def test_calculate_10th_frame_score(rolls, expected_score):
    assert CalculateScore.calculate_10th_frame_score(rolls) == expected_score
