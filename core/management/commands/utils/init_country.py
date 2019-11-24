import os
from core.models import Country


def init_country():
    project_directory = os.path.abspath(".")
    data_directory = os.path.join(project_directory, "core", "data")

    country_data_file = os.path.join(data_directory, "countries.json")
    Country.load_from_json(country_data_file)