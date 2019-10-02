"""
Task Distribution Excercise, by Adrian Fernandez

This solution contains ______ components, ...

Use case:
.......

"""
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Task:
    name: str
    task_point: int


@dataclass
class Employee:
    nickname: str
    task_point: int
    assigned_task_points: int = 0
    assigned_tasks: List[Task] = field(default_factory=list, repr=True)

    def assign_task(self, task: Task):
        self.assigned_tasks.append(task)
        self.assigned_task_points += task.task_point

    def capacity(self):
        return self.task_point - self.assigned_task_points


def distribute_tasks(employees: List[Employee], tasks: List[Task]) -> List:
    """ Finds the optimal distribution of tasks, given a group of employees"""
    tasks.sort(key=lambda x: x.task_point, reverse=True)
    for task in tasks:
        employee = max(employees, key=lambda x: x.capacity())
        if employee.capacity() >= task.task_point:
            employee.assign_task(task)

    return [asdict(employee) for employee in employees]


if __name__ == '__main__':
    employees_ls = [Employee('e1', 1),
                    Employee('e2', 2),
                    Employee('e3', 7)]

    tasks_ls = [Task('t_1', 4),
                Task('t_2', 1),
                Task('t_3', 2),
                Task('t_4', 3)]

    # Assign tasks to employees and display result
    result = distribute_tasks(employees_ls, tasks_ls)
    print(result)

    # Resutls can also be displayed as objects.repr
    print("**************")
    for employee in employees_ls:
        print(employee)
