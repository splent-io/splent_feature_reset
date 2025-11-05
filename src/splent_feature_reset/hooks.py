from splent_framework.hooks.template_hooks import register_template_hook
from flask import render_template


def inject_reset_link():
    return render_template("hooks/reset_link.html")

register_template_hook("auth.login.form_footer", inject_reset_link)
register_template_hook("auth.signup.form_footer", inject_reset_link)