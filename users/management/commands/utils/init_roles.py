import os
from users.models import Role


def init_role(license):
    project_directory = os.path.abspath(".")
    data_directory = os.path.join(project_directory, "users", "data")

    role_data_file = os.path.join(data_directory, "roles.json")
    Role.load_from_json(role_data_file, license)
    print("roles worked!!")