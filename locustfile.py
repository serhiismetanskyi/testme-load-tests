"""Locust load tests main file."""

from locust import events

from tests.register_user import RegisteredHttpUser
from tests.test_lists import Lists
from tests.test_stats import Stats
from tests.test_tests import Tests
from utils.logger import Logger, LogType
from utils.users_loader import UsersLoader


@events.test_start.add_listener
def on_test_start(**kwargs):
    """Init logger and load users."""
    try:
        parsed_options = kwargs.get("environment", {}).parsed_options
        if parsed_options and hasattr(parsed_options, "logfile") and parsed_options.logfile:
            Logger.init_logger(__name__, parsed_options.logfile)
    except (AttributeError, KeyError):
        pass

    try:
        UsersLoader.load_users()
        Logger.log_message("......... Initiating Load Test .......")
    except (FileNotFoundError, ValueError) as e:
        error_msg = f"Failed to load users: {str(e)}"
        Logger.log_message(error_msg, LogType.ERROR)
        raise


@events.test_stop.add_listener
def on_test_stop(**kwargs):
    """Test completion handler."""
    Logger.log_message("........ Load Test Completed ........")


class TestsGroup(RegisteredHttpUser):
    """CRUD operations group. Weight 4."""

    weight = 4
    tasks = [Tests]


class ListsGroup(RegisteredHttpUser):
    """Test lists group. Weight 2."""

    weight = 2
    tasks = [Lists]


class StatsGroup(RegisteredHttpUser):
    """Statistics group. Weight 1."""

    weight = 1
    tasks = [Stats]
