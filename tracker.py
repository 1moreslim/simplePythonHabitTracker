import json
import os
from utils import log_action

class Habit:
    def __init__(self, name, frequency, habit_type):
        self.name = name
        self.frequency = frequency
        self.habit_type = habit_type
        self.dates_completed = set()

    def to_dict(self):
        return {
            "name": self.name,
            "frequency": self.frequency,
            "habit_type": self.habit_type,
            "dates_completed": list(self.dates_completed)
        }

    @classmethod
    def from_dict(cls, data):

        habit_type = data.get("habit_type", "Good")
        habit = cls(data["name"], data["frequency"], habit_type)
        habit.dates_completed = set(data["dates_completed"])
        return habit


class TrackerManager:
    def __init__(self, filename="habits.json"):
        self.filename = filename
        self.all_users_data = {}
        self.current_user = None
        self.habits = {}
        self.load_data()

    def login(self, username):
        """Sets the current user, creating a new profile if they don't exist."""
        self.current_user = username
        if username not in self.all_users_data:
            self.all_users_data[username] = {}
        self.habits = self.all_users_data[username]
        self.save_data()

    @log_action
    def add_habit(self, name, frequency, habit_type):
        if name in self.habits:
            raise ValueError(f"Habit '{name}' already exists!")
        self.habits[name] = Habit(name, frequency, habit_type)
        self.save_data()

    @log_action
    def mark_completed(self, name, date_str):
        if name in self.habits:
            self.habits[name].dates_completed.add(date_str)
            self.save_data()
        else:
            raise KeyError("Habit not found.")

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:

            data = {
                user: {h_name: h_obj.to_dict() for h_name, h_obj in user_habits.items()}
                for user, user_habits in self.all_users_data.items()
            }
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.all_users_data = {
                    user: {h_name: Habit.from_dict(h_data) for h_name, h_data in user_habits.items()}
                    for user, user_habits in data.items()
                }

    def get_habits_by_type(self, h_type):
        """Generator yielding habits of a specific type."""
        for habit in self.habits.values():
            if habit.habit_type == h_type:
                yield habit

    def get_sorted_habits(self):
        """Lambda sorting by highest success rate."""
        return sorted(self.habits.values(), key=lambda h: len(h.dates_completed), reverse=True)