from flask import current_app
from flask import render_template
from myflaskapp.app import bp
from mymodels.author import Author


@bp.route("/author/<author_name>")
def add_author(author_name):
    # Add author to database
    author = Author(name=author_name)
    current_app.session.add(author)
    current_app.session.commit()

    return f"Author {author_name} created, id={author.id}"


@bp.route("/authors")
def get_authors():
    authors = current_app.session.query(Author).all()

    return render_template(
        "authors.html", title="My author's list", authors=authors
    )
