"""Get statistics tests."""

from locust import SequentialTaskSet, task

from utils.logger import Logger, LogType
from utils.utils import Utils


class Stats(SequentialTaskSet):
    """Test case statistics operations."""

    def on_start(self):
        """Get user data and token."""
        self.username = self.user.get_username()
        self.token = self.user.get_token()
        if not self.token:
            error_msg = f"Cannot proceed: token is missing for user {self.username}"
            Logger.log_message(error_msg, LogType.ERROR)
            self.interrupt()
            return
        self.headers = Utils.get_headers_with_token(self.token)

    @task
    def get_stats(self):
        """Get test case statistics."""
        Logger.add_request("Get Stats", "/api/getstat", "GET")
        with self.client.get(
            url="/api/getstat", headers=self.headers, catch_response=True, name="Get Stats"
        ) as response:
            task_result = ""
            if response.status_code != 200:
                failure_info = (
                    f"Test stats receiving failed by user: {self.username}. "
                    f"Response: {response.text}. Status code: {response.status_code}."
                )
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                task_result = failure_info
            else:
                success_info = f"Test stats successfully received by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                task_result = success_info
            Logger.add_response(response, task_result)

    @task
    def exit_task_execution(self):
        """End task execution."""
        self.interrupt()
