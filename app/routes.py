from flask import current_app as app
from flask import render_template
import markdown
import markdown.extensions.fenced_code
from pygments.formatters.html import HtmlFormatter
from markupsafe import Markup


@app.route("/")
def index():

        return render_template("index.html")