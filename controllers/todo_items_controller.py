from flask import jsonify, request
import models

def get_all_items():
    items = models.TodoItem.get_all()
    return jsonify(models.TodoItem.list_to_json(items))