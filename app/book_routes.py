from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, abort, make_response, request
from app.helper import validate_model


books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    try:
        new_book = Book.from_dict(request_body)

        db.session.add(new_book)
        db.session.commit()

        return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)
    
    except KeyError as error:
        abort(make_response(jsonify({"error message": f"missing required value: {error}"}), 400))


@books_bp.route("", methods=["GET"])
def read_all_books():

    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = [book.to_dict() for book in books]
    return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_model(Book, book_id)
    return jsonify(book.to_dict())


@books_bp.route("/<book_id>", methods=["PUT"])
def replace_book(book_id):
    book = validate_model(Book,book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book {book.id} successfully updated"))

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book {book.id} successfully deleted"))