from . import functions

is_deadline_now_diff_negative = functions.get_deadline_now_diff() < 0
has_timer_minutes_occurred = functions.get_timer_diff() % 60 == 0
