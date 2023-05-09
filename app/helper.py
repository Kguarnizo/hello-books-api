from app import db
from app.models.book import Book
from flask import Blueprint,abort, make_response, request


def validate_model(cls, model_id):
    try:
        book_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    
    return model