"""Base Locust user class."""

from locust import HttpUser


class AbstractUser(HttpUser):
    """Base HTTP user. Stores user data and token."""

    abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_data = {}

    def set_username(self, username):
        """Set username."""
        self.user_data["username"] = username

    def get_username(self):
        """Get username."""
        if "username" in self.user_data:
            return self.user_data["username"]
        else:
            return None

    def set_token(self, token):
        """Set auth token."""
        self.user_data["token"] = token

    def get_token(self):
        """Get auth token."""
        return self.user_data.get("token")

    def clear_user_data(self):
        """Clear user data."""
        self.user_data.clear()
