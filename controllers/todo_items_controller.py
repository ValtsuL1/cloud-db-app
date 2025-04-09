from flask import jsonify, request
import models
import datetime

def get_all_items():
    items = models.TodoItem.get_all()
    return jsonify(models.TodoItem.list_to_json(items))

def get_one_item(_id):
    item = models.TodoItem.get_one(_id)
    return jsonify(models.TodoItem.to_json(item))

def create_item():
    req = request.get_json()
    new_item = models.TodoItem(0, datetime.datetime.now(), req['title'], req['description'], False)
    item = models.TodoItem.create(new_item)
    return jsonify(models.TodoItem.to_json(item))

def update_item(_id):
    old_item = models.TodoItem.get_one(_id)
    req = request.get_json()
    updated_item = models.TodoItem(_id, old_item.created_at, req['title'], req['description'], req['done'])
    item = models.TodoItem.update(updated_item)
    return jsonify(models.TodoItem.to_json(item))

def delete_item(_id):
    response = models.TodoItem.delete(_id)
    return jsonify(response)