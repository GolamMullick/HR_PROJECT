from users.models import DepartmentRoleModelPermission


def init_drp(license):
    DepartmentRoleModelPermission.load_on_migrate(license)
    print("department role model permission worked!!")