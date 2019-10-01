"""
Task Distribution Excercise, by Adrian Fernandez

This solution contains ______ components, ...

Use case:
.......

"""
from dataclasses import dataclass
from typing import List

@dataclass
class Task:
    name: str
    task_point: int

@dataclass
class Employee:
    nickname: str
    task_point: int
    assigned_tasks = []
    assigned_task_points: int = 0


def distrbute_tasks(employees: List[Employee], tasks: List[Task]):
    """ Finds the optimal distribution of tasks, given a group of employees"""
    return (employees, tasks)


if __name__ == '__main__':
    employees_ls = []
    employees_ls.append(Employee('e1', 1))
    employees_ls.append(Employee('e2', 2))
    employees_ls.append(Employee('e3', 3))

    tasks_ls = []
    tasks_ls.append(Task('t_1', 1))
    tasks_ls.append(Task('t_2', 2))
    tasks_ls.append(Task('t_3', 3))

    print(distrbute_tasks(employees_ls, employees_ls))
