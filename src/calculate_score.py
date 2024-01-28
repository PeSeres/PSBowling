from src.helpers import is_strike, is_spare


class CalculateScore:
    @staticmethod
    def calculate_score_for_frame(frame_index, rolls, next_rolls):
        if frame_index < 9:
            if is_strike(rolls[0]):
                if frame_index < 8 and len(next_rolls) > 1 and is_spare(next_rolls[1]):  # Next frame is spare
                    return 20
                else:
                    return 10 + sum(map(int, next_rolls[:2]))
            elif is_spare(rolls[1]):
                return 10 + (int(next_rolls[0]) if next_rolls else 0)
            else:
                return sum(int(roll) for roll in rolls if roll.isdigit())
        else:
            # Special handling for 10th frame
            return CalculateScore.calculate_10th_frame_score(rolls)

    @staticmethod
    def calculate_10th_frame_score(rolls):
        score = 0
        for roll in rolls:
            if is_strike(roll):
                score += 10
            elif is_spare(roll):
                score += 10 - (int(rolls[rolls.index('/') - 1]) if rolls[rolls.index('/') - 1].isdigit() else 10)
            elif roll.isdigit():
                score += int(roll)
        return score
