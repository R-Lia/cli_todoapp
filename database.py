import sqlite3
import datetime
from model import Todo


conn = sqlite3.connect('todo.db')
c = conn.cursor()

def create_table():
    c.execute("""
    CREATE TABLE IF NOT EXISTS todos (
    task text,
    category text,
    date_added text,
    date_completed text,
    status integer,
    id integer
    )""")

create_table()

def insert_todo(todo):
    c.execute('select count(*) FROM todos')
    count = c.fetchone()[0]
    todo.id = count if count else 0
    with conn:
        # the :variable_name is specific to sql. It is a bind variable that prevent sql injection
        c.execute('INSERT INTO todos VALUES (:task, :category, :date_added, :date_completed, :status, :id)',
        {'task': todo.task, 'category': todo.category, 'date_added': todo.date_added,
         'date_completed': todo.date_completed, 'status': todo.status, 'id': todo.id })


def get_todos():
    c.execute('SELECT * FROM todos')
    # fetchall returns a lits of tuples
    results = c.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(*result))
    return todos


def delete_todo(todo_id):
    c.execute('select count(*) FROM todos')
    count = c.fetchone()[0]
    
    with conn:
        c.execute("DELETE from todos WHERE id=:id", {"id": todo_id})
        for pos in range(todo_id+1, count):
            change_id(pos, pos-1, False)


def change_id(old_id: int, new_id: int, commit=True):
    c.execute('UPDATE todos SET id = :id_new WHERE id = :id_old',
                {'id_old': old_id, 'id_new': new_id})
    if commit:
        conn.commit()


def update_todo(todo_id: int, task: str, category: str):
    with conn:
        if task is not None and category is not None:
            c.execute('UPDATE todos SET task = :task, category = :category WHERE id = :id',
                      {'id': todo_id, 'task': task, 'category': category})
        elif task is not None:
            c.execute('UPDATE todos SET task = :task WHERE id = :id',
                      {'id': todo_id, 'task': task})
        elif category is not None:
            c.execute('UPDATE todos SET category = :category WHERE id = :id',
                      {'id': todo_id, 'category': category})


def complete_todo(todo_id: int):
    with conn:
        c.execute('UPDATE todos SET status = 2, date_completed = :date_completed WHERE id = :id',
                  {'id': todo_id, 'date_completed': datetime.datetime.now().isoformat()})
