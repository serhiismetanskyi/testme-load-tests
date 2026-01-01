"""User authentication - login/logout."""

from locust import between

from tests.abstract_user import AbstractUser
from utils.logger import Logger, LogType
from utils.users_loader import UsersLoader
from utils.utils import Utils


class RegisteredHttpUser(AbstractUser):
    """User with auth. Auto login on start, logout on stop."""

    wait_time = between(1, 2)
    abstract = True

    username = ""

    @classmethod
    def verify_login(cls, response, username):
        """Check if login successful."""
        if response.status_code != 200:
            failure_info = (
                f"Login failed for user: {username}. Response: {response.text}. Status code: {response.status_code}."
            )
            response.failure(failure_info)
            Logger.log_message(failure_info, LogType.ERROR)
            return False
        return True

    @classmethod
    def verify_logout(cls, response, username):
        """Check if logout successful."""
        if response.status_code != 200:
            failure_info = (
                f"Logout failed for user: {username}. Response: {response.text}. Status code: {response.status_code}."
            )
            response.failure(failure_info)
            Logger.log_message(failure_info, LogType.ERROR)
            return False
        return True

    def on_start(self):
        """Load user from CSV and login."""
        try:
            user = UsersLoader.get_user()
            if not user or "username" not in user:
                error_msg = "Invalid user data: missing username"
                Logger.log_message(error_msg, LogType.ERROR)
                return

            headers = Utils.get_base_headers()
            username = user["username"]
            self.username = username

            Logger.add_request("User Login", "/api/auth/login", "POST", user)
            with self.client.post(
                url="/api/auth/login", json=user, headers=headers, catch_response=True, name="Login"
            ) as response:
                task_result = ""
                if self.verify_login(response, self.username):
                    success_info = f"Login successfully for user: {self.username}"
                    response.success()
                    Logger.log_message(success_info, LogType.INFO)
                    super().set_username(self.username)
                    token = Utils.extract_token_from_response(response)
                    if token:
                        super().set_token(token)
                        task_result = success_info
                    else:
                        error_msg = f"Failed to extract token for user: {self.username}"
                        Logger.log_message(error_msg, LogType.ERROR)
                        task_result = error_msg
                else:
                    task_result = f"Login failed for user: {self.username}"
                Logger.add_response(response, task_result)
        except (KeyError, ValueError, FileNotFoundError) as e:
            error_msg = f"Failed to load user: {str(e)}"
            Logger.log_message(error_msg, LogType.ERROR)

    def on_stop(self):
        """Logout user."""
        token = super().get_token()
        headers = Utils.get_base_headers()
        if token:
            headers = Utils.get_headers_with_token(token)

        Logger.add_request("User Logout", "/api/auth/logout", "GET")
        with self.client.get(url="/api/auth/logout", headers=headers, catch_response=True, name="Logout") as response:
            task_result = ""
            if self.verify_logout(response, self.username):
                success_info = f"Logout successfully for user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                super().clear_user_data()
                task_result = success_info
            else:
                task_result = f"Logout failed for user: {self.username}"
            Logger.add_response(response, task_result)
