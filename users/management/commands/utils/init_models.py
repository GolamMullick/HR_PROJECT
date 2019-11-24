from users.models import Model


def init_models(license):
    Model.load_on_migrate(license)
    print("models worked!!")