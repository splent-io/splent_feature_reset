from splent_framework.hooks.template_hooks import register_template_hook
from flask import render_template, url_for


def inject_reset_link():
    return render_template("hooks/reset_link.html")


register_template_hook("auth.login.form_footer", inject_reset_link)
register_template_hook("auth.signup.form_footer", inject_reset_link)


# ── Script hooks ─────────────────────────────────────────────────────────────


def reset_scripts():
    return (
        '<script src="'
        + url_for("reset.assets", subfolder="dist", filename="reset.bundle.js")
        + '"></script>'
    )


register_template_hook("layout.scripts", reset_scripts)
