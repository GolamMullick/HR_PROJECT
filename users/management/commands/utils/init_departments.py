import os
from users.models import Department


def init_department(license):
    project_directory = os.path.abspath(".")
    data_directory = os.path.join(project_directory, "users", "data")

    department_data_file = os.path.join(data_directory, "departments.json")
    Department.load_from_json(department_data_file, license)
    print("dept worked!!")