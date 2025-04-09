import psycopg2
from dotenv import load_dotenv
import datetime
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
    def __init__(self, _id, created_at, title, description, done):
        self.id = _id
        self.created_at = created_at
        self.title = title
        self.description = description
        self.done = done
    
    @staticmethod
    def get_all():
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM todo_item")
                items = cur.fetchall()
                items_list = []
                for item in items:
                    items_list.append(TodoItem(item[0], item[1], item[2], item[3], item[4]))
                return items_list
    
    @staticmethod
    def get_one(_id):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM todo_item WHERE id = %s", (_id,))
                item = cur.fetchone()
                return TodoItem(item[0], item[1], item[2], item[3], item[4])

    @staticmethod
    def create(new_item):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("INSERT INTO todo_item(created_at, title, description, done) VALUES (%s, %s, %s, %s) RETURNING id"
                            , (new_item.created_at, new_item.title, new_item.description, new_item.done))
                con.commit()
                last_row_id = cur.fetchone()[0]
                return TodoItem(
                    last_row_id,
                    new_item.created_at,
                    new_item.title,
                    new_item.description,
                    new_item.done
                )
    
    @staticmethod
    def update(updated_item):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("UPDATE todo_item SET title= %s, description = %s, done = %s WHERE id = %s"
                            , (updated_item.title, updated_item.description, updated_item.done, updated_item.id))
                con.commit()
                return TodoItem(
                    updated_item.id,
                    updated_item.created_at,
                    updated_item.title,
                    updated_item.description,
                    updated_item.done
                )

    @staticmethod
    def delete(_id):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("DELETE FROM todo_item WHERE id = %s", (_id,))
                return f"Item with id:{_id} deleted."

    def to_json(self):
        return {'id': self.id, 'created_at': self.created_at,
                'title': self.title, 'description': self.description}

    @staticmethod
    def list_to_json(list):
        json_list = []
        for item in list:
            json_list.append(item.to_json())

        return json_list