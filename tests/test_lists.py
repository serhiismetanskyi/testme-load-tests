"""Get test case lists."""

import random

from locust import SequentialTaskSet, task

from utils.logger import Logger, LogType
from utils.utils import Utils


class Lists(SequentialTaskSet):
    """Test case lists with pagination."""

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
    def get_list(self):
        """Get all test cases."""
        Logger.add_request("List Tests", "/api/tests", "GET")
        with self.client.get(
            url="/api/tests", headers=self.headers, catch_response=True, name="List Test Cases"
        ) as response:
            task_result = ""
            if response.status_code != 200:
                failure_info = (
                    f"List of tests receiving failed by user: {self.username}. "
                    f"Response: {response.text}. Status code: {response.status_code}."
                )
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                task_result = failure_info
            else:
                success_info = f"List of tests successfully received by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                task_result = success_info
            Logger.add_response(response, task_result)

    @task
    def get_list_with_params(self):
        """Get test cases with pagination."""
        page = random.randint(1, 3)
        size = random.randint(1, 5)

        Logger.add_request("List Tests with params", f"/api/tests?page={page}&size={size}", "GET")
        with self.client.get(
            url=f"/api/tests?page={page}&size={size}",
            headers=self.headers,
            catch_response=True,
            name="List Test Cases with params",
        ) as response:
            task_result = ""
            if response.status_code != 200:
                failure_info = (
                    f"List of tests receiving failed by user: {self.username}. "
                    f"Response: {response.text}. Status code: {response.status_code}."
                )
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                task_result = failure_info
            else:
                success_info = f"List of tests successfully received by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                task_result = success_info
            Logger.add_response(response, task_result)

    @task
    def exit_task_execution(self):
        """End task execution."""
        self.interrupt()
