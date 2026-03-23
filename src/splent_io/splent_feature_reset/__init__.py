from splent_framework.blueprints.base_blueprint import BaseBlueprint

reset_bp = BaseBlueprint("reset", __name__, template_folder="templates")


def init_feature(app):
    pass


def inject_context_vars(app):
    return {}
