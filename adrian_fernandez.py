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

def get_tasks_names(assigned_tp):
    """ Takes a list of tasks task_points, returns matching names."""
    task_names = []
    for tp in assigned_tp:
        t_ix = tasks_tp.index(tp)
        task_names.append(tasks_names[t_ix])
        # Modify task value to prevent duplicate matches
        tasks_tp[t_ix] = 0
    return task_names

def allocate_tasks(comb_tasks, target, task_counter):
    if not validate_solution(comb_tasks, task_counter):
        return False

    # Keep track of assignments
    empl_assignments = [[] for i in employees_tp]
    empl_remaining = employees_tp.copy()
    total_assignments = 0
    tasks_remaining = tasks_tp.copy()
    # print("Allocate tasks, comb_tasks:", comb_tasks)
#     empl_assigned = [0 for e in employees]
#     print(empl_assignments, empl_remaining)
    e_i = 0
    for tc_ix in range(len(comb_tasks)):
        while e_i <= len(employees_tp):
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
                if e_i == len(employees_tp):
                    e_i = 0
                break
            e_i += 1
            if e_i == len(employees_tp):
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
    temp = min(sum(tasks), sum(employees_tp))
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
                # print("!!!!! SOLUTION ", employees_tasks)
                # solutions.append(employees_tasks)       
                return employees_tasks     
            col-=1

        # Move to a higher combination
        if tp_difference < 0:
            row+=1
        # Move to a lower combination
        elif tp_difference > 0:
            col-=1

    # If not Solution found, lower_target task_point total and start over
    lower_target += 1
    print("*** No Solution, lower task_point target:", lower_target)
    solution =  find_combinations(combs, tasks, lower_target)
    return solution


"""
    Run Code
"""
if __name__ == '__main__':
    # Define start values
    tasks_tp = [6,3,2,3,5]
    tasks_names = ["T1", "T2", "T3", "T4", "T5"]
    employees_tp = [3,5,7]
    employees_names = ["A", "B", "C"]

    tasks_dic = {name:val for name, val in zip(tasks_names, tasks_tp)}
    tasks_tp.sort()
    employees_dic = {name:{'task_point':val} for name, val in zip(employees_names, 
                                                                  employees_tp)}
    print("Tasks", tasks_dic)                                                                
    print("Employees", employees_dic)

    # Generate possible combinations of tasks, given constraints
    combs = gen_combinations(tasks_tp)
    combs.sort(key=lambda x: sum(x))
    
    # call main function
    solution = find_combinations(combs, tasks_tp)
    
    print("-------RESULTS-------")
    for i in range(len(employees_names)):
        key = employees_names[i]
        employees_dic[key]["assigned_tasks"] = get_tasks_names(solution[i])
        employees_dic[key]["assigned_tasks_points"] = solution[i]
        print("Employee", key)
        print(employees_dic[key])
    print("--------------------")
