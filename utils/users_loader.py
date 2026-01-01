"""Load users from CSV."""

import csv
from pathlib import Path


class UsersLoader:
    """Load users from CSV queue."""

    users_list = []
    _base_dir = Path(__file__).parent.parent
    csv_file_path = _base_dir / "data" / "users.csv"

    @staticmethod
    def load_users():
        """Load all users from CSV."""
        csv_path = UsersLoader.csv_file_path
        if not csv_path.exists():
            raise FileNotFoundError(f"Users CSV file not found: {UsersLoader.csv_file_path}")

        UsersLoader.users_list.clear()
        with open(csv_path, encoding="utf-8") as csv_file:
            users = csv.DictReader(csv_file)
            for user in users:
                UsersLoader.users_list.append(user)

        if len(UsersLoader.users_list) == 0:
            raise ValueError(f"No users found in CSV file: {UsersLoader.csv_file_path}")

    @staticmethod
    def get_user():
        """Get one user from queue and remove it from the list."""
        if len(UsersLoader.users_list) < 1:
            UsersLoader.load_users()
        if len(UsersLoader.users_list) == 0:
            raise ValueError("No users available in the list")
        user = UsersLoader.users_list.pop()
        return user
