import bisect
from itertools import permutations, repeat, combinations

# def match_single_options(tasks, employees, emp_names):
#     """ Match all employee's with a single task-match, remove task from tasks.
    
#     This is an easy way of restricting options and improving performance. 
#     Matching attempts start from lowest to highest, requires sorted lists for
#     employees_tp and tasks_tp. 

#     There is 3 options:
#     - No match: employee capacity is not large enough, drop this employee
#     - Single match: allocate this task to employee, remove both from their
#         respective lists
#     - More than 1 match: given employee could take more than 1 task

#     If all employees had either a single match or no match, this is the solution.

#     Use:
#         tasks = [1,2,3,4]
#         emp_tp = [1,2,7]
#         emp_names = ["A", "B", "C"]
#         match_single_options(tasks, emp_tp, emp_names)
#     """
#     task_assignment = {}
#     for e_i in range(len(employees)):
#         emp = employees[e_i]
#         print("#", emp, tasks)
#         index = bisect.bisect(tasks, emp)
#         if index == 0 or index >= len(tasks):
#             break
#         single_task = tasks[index-1]
#         if single_task <= emp and tasks[index] > emp:
#             print("Single Match", single_task, "=>", emp)
#             task_assignment[emp_names[e_i]] = single_task
#             tasks.remove(single_task)
#     print(task_assignment)    
        


def gen_combinations(tasks):
    max_val = sum(tasks)
    combs = []
    for r in range(1, len(tasks)):
        combs += [x for x in combinations(tasks, r) if sum(x) <= max_val]
    return list(set(combs))

def sum_pairs(combs, r, c):
    return sum(combs[r]) + sum(combs[c])

def allocate_tasks(task_combination):
    # TODO do this transformation when creating the output (?)
    tc_ls = list(task_combination[0]) + list(task_combination[1])
    tc_sums = [sum(comb) for comb in task_combination]
    # vars for tracking
    empl_ls = [[] for i in employees]
    empl_assigned = [0 for e in employees]
#     print(empl_ls, empl_assigned)
    remaining_tp = employees.copy()
    tasks_remaining = tasks.copy()
    e_i = 0
    for t_tc in tc_ls:
        count = 0
    #     for e in range(len(employees)):
        while count <= len(employees):
#             print("#", e_i, employees[e_i], ">", remaining_tp, t_tc)
            if remaining_tp[e_i] >= t_tc:
                empl_ls[e_i].append(t_tc)
                remaining_tp[e_i] -= t_tc
                print(tasks_remaining, t_tc)
                t_i = tasks_remaining.index(t_tc)
                tasks_remaining[t_i] = 0
                print(tasks_remaining, t_tc)
                print("---")
                e_i += 1
                if e_i == len(employees):
                    e_i = 0
                break
            e_i += 1
            count += 1
            if e_i == len(employees):
                e_i = 0
    print(sum(tasks), tasks)
    print(sum(tasks_remaining), tasks_remaining)
    return empl_ls


def find_combinations(combs, tasks):
    #**** TODO if there is no perfect match, reduce target and start over
#     print("combs", combs)
#     print("tasks", sum(tasks), tasks)
    row, col = 0, len(combs)-1
    tp_target = min(sum(tasks), sum(employees))
    solutions = []

    while row < len(combs) and col >= 0:
        comb_value = sum_pairs(combs, row, col)
        print("#", row, col, "->", comb_value, tp_target)
        tp_difference = comb_value - tp_target

        if tp_difference == 0:
            print("Bingo!", sum_pairs(combs, row, col), "->", combs[row], combs[col])
#             TODO Verify solution, if satisfies requirements, return and stop this.
            solutions.append((combs[row], combs[col]))
            col-=1
            
        if tp_difference < 0:
            row+=1
        elif tp_difference > 0:
            col-=1

    return solutions


"""
    Run Code
"""
# tasks = [3,3,3,4,4,5]
# employees = [7,8,9]

# tasks = [2,2,2,2,2]
# employees = [1,4,4,6]
tasks = [6,4,2,3,5]
tasks_name = ["T1", "T2", "T3", "T4", "T5"]
employees = [3,5,7]

# tasks = [2,2,3,3]
# employees = [1,4,6]
emp_names = ["A", "B", "C"]
# tasks = [1,2,2,3,3,4,4]
# employees = [3,5,7,9] # TODO sort decending (?)
# emp_names = ["A", "B", "C", "D"]
# emp_names = ["A", "B", "C"]

# Create dict to map tasks after sorting
tasks_dict = {}
for i in range(len(tasks)):
    tasks_dict[tasks_name[i]] = tasks[i]
tasks.sort()

# Generate possible combinations of tasks, given constraints
combs = gen_combinations(tasks)
combs.sort(key=lambda x: sum(x))
# combs_sum2 = [sum(c) for c in combs]
# print(combs)
# print(combs_sum2)

solutions = find_combinations(combs, tasks)