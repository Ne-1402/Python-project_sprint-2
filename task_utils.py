from __future__ import annotations
import csv
from typing import List, Callable, Iterable, Any, Dict
from functools import wraps
from pathlib import Path
import json
from task_class import Task

def validate_task_update(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'completed' in kwargs:
            candidate = kwargs['completed']
            if not isinstance(candidate, bool):
                raise TypeError("completed must be boolean")
        else:
            if len(args) >= 2:
                candidate = args[1]
                if not isinstance(candidate, bool):
                    raise TypeError("completed must be boolean")
        return func(*args, **kwargs)
    return wrapper

def load_tasks_from_csv(path: str | Path) -> List[Task]:
    tasks = []
    path = Path(path)
    with path.open(newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            emp_name = row.get('emp_name', '').strip()
            description = row.get('description', '').strip()
            completed_raw = row.get('completed', '').strip().lower()
            completed = completed_raw in ('1', 'true', 'yes', 'y', 't')
            deadline = row.get('deadline') or None
            created_at = row.get('created_at') or None
            if not emp_name:
                continue
            tasks.append(Task(emp_name=emp_name, description=description,
                              completed=completed, deadline=deadline, created_at=created_at))
    return tasks

def save_employee_summary(report: Dict[str, Any], out_path: str | Path) -> None:
    p = Path(out_path)
    with p.open('w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=2)

compute_percentage = lambda completed, total: (completed / total * 100.0) if total > 0 else 0.0

def incomplete_tasks(tasks: Iterable[Task]) -> List[Task]:
    return [t for t in tasks if not t.completed]

def completed_tasks(tasks: Iterable[Task]) -> List[Task]:
    return [t for t in tasks if t.completed]
