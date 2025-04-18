from flask import Flask

from controllers.todo_items_controller import (get_all_items,
                                                get_one_item,
                                                create_item,
                                                update_item,
                                                delete_item)

from controllers.todo_lists_controller import (get_all_lists,
                                               get_one_list,
                                               create_list,
                                               update_list,
                                               delete_list)

app = Flask(__name__)

app.add_url_rule('/api/<list_id>/todo_item', view_func=get_all_items)

app.add_url_rule('/api/<list_id>/todo_item/<_id>', view_func=get_one_item, methods=['GET'])

app.add_url_rule('/api/todo_item', view_func=create_item, methods=['POST'])

app.add_url_rule('/api/todo_item/<_id>', view_func=update_item, methods=['PUT'])

app.add_url_rule('/api/<list_id>/todo_item/<_id>', view_func=delete_item, methods=['DELETE'])

app.add_url_rule('/api/todo_list', view_func=get_all_lists)

app.add_url_rule('/api/todo_list/<_id>', view_func=get_one_list, methods=['GET'])

app.add_url_rule('/api/todo_list', view_func=create_list, methods = ['POST'])

app.add_url_rule('/api/todo_list/<_id>', view_func=update_list, methods = ['PUT'])

app.add_url_rule('/api/todo_list/<_id>', view_func=delete_list, methods = ['DELETE'])

if __name__ == '__main__':
    app.run()
