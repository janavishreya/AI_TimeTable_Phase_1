from algorithms.genetic_algorithm import run_genetic_algorithm
from algorithms.constraint_propagation import apply_constraints
from algorithms.local_search import optimize_timetable
from algorithms.backtacking import resolve_conflicts



def generate_timetable(input_data):
    initial_population = run_genetic_algorithm(input_data)
    feasible_population = apply_constraints(initial_population, input_data)
    optimized_timetable = optimize_timetable(feasible_population, input_data)
    final_timetable = resolve_conflicts(optimized_timetable, input_data)

    return final_timetable
