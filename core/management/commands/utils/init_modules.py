import os
from erplicense.models import Modules


def init_modules():
    project_directory = os.path.abspath(".")
    data_directory = os.path.join(project_directory, "core", "data")

    module_data_file = os.path.join(data_directory, "modules.json")
    Modules.load_from_json(module_data_file)