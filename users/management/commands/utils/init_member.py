from users.models import Member


def init_member(license):
    Member.load_on_migrate(license)
    print("member worked!!")