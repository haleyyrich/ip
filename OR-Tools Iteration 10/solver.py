# solver.py
# MAIN FUNCTION, RUN THIS FILE!

from ortools.sat.python import cp_model
from constants import (rooms, days, max_solver_time, categories, academic_subgroups, general_interest_subgroups, sports_subgroups,
    neighborhoods, power_stalls, conflict_societies, required_power_societies, preferred_neighbors)
from utils import (precompute_stall_to_neighborhood, build_society_to_category, build_society_to_subgroup, print_assignments)
from model import (create_assignment_vars, single_assignment_constraint, no_double_occupancy_constraint, room3_constraints, conflict_constraints, power_constraints, build_power_terms, category_pure_neighborhood_objective, subgroup_clustering_objective, category_room_compactness_objective, preferred_neighbors_objective, finalize_objective)

def main():
    model = cp_model.CpModel()

    # --- Lookups ---
    societies = [s for soc_list in categories.values() for s in soc_list]

    society_to_category = build_society_to_category(categories)
    society_to_subgroup = build_society_to_subgroup([academic_subgroups, general_interest_subgroups, sports_subgroups])
    stall_to_neighborhood = precompute_stall_to_neighborhood(neighborhoods)

    # --- Create Variables ---
    x = create_assignment_vars(model, societies, rooms, days)

    # --- Constraints ---
    single_assignment_constraint(model, x, societies, rooms, days)
    no_double_occupancy_constraint(model, x, societies, rooms, days)
    room3_constraints(model, x, societies, society_to_category, rooms, days)
    conflict_constraints(model, x, societies, conflict_societies, stall_to_neighborhood, rooms, days)
    power_constraints(model, x, required_power_societies, neighborhoods, rooms, days)
   

    # --- Objective Function ---
    objective_terms = power_constraints(model, x, required_power_societies, neighborhoods, rooms, days)
    objective_terms = build_power_terms(model, x, societies, required_power_societies, power_stalls, rooms, days)
    objective_terms += preferred_neighbors_objective(model, x, societies, preferred_neighbors, rooms, neighborhoods, days)
    objective_terms += category_pure_neighborhood_objective(model, x, societies, society_to_category, rooms, neighborhoods, days)
    objective_terms += subgroup_clustering_objective(model, x, societies, society_to_subgroup, rooms, neighborhoods, days)
    objective_terms += category_room_compactness_objective(model, x, societies, society_to_category, rooms, days)
    objective_terms += preferred_neighbors_objective(model, x, societies, preferred_neighbors, rooms, neighborhoods, days)
    finalize_objective(model, objective_terms)

    # --- Solve ---
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = max_solver_time
    status = solver.Solve(model)

    # --- Output ---
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("\n Feasible solution found!")
        assignments = []
        placed_societies = set()
        assigned_stalls = set()

        for s in societies:
            for r in rooms:
                for stall in rooms[r]:
                    for d in days:
                        if solver.BooleanValue(x[s][r][stall][d]):
                            cat = society_to_category.get(s, "Unknown")
                            subgroup = society_to_subgroup.get(s, "None")
                            neighborhood = stall_to_neighborhood.get((r, stall), "Unknown")
                            assignments.append((d, r, neighborhood, stall, s, cat, subgroup, False))  # False = not fallback
                            placed_societies.add(s)
                            assigned_stalls.add((r, stall, d))

    # --- Fallback Assignment --- 
        # - Find unplaced societies and open stalls
        unplaced_societies = list(set(societies) - placed_societies)
        open_stalls = []
        for r in rooms:
            for stall in rooms[r]:
                for d in days:
                    if (r, stall, d) not in assigned_stalls:
                        open_stalls.append((r, stall, d))
        fallback_societies = set()

        # - Simple greedy fallback allocation
        for s, (r, stall, d) in zip(unplaced_societies, open_stalls):
            cat = society_to_category.get(s, "Unknown")
            subgroup = society_to_subgroup.get(s, "None")
            neighborhood = stall_to_neighborhood.get((r, stall), "Unknown")
            assignments.append((d, r, neighborhood, stall, s, cat, subgroup, True))  # True = fallback
            fallback_societies.add(s)
        
        # - Total placements
        if assignments:
            print_assignments(assignments, days)
            print(f"\nTotal societies placed: {len(set(a[4] for a in assignments))} / {len(societies)}")
        else:
            print("\nNo assignments made.")

        # - Fallback societies diagnostics
        if fallback_societies:
            print(f"\n {len(fallback_societies)} societies were assigned via fallback:")
            print("\n Societies assigned via fallback:")
            for s in sorted(fallback_societies):
                print(f"- {s}")
        else:
            print("\n No fallback assignments were needed!")
        
    # --- Diagnostics ---
        # - Required power societies diagnostics
        placed_required_power = required_power_societies & placed_societies
        print(f"\n Required power societies placed: {len(placed_required_power)} / {len(required_power_societies)}")

        # - Conflicts avoided diagnostics
        total_conflict_pairs = 0
        conflicts_avoided = 0

        for s1 in societies:
            for s2 in conflict_societies.get(s1, set()):
                if s1 >= s2:
                    continue  # avoid double-counting
                total_conflict_pairs += 1
                conflict = False
                for d in days:
                    for r in rooms:
                        for stall1 in rooms[r]:
                            for stall2 in rooms[r]:
                                if solver.BooleanValue(x[s1][r][stall1][d]) and solver.BooleanValue(x[s2][r][stall2][d]):
                                    n1 = stall_to_neighborhood.get((r, stall1))
                                    n2 = stall_to_neighborhood.get((r, stall2))
                                    if n1 is not None and n2 is not None and abs(n1 - n2) <= 1:
                                        conflict = True
                if not conflict:
                    conflicts_avoided += 1

        print(f"\n Conflicts avoided: {conflicts_avoided} / {total_conflict_pairs}")

        # - Preferred neighbors paired diagnostics
        total_preferred = 0
        preferred_success = 0

        for soc1, neighbors in preferred_neighbors.items():
            for soc2 in neighbors:
                if soc1 not in societies or soc2 not in societies or soc1 >= soc2:
                    continue
            total_preferred += 1
            matched = False
            for d in days:
                for r in rooms:
                    for n in neighborhoods[r]:
                        stalls = neighborhoods[r][n]
                        if any(solver.BooleanValue(x[soc1][r][s][d]) for s in stalls) and \
                            any(solver.BooleanValue(x[soc2][r][s][d]) for s in stalls):
                            matched = True
            if matched:
                preferred_success += 1

        print(f"\n Preferred neighbors grouped: {preferred_success} / {total_preferred}")

    else:
        print("\n No feasible solution found within time limit.")

if __name__ == "__main__":
    main()
