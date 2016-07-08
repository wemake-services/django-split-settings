import os.path

# This settings will override settings in static.py
STATIC_ROOT = 'test_folder'


class TestingConfiguration(object):
    def __init__(self, testing_dir):
        self.test_path = os.path.join(testing_dir, STATIC_ROOT)

    def get_path(self):
        return self.test_path
