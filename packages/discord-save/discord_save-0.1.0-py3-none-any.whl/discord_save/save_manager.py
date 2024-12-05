import json
import os

class SaveManager:
    def __init__(self, save_file="save_data.json"):
        """
        Initialize the SaveManager with a specified save file.
        :param save_file: The path to the save file.
        """
        self.save_file = save_file
        self.data = {}
        self._load_data()

    def _load_data(self):
        """Loads the data from the save file."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as file:
                    self.data = json.load(file)
            except json.JSONDecodeError:
                print("Save file is corrupted. Starting with a fresh file.")
                self.data = {}
        else:
            self.data = {}

    def save(self):
        """Writes the current data to the save file."""
        with open(self.save_file, "w") as file:
            json.dump(self.data, file, indent=4)

    def get_user(self, user_id):
        """
        Retrieve data for a specific user.
        :param user_id: The Discord user ID.
        :return: User's data as a dictionary.
        """
        if user_id not in self.data:
            self.data[user_id] = {
                "balance": 0,
                "games_played": 0,
                "games_won": 0
            }
        return self.data[user_id]

    def update_user(self, user_id, **kwargs):
        """
        Update a user's stats.
        :param user_id: The Discord user ID.
        :param kwargs: Key-value pairs to update.
        """
        user_data = self.get_user(user_id)
        for key, value in kwargs.items():
            if key in user_data:
                user_data[key] = value
            else:
                print(f"Warning: {key} is not a recognized field.")
        self.data[user_id] = user_data

    def reset_user(self, user_id):
        """
        Resets a user's stats to default values.
        :param user_id: The Discord user ID.
        """
        if user_id in self.data:
            del self.data[user_id]
        self.get_user(user_id)  # Reinitialize the user

    def get_all_users(self):
        """Returns all user data."""
        return self.data
