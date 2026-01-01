"""Test case data class."""


class NewTest:
    """Test case data storage."""

    def __init__(self):
        self.test_data = {}

    def set_test_id(self, id):
        self.test_data["id"] = id

    def set_test_name(self, name):
        self.test_data["name"] = name

    def set_test_desc(self, description):
        self.test_data["description"] = description

    def set_test_author(self, author):
        self.test_data["author"] = author

    def set_test_status(self, status):
        self.test_data["status"] = status

    def set_test_executor(self, executor):
        self.test_data["executor"] = executor

    def get_test_id(self):
        return self.test_data["id"]

    def get_test_name(self):
        return self.test_data["name"]

    def get_test_desc(self):
        return self.test_data["description"]

    def get_test_author(self):
        return self.test_data["author"]

    def get_test_status(self):
        return self.test_data["status"]

    def get_test_executor(self):
        return self.test_data["executor"]
