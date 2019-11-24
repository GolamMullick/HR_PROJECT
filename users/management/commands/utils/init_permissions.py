import os
from users.models import Permission


def init_permission(license_id):
    project_directory = os.path.abspath(".")
    data_directory = os.path.join(project_directory, "users", "data")

    permission_data_file = os.path.join(data_directory, "permissions.json")
    Permission.load_from_json(permission_data_file, license_id)
    print("permission worked!!")