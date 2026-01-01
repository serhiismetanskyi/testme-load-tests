"""Test cases CRUD operations."""

import time

from locust import SequentialTaskSet, task

from data.test_data import NewTest
from utils.logger import Logger, LogType
from utils.utils import Utils


class Tests(SequentialTaskSet):
    """Test case operations: create -> get -> update -> delete."""

    test_id = ""

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
    def create_new_test(self):
        """Create new test case."""
        test = NewTest()
        test.set_test_name(f"API Test {int(time.time() * 1000)}")
        test.set_test_desc(f"Checking the creation of a new test by {self.username}. Endpoint: /api/tests/new")

        test_name = test.get_test_name()
        test_desc = test.get_test_desc()

        form_data = {"name": test_name, "description": test_desc}

        Logger.add_request("Create Test", "/api/tests/new", "POST", form_data)
        with self.client.post(
            url="/api/tests/new", json=form_data, headers=self.headers, catch_response=True, name="Create new Test"
        ) as response:
            task_result = ""
            if response.status_code != 201:
                failure_info = (
                    f"Test creation failed by user: {self.username}. "
                    f"Response: {response.text}. Status code: {response.status_code}."
                )
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                task_result = failure_info
            else:
                success_info = f"Test successfully created by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                task_result = success_info
            try:
                response_json = response.json()
                if "test_id" in response_json:
                    self.test_id = response_json["test_id"]
                    test.set_test_id(self.test_id)
                else:
                    Logger.log_message("Response missing test_id field", LogType.ERROR)
            except (ValueError, KeyError) as e:
                Logger.log_message(f"Failed to parse response JSON: {str(e)}", LogType.ERROR)
            Logger.add_response(response, task_result)

    @task
    def get_test(self):
        """Get test case by ID."""
        if not self.test_id:
            Logger.log_message("Cannot get test: test_id is not set", LogType.ERROR)
            return

        Logger.add_request("Get Test", f"/api/tests/{self.test_id}", "GET")
        with self.client.get(
            url=f"/api/tests/{self.test_id}", headers=self.headers, catch_response=True, name="Get Test Case by ID"
        ) as response:
            task_result = ""
            if response.status_code != 200:
                failure_info = (
                    f"Test receiving failed by user: {self.username}. "
                    f"Response: {response.text}. Status code: {response.status_code}."
                )
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                task_result = failure_info
            else:
                success_info = f"Test successfully received by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                task_result = success_info
            Logger.add_response(response, task_result)

    @task
    def update_test(self):
        """Full update test case (PUT)."""
        if not self.test_id:
            Logger.log_message("Cannot update test: test_id is not set", LogType.ERROR)
            return

        test_new_name = f"Updated API Test {int(time.time() * 1000)}"
        test_new_desc = f"Checking the update a test by {self.username}."

        form_data = {"name": test_new_name, "description": test_new_desc}

        Logger.add_request("Update Test", f"/api/tests/{self.test_id}", "PUT", form_data)
        with self.client.put(
            url=f"/api/tests/{self.test_id}",
            json=form_data,
            headers=self.headers,
            catch_response=True,
            name="Update Test Case by ID",
        ) as response:
            task_result = ""
            if response.status_code != 200:
                failure_info = (
                    f"Test changing failed by user: {self.username}. "
                    f"Response: {response.text}. Status code: {response.status_code}."
                )
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                task_result = failure_info
            else:
                success_info = f"Test successfully changed by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                task_result = success_info
            Logger.add_response(response, task_result)

    @task
    def partial_update_test(self):
        """Partial update test case (PATCH)."""
        if not self.test_id:
            Logger.log_message("Cannot partial update test: test_id is not set", LogType.ERROR)
            return

        test_new_desc = f"Checking the update a test description by {self.username}."

        form_data = {"description": test_new_desc}

        Logger.add_request("Partial Update Test", f"/api/tests/{self.test_id}", "PATCH", form_data)
        with self.client.patch(
            url=f"/api/tests/{self.test_id}",
            json=form_data,
            headers=self.headers,
            catch_response=True,
            name="Partial Update Test Case by ID",
        ) as response:
            task_result = ""
            if response.status_code != 200:
                failure_info = (
                    f"Test description changing failed by user: {self.username}. "
                    f"Response: {response.text}. Status code: {response.status_code}."
                )
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                task_result = failure_info
            else:
                success_info = f"Test description successfully changed by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                task_result = success_info
            Logger.add_response(response, task_result)

    @task
    def run_test(self):
        """Set test status to PASS."""
        if not self.test_id:
            Logger.log_message("Cannot run test: test_id is not set", LogType.ERROR)
            return

        form_data = {"status": "PASS"}

        Logger.add_request("Run Test", f"/api/tests/{self.test_id}/status", "POST", form_data)
        with self.client.post(
            url=f"/api/tests/{self.test_id}/status",
            json=form_data,
            headers=self.headers,
            catch_response=True,
            name="Run Test",
        ) as response:
            task_result = ""
            if response.status_code != 200:
                failure_info = (
                    f"Test running failed by user: {self.username}. "
                    f"Response: {response.text}. Status code: {response.status_code}."
                )
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                task_result = failure_info
            else:
                success_info = f"Test successfully run by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                task_result = success_info
            Logger.add_response(response, task_result)

    @task
    def delete_test(self):
        """Delete test case by ID."""
        if not self.test_id:
            Logger.log_message("Cannot delete test: test_id is not set", LogType.ERROR)
            return

        Logger.add_request("Delete Test", f"/api/tests/{self.test_id}", "DELETE")
        with self.client.delete(
            url=f"/api/tests/{self.test_id}", headers=self.headers, catch_response=True, name="Delete Test Case by ID"
        ) as response:
            task_result = ""
            if response.status_code != 200:
                failure_info = (
                    f"Test deleting failed by user: {self.username}. "
                    f"Response: {response.text}. Status code: {response.status_code}."
                )
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                task_result = failure_info
            else:
                success_info = f"Test successfully deleted by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                task_result = success_info
            Logger.add_response(response, task_result)

    @task
    def exit_task_execution(self):
        """End task sequence."""
        self.interrupt()
