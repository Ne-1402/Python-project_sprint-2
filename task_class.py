from __future__ import annotations
from typing import List, Dict, Any
from datetime import datetime
import json

class Task:
    def __init__(self, emp_name: str, description: str, completed: bool = False,
                 deadline: str | None = None, created_at: str | None = None) -> None:
        self.emp_name = emp_name
        self.description = description
        self.completed = bool(completed)
        self.deadline = deadline
        self.created_at = created_at or datetime.utcnow().isoformat()

    def assign_task(self, emp_name: str) -> None:
        if not emp_name or not isinstance(emp_name, str):
            raise ValueError("emp_name must be a non-empty string")
        self.emp_name = emp_name

    def update_status(self, completed: bool) -> None:
        if not isinstance(completed, bool):
            raise TypeError("completed must be boolean")
        self.completed = completed

    def completion_rate(self) -> float:
        return 1.0 if self.completed else 0.0

    @staticmethod
    def team_report(tasks: List["Task"]) -> Dict[str, Any]:
        report = {}
        for t in tasks:
            if t.emp_name not in report:
                report[t.emp_name] = {"total_tasks": 0, "completed_tasks": 0}
            report[t.emp_name]["total_tasks"] += 1
            if t.completed:
                report[t.emp_name]["completed_tasks"] += 1
        for emp, stats in report.items():
            total = stats["total_tasks"]
            comp = stats["completed_tasks"]
            percent = (comp / total * 100.0) if total > 0 else 0.0
            stats["completion_percentage"] = round(percent, 2)
        return report

    def to_dict(self) -> Dict[str, Any]:
        return {
            "emp_name": self.emp_name,
            "description": self.description,
            "completed": self.completed,
            "deadline": self.deadline,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Task":
        return cls(
            emp_name=d["emp_name"],
            description=d["description"],
            completed=bool(d.get("completed", False)),
            deadline=d.get("deadline"),
            created_at=d.get("created_at"),
        )
