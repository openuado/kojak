import gettext
import os

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Report:
    def __init__(self):
        """Initialize a report object."""
        template_dir = "{basedir}/kojak/templates".format(basedir=BASE_DIR)
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            extensions=["jinja2.ext.i18n"],
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.env.install_gettext_callables(
            gettext=gettext.gettext, ngettext=gettext.ngettext, newstyle=True
        )

    def rendering(self, template, analyze):
        template = self.env.get_template(template)
        print(template.render(analyze=analyze))
