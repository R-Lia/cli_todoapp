import datetime

class Todo:
    def __init__(self, task, category, date_added=None, date_completed=None, status=0, todo_id=None):
        self.task=task
        self.category = category
        self.date_added = datetime.datetime.now().isoformat()
        self.date_completed = date_completed 
        self.status = status
        self.id = todo_id

    def __repr__(self) -> str:
        return f"({self.task}, {self.category}, {self.date_added}, {self.date_completed}, {self.status}, {self.id})"


