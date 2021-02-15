import os

# This settings will override settings in static.py
STATIC_ROOT = 'test_folder'


class TestingConfiguration(object):
    """Test class."""

    def __init__(self, testing_dir):
        """Public constructor."""
        self.test_path = os.path.join(testing_dir, STATIC_ROOT)

    def get_path(self):
        """Returns path."""
        return self.test_path
