from users.models import Apps


def init_apps(license):
    Apps.load_on_migrate(license)
    print("apps worked!!")