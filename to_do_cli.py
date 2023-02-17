import typer
from rich.console import Console
from rich.table import Table

from model import Todo
import database

console = Console()

app = typer.Typer()

@app.command(short_help="adds an item")
def add(task:str, category:str):
    typer.echo("adding {}, {}".format(task,category))
    todo = Todo(task,category)
    database.insert_todo(todo)
    show()

@app.command(short_help="deletes an item")
def delete(todo_id:int):
    typer.echo("deleting id {} task".format(todo_id))
    database.delete_todo(todo_id)
    show()

@app.command(short_help="update an item")
def update(todo_id:int,task:str=None, category:str=None):
    typer.echo("updating {}, {}".format(task,category))
    database.update_todo(todo_id,task,category)
    show()

@app.command()
def show():
    tasks = database.get_todos()
    console.print("[bold magenta] DISPLAY TODO [/bold magenta]")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Status", min_width=12, justify="right")
    
    def get_category_color(status):
        COLORS = {'0': 'cyan', '1': 'orange', '2': 'green'}
        return COLORS[status]

    for idx, task in enumerate(tasks):
        c = get_category_color(str(task.status))
        status = False
        if task.status == 0:
            is_done_str = "To start"
        elif task.status == 1:
            is_done_str = "In progress"
        else :
            is_done_str = "Done"
        table.add_row(f'[{c}]{task.id}[/{c}]',f'[{c}]{task.task}[/{c}]', f'[{c}]{task.category}[/{c}]',f'[{c}]{is_done_str}[/{c}]')
    console.print(table)

@app.command()
def complete(position: int):
    typer.echo(f"complete {position}")
    database.complete_todo(position)
    show()

if __name__ == "__main__":
    app()
