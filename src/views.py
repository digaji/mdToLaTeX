from flask import Blueprint, render_template, redirect, request, url_for
from src.backend import generator, lexer, myParser

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def index():
    result = []

    def callback(string):
        result.append(string)

    if request.method == "POST":
        markdown = str(request.form.get("markdown")).replace("\r", "")

        try:
            md_lexer = lexer.Lexer(markdown)
            tokens = md_lexer.tokenize()
            md_parser = myParser.Parser(tokens)
            document = md_parser.parse()

            md_generator = generator.Generator(document, callback)
            md_generator.generate()
        except Exception as e:
            error_string = str(e)
            error_string += "\n\nPlease return to the homepage!"
            return render_template("result.html", result=error_string)

        latex = "".join(result)

        return render_template("result.html", result=latex)

    return render_template("index.html")
