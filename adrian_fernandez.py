from itertools import permutations, repeat, combinations
from collections import Counter

"""
    Helpers
"""
def gen_combinations(tasks: list):
    """ Generate a set of all possible tasks combinations.

    Constraints:
    1) Combinations can't be higher than max task task point (tp) value,
    2) Sum of all combinations can't be higher than sum of tasks tp
    """
    max_val = sum(tasks)
    combs = []
    for r in range(1, len(tasks)):
        combs += [x for x in combinations(tasks, r) if sum(x) <= max_val]
    return list(set(combs))

def validate_solution(solution: list, task_counter: Counter):
    """ Checks for duplicate use of tasks items in combinations."""
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
    """ Tries to match all task_points from the solution, with employees."""
    if validate_solution(comb_tasks, task_counter) is False:
        return False

    # Keep track of assignments
    empl_assignments = [[] for i in employees_tp]
    empl_remaining = employees_tp.copy()
    total_assignments = 0
    tasks_remaining = tasks_tp.copy()

    e_ix = 0
    # Loop through task_points (index) in combination tasks, and employees
    for tc_ix in range(len(comb_tasks)):
        while e_ix <= len(employees_tp):
            # Get task_point value if, has to be lower than max employee capacity
            t_tc = comb_tasks[tc_ix]
            if t_tc > max(empl_remaining):
                break
            
            # Match task with employee, then focus on next employee. This is
            # to achieve a more even distribution of work (as opposed to exhausting
            # a single employee before moving to the next) 
            if empl_remaining[e_ix] >= t_tc:
                empl_assignments[e_ix].append(t_tc)
                empl_remaining[e_ix] -= t_tc
                tasks_remaining[tc_ix] = 0
                total_assignments += t_tc
                # I'm not proud of the following lines... but YOLO 
                e_ix += 1
                if e_ix == len(employees_tp):
                    e_ix = 0
                break
            e_ix += 1
            if e_ix == len(employees_tp):
                e_ix = 0

    if target == total_assignments:
        print("Target!", total_assignments, empl_assignments)
        return empl_assignments
    else:
        return False

"""
    Main Func
"""
def assign_tasks_to_workers(combs, tasks, lower_target=0):
    """ Finds an optimal way to match tasks to employees."""
    
    row, col = 0, len(combs)-1
    tp_target =  min(sum(tasks), sum(employees_tp)) - lower_target

    # Task task_point counter used to validate task-combinations
    task_counter = Counter(tasks)
    print("Target task_point:", tp_target, lower_target)

    # Use a matrix-ish to find the combinations of possible tasks 
    # that == the target task_point. Search moves from top-right
    # to bottom-left until it finds a matching value.
    while row < len(combs) and col >= 0:
        comb_value = sum(combs[row]) + sum(combs[col])
        tp_difference = comb_value - tp_target

        if tp_difference == 0:
            # Join task-combinations into a list
            comb_tasks = list(combs[row]) + list(combs[col])
            
            # Attempt to match this task-combination to employees
            employees_tasks = allocate_tasks(comb_tasks,tp_target, task_counter)
            if employees_tasks:     
                return employees_tasks     
            col-=1

        # Move to a higher combination
        if tp_difference < 0:
            row+=1
        # Move to a lower combination
        else:
            col-=1

    # If not Solution found, lower_target task_point and start over
    lower_target += 1
    print("*** No Solution, lower task_point target:", lower_target)
    solution =  assign_tasks_to_workers(combs, tasks, lower_target)
    if solution:
        return solution
    else:
        return None


"""
    Run Code
"""
if __name__ == '__main__':
    # Define start values
    tasks_tp = [6, 3, 2, 8, 3, 5, 9, 13, 5, 4, 7, 2, 3, 5]
    tasks_names = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12", "T13"]
    employees_tp = [2, 8, 5, 7, 17, 20, 18]
    employees_names = ["A", "B", "C", "D", "E", "F"]

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
    solution = assign_tasks_to_workers(combs, tasks_tp)

    print("-------RESULTS-------")
    for i in range(len(employees_names)):
        key = employees_names[i]
        employees_dic[key]["assigned_tasks"] = get_tasks_names(solution[i])
        employees_dic[key]["assigned_tasks_points"] = solution[i]
        print("Employee", key)
        print(employees_dic[key])
    print("--------------------")
