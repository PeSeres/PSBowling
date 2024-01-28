import pytest

from unittest.mock import MagicMock

from src.bowling_ui import BowlingUI


def fill_up_entry_fields(ui, frame_values=None):
    if frame_values is None:
        frame_values = [[], [], [], [], [], [], [], [], [], [[], [], []]]

    for frame in frame_values:
        if not frame:
            frame.append('')
            frame.append('')

    ui.entry_fields = [[MockEntry(value) for value in frame] for frame in frame_values]


class MockEntry:
    def __init__(self, value=''):
        self.value = value
        self.state = ''

    def get(self):
        return self.value

    def set_state(self, state):
        self.state = state

    def config(self, state):
        self.state = state

    def delete(self, start, end):
        self.value = ''

    def insert(self, index, value):
        self.value = value


@pytest.mark.parametrize("frame_values, expected_scores", [
    ([["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"],
      ["0", "0", "0"]], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ([["6", "1"], ["6", "/"], ["2", "3"], ["x"], ["x"], ["2", "2"], ["4", "2"], ["7", "1"], ["1", "3"], ["1", "0"]],
     [7, 19, 24, 46, 60, 64, 70, 78, 82, 83]),
    ([["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X", "X", "X"]],
     [30, 60, 90, 120, 150, 180, 210, 240, 270, 300]),
    ([["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X", "X", "9"]],
     [30, 60, 90, 120, 150, 180, 210, 240, 270, 299]),
    ([["4", "5"], ["6", "/"], ["2", "3"], [], [], [], [], [], [], []], [9, 21, 26]),
    ([["X"], ["3", "/"], ["1", ""], [], [], [], [], [], [], []], [20, 31, 32])
])
def test_calculate_and_update_scores(frame_values, expected_scores):
    ui = BowlingUI(None)

    fill_up_entry_fields(ui, frame_values)

    ui.score_labels = [MagicMock() for _ in range(10)]

    ui.calculate_and_update_scores()

    for i, expected_score in enumerate(expected_scores):
        ui.score_labels[i].config.assert_called_with(text=str(expected_score))


@pytest.mark.parametrize("frame_index, frame_values, expected", [
    (9, [["X"], ["X"], ["x"], ["x"], ["x"], ["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"], ["0"]], True),
    (9, [["X"], ["X"], ["x"], ["x"], ["x"], ["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"], []], False),
    (7, [["X"], ["X"], ["x"], ["x"], ["x"], ["0", "0"], ["0", "0"], [], [], []], False),
    (1, [["X"], ["1", "/"], ["1", "2"], [], [], [], [], [], [], []], True),
    (0, [["X"], ["3", "/"], ["1", ""], [], [], [], [], [], [], []], True),
    (4, [["X"], ["X"], ["x"], ["x"], ["x"], [], [], [], [], []], True)
])
def test_is_frame_reached(frame_index, frame_values, expected):
    ui = BowlingUI(None)
    fill_up_entry_fields(ui, frame_values)

    result = ui.is_frame_reached(frame_index)
    assert result == expected


@pytest.mark.parametrize("frame_index, frame_entries, expected_next_rolls", [
    (1, [["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"], ["0", "0"],
         ["0", "0", "0"]], [0, 0, 0, 0]),
    (4, [["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X", "X", "X"]], [10, 10]),
    (9, [["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X"], ["X", "X", "X"]], []),
    (0, [["X"], ["3", "/"], ["1", ""], [], [], [], [], [], [], []], [3, 7, 1])
])
def test_get_next_rolls_for_score(frame_index, frame_entries, expected_next_rolls):
    ui = BowlingUI(None)
    fill_up_entry_fields(ui, frame_entries)

    for i, rolls in enumerate(frame_entries):
        for j, roll in enumerate(rolls):
            ui.entry_fields[i][j] = MockEntry(roll)

    result = ui.get_next_rolls_for_score(frame_index)
    assert result == expected_next_rolls


@pytest.mark.parametrize("rolls_10th_frame, expected", [
    (['X', 'X', 'X'], True),
    (['9', '/', 'X'], True),
    (['3', '6', ''], False)
])
def test_is_third_roll_available(rolls_10th_frame, expected):
    ui = BowlingUI(None)
    fill_up_entry_fields(ui)

    for i, roll in enumerate(rolls_10th_frame):
        ui.entry_fields[9][i].value = roll

    result = ui.is_third_roll_available()
    assert result == expected


@pytest.mark.parametrize("frame_index, roll_index, value, expected", [
    (4, 0, 'X', True),
    (0, 1, '2', True),
    (4, 0, '5', True),
    (9, 1, '6', False),
    (3, 0, 'c', False),
    (0, 0, 'c', False)
])
def test_is_write_able(frame_index, roll_index, value, expected):
    ui = BowlingUI(None)
    fill_up_entry_fields(ui)

    if roll_index == 0:
        ui.entry_fields[frame_index][roll_index].value = value
    elif frame_index < 9:
        ui.entry_fields[frame_index][0].value = "1"
        ui.entry_fields[frame_index].append(MockEntry(str(value)))
    else:
        ui.entry_fields[frame_index][0].value = "X"
        ui.entry_fields[frame_index][1].value = "X"
        ui.entry_fields[frame_index][2].value = "X"
        ui.entry_fields[frame_index][roll_index].value = value

    result = ui.is_write_able(value, frame_index, roll_index)
    assert result == expected


@pytest.mark.parametrize("frame_index, roll_index, current_value, next_state", [
    (0, 0, 'X', 'normal'),
    (4, 0, '4', 'normal'),
    (9, 0, 'X', 'normal'),
])
def test_set_next_entry_available(frame_index, roll_index, current_value, next_state):
    ui = BowlingUI(None)
    fill_up_entry_fields(ui)

    ui.set_next_entry_available(current_value, frame_index, roll_index)

    if (current_value == 'X' or roll_index == 1) and frame_index < 9:
        next_frame_index = frame_index + 1
        next_roll_index = 0
    else:
        next_frame_index = frame_index
        next_roll_index = roll_index + 1

    next_entry = ui.entry_fields[next_frame_index][next_roll_index]
    assert next_entry.state == next_state


@pytest.mark.parametrize("frame_index, roll_index,current_value,  entry_fields, expected", [
    (9, 0, "x", [[], [], [], [], [], [], [], [], [], ["x", "x", "x"]], "x"),
    (9, 0, "/", [[], [], [], [], [], [], [], [], [], ["/", "x", "x"]], ""),
    (9, 1, "/", [[], [], [], [], [], [], [], [], [], ["X", "/", "x"]], ""),
    (9, 1, "8", [[], [], [], [], [], [], [], [], [], ["2", "8", "x"]], "/"),
    (9, 2, "/", [[], [], [], [], [], [], [], [], [], ["X", "X", "/"]], ""),
    (9, 2, "3", [[], [], [], [], [], [], [], [], [], ["X", "7", "3"]], "/"),
    (9, 2, "5", [[], [], [], [], [], [], [], [], [], ["X", "7", "5"]], ""),
    (9, 2, "test", [[], [], [], [], [], [], [], [], [], ["X", "X", "test"]], "")
])
def test_handle_10th_frame_input(frame_index, roll_index, current_value, entry_fields, expected):
    ui = BowlingUI(None)
    fill_up_entry_fields(ui, entry_fields)

    ui.handle_10th_frame_input(ui.entry_fields[frame_index][roll_index], current_value, frame_index, roll_index)

    assert ui.entry_fields[frame_index][roll_index].value == expected
