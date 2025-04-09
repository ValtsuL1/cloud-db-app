from flask import Flask

from controllers.todo_items_controller import get_all_items

app = Flask(__name__)

app.add_url_rule('/api/todo_item', view_func=get_all_items)

if __name__ == '__main__':
    app.run()
