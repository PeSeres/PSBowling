import tkinter as tk

from helpers import is_valid_input, is_strike, is_spare
from src.calculate_score import CalculateScore


class BowlingUI:
    def __init__(self, root):
        self.score_labels = []
        self.entry_fields = []
        self.root = root
        self.score = CalculateScore()
        if root is not None:
            self.setup_ui()

    def setup_ui(self):
        self.root.geometry("900x150")

        frames_container = tk.Frame(self.root)
        frames_container.pack(padx=8, pady=8)

        for i in range(1, 11):
            frame_ui = tk.Frame(frames_container, borderwidth=2, relief='groove')
            frame_ui.pack(side=tk.LEFT, padx=4, pady=4)

            tk.Label(frame_ui, text=f"{i}", font=('Helvetica', 12)).pack()

            entry_container = tk.Frame(frame_ui)
            entry_container.pack()

            num_entries = 3 if i == 10 else 2
            entries = [tk.Entry(entry_container, width=3, font=('Helvetica', 12)) for _ in range(num_entries)]

            for entry in entries:
                entry.pack(side=tk.LEFT, padx=2)
                entry.bind("<KeyRelease>", self.on_key_release)

            self.entry_fields.append(entries)

            score_label = tk.Label(frame_ui, text="0", font=('Helvetica', 12))
            score_label.pack()
            self.score_labels.append(score_label)

        self.reset_entries()

        reset_button = tk.Button(self.root, text="RESET", command=self.reset)
        reset_button.pack(side=tk.BOTTOM, pady=10)

    def on_key_release(self, event):
        entry = event.widget
        current_value = entry.get().strip().upper()

        frame_index, roll_index = self.find_entry_indices(entry)

        self.set_next_entry_available(current_value, frame_index, roll_index)

        # Handle validation for frames 1-9
        if frame_index < 9:
            if not self.is_write_able(current_value, frame_index, roll_index):
                entry.delete(0, tk.END)
            if roll_index == 1:
                self.validate_second_roll(frame_index)
        else:  # Specific logic for the 10th frame
            self.handle_10th_frame_input(entry, current_value, frame_index, roll_index)

        self.calculate_and_update_scores()
        if event.keysym == 'Return':
            self.move_focus_to_next(entry, frame_index, roll_index)

    def set_next_entry_available(self, current_value, frame_index, roll_index):
        if current_value != '' and roll_index == 0 and frame_index < 9 and not is_strike(current_value):
            self.entry_fields[frame_index][roll_index + 1].config(state='normal')
        elif frame_index < 9:
            self.entry_fields[frame_index + 1][0].config(state='normal')
        else:
            if roll_index == 0 and current_value != '':
                self.entry_fields[frame_index][roll_index + 1].config(state='normal')
            elif roll_index == 1 and current_value != '' and self.is_third_roll_available():
                self.entry_fields[frame_index][roll_index + 1].config(state='normal')

    def calculate_and_update_scores(self):
        accumulated_score = 0
        for frame_index in range(10):
            if self.is_frame_reached(frame_index):
                rolls = [entry.get().strip().upper() for entry in self.entry_fields[frame_index]]
                next_rolls = self.get_next_rolls_for_score(frame_index)
                frame_score = self.score.calculate_score_for_frame(frame_index, rolls, next_rolls)
                accumulated_score += frame_score
                self.score_labels[frame_index].config(text=str(accumulated_score))
            else:
                self.score_labels[frame_index].config(text="")

    def is_frame_reached(self, frame_index):
        first_roll = self.entry_fields[frame_index][0].get().strip().upper()
        return first_roll != ''

    def get_next_rolls_for_score(self, frame_index):
        next_rolls = []
        frames_to_consider = self.entry_fields[frame_index + 1: frame_index + 3]
        for next_frame_rolls in frames_to_consider:
            for roll in next_frame_rolls:
                roll_value = roll.get().strip().upper()
                if roll_value.isdigit():
                    next_rolls.append(int(roll_value))
                elif is_strike(roll_value):
                    next_rolls.append(10)
                # Handle spare separately
                if is_spare(roll_value) and len(next_rolls) < 2:
                    # Add next roll's score for spare calculation
                    next_roll_index = next_frame_rolls.index(roll) + 1
                    if next_roll_index < len(next_frame_rolls):
                        next_roll_value = next_frame_rolls[next_roll_index].get().strip().upper()
                        if next_roll_value.isdigit():
                            next_rolls.append(int(next_roll_value))
                        elif next_roll_value == 'X':
                            next_rolls.append(10)
                    else:
                        next_rolls.append(10 - int(next_rolls[-1]))
                    break
        return next_rolls

    def handle_10th_frame_input(self, entry, current_value, frame_index, roll_index):
        if roll_index == 0 and is_spare(current_value) or not is_valid_input(current_value):
            entry.delete(0, tk.END)

        if roll_index == 1 and (is_spare(current_value) or
                                int(current_value) + int(self.entry_fields[9][0].get()) == 10):
            self.validate_second_roll(frame_index)
        elif roll_index == 2:
            self.validate_third_roll(frame_index)

    def validate_third_roll(self, frame_index):
        second_roll_value = self.entry_fields[frame_index][1].get().strip().upper()
        third_roll_value = self.entry_fields[frame_index][2].get().strip().upper()

        if (second_roll_value.isdigit() and is_strike(third_roll_value)) or \
                (is_strike(second_roll_value) and is_spare(third_roll_value)) or \
                (second_roll_value.isdigit() and third_roll_value.isdigit() and
                 (int(second_roll_value) + int(third_roll_value) > 10)):
            self.entry_fields[frame_index][2].delete(0, tk.END)

        if is_valid_input(second_roll_value) and second_roll_value.isdigit() and \
                int(second_roll_value) + int(third_roll_value) == 10:
            self.entry_fields[frame_index][2].delete(0, tk.END)
            self.entry_fields[frame_index][2].insert(0, '/')

    def is_third_roll_available(self):
        first_roll_value = self.entry_fields[9][0].get().strip().upper()
        second_roll_value = self.entry_fields[9][1].get().strip().upper()

        if is_strike(first_roll_value) or is_spare(second_roll_value):
            self.entry_fields[9][2].config(state='normal')
            return True
        else:
            self.entry_fields[9][2].delete(0, tk.END)
            self.entry_fields[9][2].config(state='disabled')
            return False

    def validate_second_roll(self, frame_index):
        first_roll_value = self.entry_fields[frame_index][0].get().strip()
        second_roll_value = self.entry_fields[frame_index][1].get().strip()

        if first_roll_value.isdigit() and is_strike(second_roll_value) or \
                (is_strike(first_roll_value) and is_spare(second_roll_value)):
            self.entry_fields[frame_index][1].delete(0, tk.END)

        if first_roll_value.isdigit() and second_roll_value.isdigit():
            total_pins = int(first_roll_value) + int(second_roll_value)
            if total_pins > 10:
                self.entry_fields[frame_index][1].delete(0, tk.END)
            elif total_pins == 10:
                self.entry_fields[frame_index][1].delete(0, tk.END)
                self.entry_fields[frame_index][1].insert(0, '/')

    def is_write_able(self, value, frame_index, roll_index):
        if roll_index == 0 and is_spare(value) or not is_valid_input(value):
            return False

        if roll_index == 1:
            first_roll = self.entry_fields[frame_index][0].get().strip().upper()
            second_roll = self.entry_fields[frame_index][1].get().strip().upper()
            if is_strike(first_roll) or is_strike(second_roll):
                return False
        return True

    def move_focus_to_next(self, entry, frame_index, roll_index):
        current_value = entry.get().strip().upper()

        if frame_index < 9:
            if roll_index == 0 and is_strike(current_value):
                self.entry_fields[frame_index + 1][0].focus_set()
            else:
                # Normal focus movement to next roll or next frame
                next_frame_index = frame_index + (roll_index + 1) // 2
                next_roll_index = (roll_index + 1) % 2
                self.entry_fields[next_frame_index][next_roll_index].focus_set()
        elif frame_index == 9:  # Special handling for 10th frame
            self.handle_10th_frame_focus(entry, roll_index)

    def handle_10th_frame_focus(self, entry, roll_index):
        current_value = entry.get().strip().upper()
        if roll_index == 0:
            if is_strike(current_value):
                self.entry_fields[9][1].focus_set()
            else:
                self.entry_fields[9][1].focus_set()
        elif roll_index == 1:
            first_roll = self.entry_fields[9][0].get().strip().upper()
            if is_strike(first_roll) or current_value in ['/', 'X', 'x']:
                self.entry_fields[9][2].focus_set()

    def find_entry_indices(self, entry):
        for i, frame_entries in enumerate(self.entry_fields):
            if entry in frame_entries:
                return i, frame_entries.index(entry)
        return -1, -1

    def reset(self):
        for entries in self.entry_fields:
            for entry in entries:
                entry.delete(0, tk.END)
        for label in self.score_labels:
            label.config(text="0")
        self.reset_entries()
        self.entry_fields[0][0].focus_set()

    def reset_entries(self):
        for entries in self.entry_fields:
            for entry in entries:
                entry.config(state='disabled')
        self.entry_fields[0][0].config(state='normal')
