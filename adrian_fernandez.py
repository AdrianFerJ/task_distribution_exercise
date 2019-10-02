"""
Task Distribution Excercise, by Adrian Fernandez

This solution contains ______ components, ...

Use case:
.......

"""
from dataclasses import dataclass
from typing import List
from operator import attrgetter

@dataclass
class Task:
    name: str
    task_point: int

@dataclass
class Employee:
    nickname: str
    task_point: int
    # capacity: int = False
    assigned_tasks = []
    assigned_task_points: int = 0

    def assign_task(self, task: Task):
        self.assigned_tasks.append(task)
        self.assigned_task_points += task.task_point
        if self.capacity == False:
            self.capacity = self.task_point
        self.capacity -= task.task_point
    
    # def capacity(self):
    #     return self.task_point - self.assigned_task_points


def distrbute_tasks(employees: List[Employee], tasks: List[Task]):
    """ Finds the optimal distribution of tasks, given a group of employees"""
    tasks.sort(key = lambda x: x.task_point, reverse=True)
    for task in tasks:
        employee = max(employees, key=attrgetter('task_point'))
        # employee = max(employees, key = lambda x: x.capacity())
        if employee.capacity >= task.task_point:
            employee.assign_task(task)

    return employees
    



if __name__ == '__main__':
    employees_ls = []
    employees_ls.append(Employee('e1', 1))
    employees_ls.append(Employee('e2', 2))
    employees_ls.append(Employee('e3', 6))

    tasks_ls = []
    tasks_ls.append(Task('t_4', 4))
    tasks_ls.append(Task('t_1', 1))
    tasks_ls.append(Task('t_2', 2))
    tasks_ls.append(Task('t_3', 3))

    # Assign tasks to employees and display result
    result = distrbute_tasks(employees_ls, tasks_ls)
    for r in result:
        print(r)
        #TODO print(r.show_all())
