from flask import jsonify, request
import models
import datetime

def get_all_lists():
    todo_lists = models.TodoList.get_all()
    return jsonify(models.TodoList.list_to_json(todo_lists))

def get_one_list(_id):
    todo_list = models.TodoList.get_one(_id)
    return jsonify(models.TodoList.to_json(todo_list))

def create_list():
    req = request.get_json()
    new_todo_list = models.TodoList(0, datetime.datetime.now(), req['title'])
    todo_list = models.TodoList.create(new_todo_list)
    return jsonify(models.TodoList.to_json(todo_list))

def update_list(_id):
    old_todo_list = models.TodoList.get_one(_id)
    req = request.get_json()
    updated_todo_list = models.TodoList(_id, old_todo_list.created_at, req['title'])
    todo_list = models.TodoList.update(updated_todo_list)
    return jsonify(models.TodoList.to_json(todo_list))

def delete_list(_id):
    response = models.TodoList.delete(_id)
    return jsonify(response)