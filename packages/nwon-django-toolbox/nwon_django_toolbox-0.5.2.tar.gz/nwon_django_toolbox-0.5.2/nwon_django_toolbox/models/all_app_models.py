from django.apps import apps


def all_app_models(app_name: str = "nwon"):
    return apps.get_app_config(app_name).get_models()
