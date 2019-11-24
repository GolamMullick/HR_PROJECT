from users.models import DepartmentModelPermission


def init_dmp(license):
    DepartmentModelPermission.load_on_migrate(license)
    print("department model permission worked!!")