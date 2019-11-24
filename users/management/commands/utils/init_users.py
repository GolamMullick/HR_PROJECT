from users.models import CompanyUsers


def init_users(license):
    CompanyUsers.load_on_migrate(license)
    print("users worked!!")