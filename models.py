import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

class TodoItem:
    def __init__(self, _id, created_at, title, description, done, todo_list_id):
        self.id = _id
        self.created_at = created_at
        self.title = title
        self.description = description
        self.done = done
        self.todo_list_id = todo_list_id
    
    @staticmethod
    def get_all(list_id):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM todo_item WHERE todo_list_id = %s", (list_id,))
                items = cur.fetchall()
                items_list = []
                for item in items:
                    items_list.append(TodoItem(item[0], item[1], item[2], item[3], item[4], item[5]))
                return items_list
    
    @staticmethod
    def get_one(_id, list_id):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM todo_item WHERE id = %s AND todo_list_id = %s", (_id, list_id,))
                item = cur.fetchone()
                return TodoItem(item[0], item[1], item[2], item[3], item[4], item[5])

    @staticmethod
    def create(new_item):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("INSERT INTO todo_item(created_at, title, description, done, todo_list_id) VALUES (%s, %s, %s, %s, %s) RETURNING id"
                            , (new_item.created_at, new_item.title, new_item.description, new_item.done, new_item.todo_list_id))
                con.commit()
                last_row_id = cur.fetchone()[0]
                return TodoItem(
                    last_row_id,
                    new_item.created_at,
                    new_item.title,
                    new_item.description,
                    new_item.done,
                    new_item.todo_list_id
                )
    
    @staticmethod
    def update(updated_item):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("UPDATE todo_item SET title = %s, description = %s, done = %s WHERE id = %s AND todo_list_id = %s"
                            , (updated_item.title, updated_item.description, updated_item.done, updated_item.id, updated_item.todo_list_id))
                con.commit()
                return TodoItem(
                    updated_item.id,
                    updated_item.created_at,
                    updated_item.title,
                    updated_item.description,
                    updated_item.done,
                    updated_item.todo_list_id
                )

    @staticmethod
    def delete(_id, list_id):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("DELETE FROM todo_item WHERE id = %s AND todo_list_id = %s", (_id, list_id,))
                return f"Item with id: {_id} deleted from list with id: {list_id}."

    def to_json(self):
        return {'id': self.id, 'created_at': self.created_at,
                'title': self.title, 'description': self.description, 'todo_list_id': self.todo_list_id}

    @staticmethod
    def list_to_json(list):
        json_list = []
        for item in list:
            json_list.append(item.to_json())

        return json_list
    
class TodoList:
    def __init__(self, _id, created_at, title):
        self.id = _id
        self.created_at = created_at
        self.title = title

    @staticmethod
    def get_one(_id):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM todo_list WHERE id = %s", (_id,))
                todo_list = cur.fetchone()
                return TodoList(todo_list[0], todo_list[1], todo_list[2])
    
    @staticmethod
    def get_all():
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("SELECT * FROM todo_list")
                todo_lists = cur.fetchall()
                todo_lists_list = []
                for todo_list in todo_lists:
                    todo_lists_list.append(TodoList(todo_list[0], todo_list[1], todo_list[2]))
                return todo_lists_list
    
    @staticmethod
    def create(new_list):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("INSERT INTO todo_list(created_at, title) VALUES (%s, %s) RETURNING id", 
                            (new_list.created_at, new_list.title,))
                con.commit()
                last_row_id = cur.fetchone()[0]
                return TodoList(
                    last_row_id,
                    new_list.created_at,
                    new_list.title
                )
    
    @staticmethod
    def update(updated_list):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("UPDATE todo_list SET title = %s WHERE id = %s", 
                            (updated_list.title, updated_list.id,))
                con.commit()
                return TodoList(
                    updated_list.id,
                    updated_list.created_at,
                    updated_list.title
                )
            
    @staticmethod
    def delete(_id):
        with psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, dbname=DBNAME) as con:
            with con.cursor() as cur:
                cur.execute("DELETE FROM todo_list WHERE id = %s", (_id,))
                return (f"list with id: {_id} deleted")
    
    def to_json(self):
        return {'id': self.id, 'created_at': self.created_at, 'title': self.title}

    @staticmethod
    def list_to_json(list):
        json_list = []
        for item in list:
            json_list.append(item.to_json())

        return json_list