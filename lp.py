from pulp import *

def distribute_tasks(employees, emp_capacity, tasks, tasks_complexity):
    # Generate dictionaries for task_point supply and demmand nodes
    tp_supply = gen_dict(employees, emp_capacity)
    # TODO remove tp_demand
    #tp_demand = gen_dict(tasks, tasks_complexity)
    
    # Creates a dictionary of Assignment cost" for each possible matching (same, unless adding weigths)
    # TODO use this to assign some sort of diminishing reward to incentivise fair distribution
    tp_cost = [tasks_complexity for i in range(len(capacity))]
    tp_cost = makeDict([employees,tasks], tp_cost,0)
    
    # Initialize LpProblem. Use LpMaximize (maximize task_points assigned)
    prob = LpProblem("Task Assignment Problem", LpMaximize)

    # Creates a list of tuples containing all the possible routes for transport
    assignments = [(e,t) for e in employees for t in tasks]

    # Initialize a dictionary of LpVariables for all possible task-to-employee assignments
    # Use LpBinary to enforce one assignment per task
    assignment_vars = LpVariable.dicts("Assignment", (employees, tasks), cat=LpBinary)
    
    # Objective function for total employees capacity utilization 
    # aka. Sum of employees' assigned task_points (Higher is better)
    prob += lpSum([assignment_vars[e][t]*tp_cost[e][t] for (e,t) in assignments]), "Employee's capacity utilization"
    
    # Constraints
    # Sum of assigned tasks (0||1) * tasks_complexity (task_points) <= worker-capacity (Employee's task_point) 
    for e in employees:
        msj = f"Assigned_tasks_to_Employee_{e}"
        prob += lpSum([assignment_vars[e][t]*tp_cost[e][t] for t in tasks])<=tp_supply[e], msj
    # Only one assignment per task
    for t in tasks:
        prob += lpSum([assignment_vars[e][t] for e in employees])== 1, "Only_1_assignment_per_task%s"%t
        
    # Solve problem and display results
    prob.solve()

    print("Status:", LpStatus[prob.status])
    for v in prob.variables():
    #     if v.varValue > 0:
        print(v.name, "=", v.varValue)
    print("Total task points assigned = ", value(prob.objective))
    # Generate dictionaries for task_point supply and demmand nodes
    tp_supply = gen_dict(employees, emp_capacity)
    tp_demand = gen_dict(tasks, tasks_complexity)
    
    # Creates a dictionary of Assignment cost" for each possible matching (same, unless adding weigths)
    # TODO use this to assign some sort of diminishing reward to incentivise fair distribution
    tp_cost = [tasks_complexity for i in range(len(capacity))]
    tp_cost = makeDict([employees,tasks], tp_cost,0)
    
    # Initialize LpProblem. Use LpMaximize (maximize task_points assigned)
    prob = LpProblem("Task Assignment Problem", LpMaximize)

    # Creates a list of tuples containing all the possible routes for transport
    assignments = [(e,t) for e in employees for t in tasks]

    # Initialize a dictionary of LpVariables for all possible task-to-employee assignments
    # Use LpBinary to enforce one assignment per task
    assignment_vars = LpVariable.dicts("Assignment", (employees, tasks), cat=LpBinary)
    
    # Objective function for total employees capacity utilization 
    # aka. Sum of employees' assigned task_points (Higher is better)
    prob += lpSum([assignment_vars[e][t]*tp_cost[e][t] for (e,t) in assignments]), "Employee's capacity utilization"
    
    # Constraints
    # Sum of assigned tasks (0||1) * tasks_complexity (task_points) <= worker-capacity (Employee's task_point) 
    for e in employees:
        print(assignment_vars[e])
        print(tasks_complexity[e])
        msj = f"Assigned_tasks_to_Employee_{e}"
        prob += lpSum([assignment_vars[e][t]*tasks_complexity[e][t] for t in tasks])<=employees_capacity[e], msj
    # Only one assignment per task
    for t in tasks:
        prob += lpSum([assignment_vars[e][t] for e in employees])== 1, "Only_1_assignment_per_task%s"%t
        
    # Solve problem and display results
    prob.solve()

    print("Status:", LpStatus[prob.status])
    for v in prob.variables():
    #     if v.varValue > 0:
        print(v.name, "=", v.varValue)
    print("Total task points assigned = ", value(prob.objective))