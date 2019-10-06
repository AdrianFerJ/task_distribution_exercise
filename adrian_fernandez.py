from itertools import permutations, repeat, combinations
from collections import Counter

def gen_combinations(tasks):
    max_val = sum(tasks)
    combs = []
    for r in range(1, len(tasks)):
        combs += [x for x in combinations(tasks, r) if sum(x) <= max_val]
    return list(set(combs))

def sum_pairs(combs, r, c):
    return sum(combs[r]) + sum(combs[c])

def validate_solution(solution, task_counter):
    sol_counter = Counter(solution)
    for item in solution:
        if sol_counter[item] > task_counter[item]:
            return False
    return True      

def allocate_tasks(comb_tasks, target, task_counter):
    if not validate_solution(comb_tasks, task_counter):
        return False

    # Keep track of assignments
    empl_assignments = [[] for i in employees]
    empl_remaining = employees.copy()
    total_assignments = 0
    tasks_remaining = tasks.copy()
    # print("Allocate tasks, comb_tasks:", comb_tasks)
#     empl_assigned = [0 for e in employees]
#     print(empl_assignments, empl_remaining)
    e_i = 0
    for tc_ix in range(len(comb_tasks)):
        while e_i <= len(employees):
#             print("$$", comb_tasks[tc_ix], "<?>", max(empl_remaining))
            if comb_tasks[tc_ix] > max(empl_remaining):
                break
            t_tc = comb_tasks[tc_ix]
#             print("# EMP", e_i, employees[e_i], "Remaining:", empl_remaining, "Task", t_tc)
            if empl_remaining[e_i] >= t_tc:
                empl_assignments[e_i].append(t_tc)
                empl_remaining[e_i] -= t_tc
                tasks_remaining[tc_ix] = 0
                total_assignments += t_tc
                e_i += 1
                if e_i == len(employees):
                    e_i = 0
                break
            e_i += 1
            if e_i == len(employees):
                e_i = 0
    if target == total_assignments:
        print("Target!", total_assignments, empl_assignments)
        return empl_assignments
    else:
        return False

def find_combinations(combs, tasks, lower_target=0):
    # if there is no perfect match, reduce target and start over

    # Task task_point counter, for validaiton
    task_counter = Counter(tasks)
    row, col = 0, len(combs)-1
    temp = min(sum(tasks), sum(employees))
    tp_target = temp - lower_target
    print("Target task_point:", tp_target, lower_target)

    while row < len(combs) and col >= 0:
        comb_value = sum_pairs(combs, row, col)
        tp_difference = comb_value - tp_target
        # print("#", row, col, "->", comb_value, tp_target)

        # If combination matches target taskpoint 
        if tp_difference == 0:
            comb_tasks = list(combs[row]) + list(combs[col])
            # print("Bingo!", comb_value, "->", comb_tasks)            
            employees_tasks = allocate_tasks(comb_tasks, tp_target, task_counter)
            if employees_tasks:
                print("!!!!! SOLUTION ", employees_tasks)
                # solutions.append(employees_tasks)       
                return employees_tasks     
            col-=1

        # Move to a higher combination
        if tp_difference < 0:
            row+=1
        # Move to a lower combination
        elif tp_difference > 0:
            col-=1

    # If not Solution found
    lower_target += 1
    print("*** No Solution, lower task_point target:", lower_target)
    solution =  find_combinations(combs, tasks, lower_target)
    print("solutions >>>", len(solution))
    return solution


"""
    Run Code
"""
if __name__ == '__main__':
    tasks = [6,4,2,3,5]
    tasks_name = ["T1", "T2", "T3", "T4", "T5"]
    employees = [3,5,7]
    emp_names = ["A", "B", "C"]
    # tasks = [3,3,3,4,4,5]
    # employees = [7,8,9]

    # tasks = [2,2,2,2,2]
    # employees = [1,4,4,6]

    # tasks = [2,2,3,3]
    # employees = [1,4,6]
    
    # tasks = [1,2,2,3,3,4,4]
    # employees = [3,5,7,9] # TODO sort decending (?)
    # emp_names = ["A", "B", "C", "D"]

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
    
    print("-------RESULT-------")
    solutions = find_combinations(combs, tasks)
    for s in solutions:
        print(s)



"""
    ............................
"""

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