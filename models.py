import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

class TodoItem:
    def __init__(self, _id, created_at, title, description):
        self.id = _id
        self.created_at = created_at
        self.title = title
        self.description = description

    def __del__(self):
        if self.db is not None and self.db.closed:
            self.db.close()
    
    @staticmethod
    def get_all():
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM todo_item")
                items = cur.fetchall()
                items_list = []
                for item in items:
                    items_list.append(TodoItem(item[0], item[1], item[2], item[3]))
                return items_list
    
    @staticmethod
    def get_one(_id):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM todo_item WHERE id = %s", (_id,))
                item = cur.fetchone()
                return TodoItem(item[0], item[1], item[2], item[3])

    def to_json(self):
        return {'id': self.id, 'created_at': self.created_at,
                'title': self.title, 'description': self.description}

    @staticmethod
    def list_to_json(list):
        json_list = []
        for item in list:
            json_list.append(item.to_json())

        return json_list