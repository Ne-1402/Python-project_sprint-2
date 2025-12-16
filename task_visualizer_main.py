from __future__ import annotations
from pathlib import Path
import argparse
from typing import List, Dict
import matplotlib.pyplot as plt
from task_utils import load_tasks_from_csv, save_employee_summary, incomplete_tasks, completed_tasks, compute_percentage
from task_class import Task
import sys

def parse_args():
    p = argparse.ArgumentParser(description="Employee Task Completion Visualizer")
    p.add_argument("--tasks", "-t", default="tasks.csv")
    p.add_argument("--out", "-o", default="employee_summary.json")
    p.add_argument("--show", action="store_true")
    return p.parse_args()

def make_plots(report: Dict[str, Dict[str, float]], show: bool = False) -> None:
    names = list(report.keys())
    percentages = [report[n]['completion_percentage'] for n in names]

    plt.figure(figsize=(8, 4))
    plt.bar(names, percentages)
    plt.title('Completion Percentage per Employee')
    plt.ylabel('Completion %')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig('completion_bar.png')
    if show: plt.show()
    plt.close()

    total_completed = sum(report[n]['completed_tasks'] for n in names)
    total_tasks = sum(report[n]['total_tasks'] for n in names)
    total_incomplete = total_tasks - total_completed

    labels = ['Completed', 'Incomplete']
    sizes = [total_completed, total_incomplete]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Task Status Distribution (team)')
    plt.tight_layout()
    plt.savefig('task_status_pie.png')
    if show: plt.show()
    plt.close()

def summarize_and_save(tasks: List[Task], out_path: str):
    report = Task.team_report(tasks)
    save_employee_summary(report, out_path)
    return report

def main():
    args = parse_args()
    try:
        tasks = load_tasks_from_csv(args.tasks)
    except Exception as e:
        print("Error loading tasks:", e, file=sys.stderr)
        sys.exit(1)

    incomps = incomplete_tasks(tasks)
    comps = completed_tasks(tasks)

    total_completed = len(comps)
    total = len(tasks)
    overall_pct = compute_percentage(total_completed, total)

    print(f"Loaded {total} tasks. Completed: {total_completed}. Overall completion: {overall_pct:.2f}%")

    report = summarize_and_save(tasks, args.out)
    make_plots(report, show=args.show)

if __name__ == "__main__":
    main()
