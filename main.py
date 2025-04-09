from flask import Flask

from controllers.todo_items_controller import (get_all_items,
                                                get_one_item,
                                                create_item,
                                                update_item,
                                                delete_item)

app = Flask(__name__)

app.add_url_rule('/api/todo_item', view_func=get_all_items)

app.add_url_rule('/api/todo_item/<_id>', view_func=get_one_item, methods=['GET'])

app.add_url_rule('/api/todo_item', view_func=create_item, methods=['POST'])

app.add_url_rule('/api/todo_item/<_id>', view_func=update_item, methods=['PUT'])

app.add_url_rule('/api/todo_item/<_id>', view_func=delete_item, methods=['DELETE'])

if __name__ == '__main__':
    app.run()
