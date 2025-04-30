# model.py

from ortools.sat.python import cp_model
from constants import (
    preferred_neighbor_bonus, required_power_bonus, subgroup_clustering_bonus, category_compactness_bonus, 
    all_together_bonus, category_pure_bonus, normal_placement_bonus)

# --- Assigning Variables --- 
def create_assignment_vars(model, societies, rooms, days):
    x = {}
    for s in societies:
        x[s] = {}
        for r in rooms:
            x[s][r] = {}
            for stall in rooms[r]:
                x[s][r][stall] = {}
                for d in days:
                    x[s][r][stall][d] = model.NewBoolVar(f"x_{s}_{r}_{stall}_{d}")
    return x

# --- Hard Constraint #1: Single Assignment ---
def single_assignment_constraint(model, x, societies, rooms, days):
    for s in societies:
        model.Add(sum(x[s][r][stall][d] for r in rooms for stall in rooms[r] for d in days) <= 1)

# --- Hard Constraint #2: No Double Occupancy ---
def no_double_occupancy_constraint(model, x, societies, rooms, days):
    for r in rooms:
        for stall in rooms[r]:
            for d in days:
                model.Add(sum(x[s][r][stall][d] for s in societies) <= 1)

# --- Hard Constraint #3: Room Availability ---
def room3_constraints(model, x, societies, society_to_category, rooms, days):
    allowed_room3_categories = {"Sport", "Martial Arts", "Outdoor", "Dance"}
    for s in societies:
        for stall in rooms["Room 3"]:
            model.Add(x[s]["Room 3"][stall]["Monday"] == 0)
        if society_to_category[s] not in allowed_room3_categories:
            for stall in rooms["Room 3"]:
                for d in days:
                    model.Add(x[s]["Room 3"][stall][d] == 0)

# --- Hard Constraint #4: Conflict Avoidance ---
def conflict_constraints(model, x, societies, conflict_societies, stall_to_neighborhood, rooms, days):
    for s1 in societies:
        for s2 in conflict_societies.get(s1, set()):
            for r in rooms:
                for d in days:
                    for stall1 in rooms[r]:
                        for stall2 in rooms[r]:
                            n1 = stall_to_neighborhood.get((r, stall1))
                            n2 = stall_to_neighborhood.get((r, stall2))
                            if n1 is not None and n2 is not None and abs(n1 - n2) <= 1:
                                model.Add(x[s1][r][stall1][d] + x[s2][r][stall2][d] <= 1)

# --- Soft Constraint #1: Power Socket Reward ---
def power_constraints(model, x, required_power_societies, power_stalls, rooms, days):
    for s in required_power_societies:
        for r in rooms:
            for stall in rooms[r]:
                for d in days:
                    if stall not in power_stalls.get(r, set()):
                        model.Add(x[s][r][stall][d] == 0)

# - Normal reward for placing society
def build_power_terms(model, x, societies, required_power_societies, power_stalls, rooms, days):
    objective_terms = []
    for s in societies:
        for r in rooms:
            for stall in rooms[r]:
                for d in days:
                    if s in required_power_societies and stall in power_stalls.get(r, set()):
                        objective_terms.append(required_power_bonus * x[s][r][stall][d])
                    else:
                        objective_terms.append(normal_placement_bonus * x[s][r][stall][d])
    return objective_terms

# --- Soft Constraint #2: Category / Subgroup Clustering ---
# - Category Clustering
def category_pure_neighborhood_objective(model, x, societies, society_to_category, rooms, neighborhoods, days):
    objective_terms = []
    all_categories = list(set(society_to_category[s] for s in societies))

    for r in rooms:
        for n in neighborhoods[r]:
            for d in days:
                in_neigh = {
                    cat: [x[s][r][stall][d]
                          for s in societies if society_to_category[s] == cat
                          for stall in neighborhoods[r][n]]
                    for cat in all_categories
                }

                not_in_neigh = {
                    cat: [x[s][r][stall][d]
                          for s in societies if society_to_category[s] != cat
                          for stall in neighborhoods[r][n]]
                    for cat in all_categories
                }

                for cat in all_categories:
                    if not in_neigh[cat]:
                        continue
                    pure = model.NewBoolVar(f"pure_{r}_{n}_{d}_{cat}")
                    model.Add(sum(in_neigh[cat]) >= 1).OnlyEnforceIf(pure)
                    model.Add(sum(not_in_neigh[cat]) == 0).OnlyEnforceIf(pure)
                    model.Add(sum(in_neigh[cat]) < 1).OnlyEnforceIf(pure.Not())
                    objective_terms.append(category_pure_bonus * pure)
    return objective_terms

# - Subgroup Clustering
def subgroup_clustering_objective(model, x, societies, society_to_subgroup, rooms, neighborhoods, days):
    objective_terms = []
    all_subgroups = list(set(society_to_subgroup[s] for s in societies if s in society_to_subgroup))

    subgroup_count_vars = {}

    for r in rooms:
        for n in neighborhoods[r]:
            for d in days:
                for subgroup in all_subgroups:
                    subgroup_societies = [s for s in societies if society_to_subgroup.get(s) == subgroup]
                    subgroup_count = model.NewIntVar(0, len(subgroup_societies) * len(neighborhoods[r][n]), f"subgrp_count_{r}_{n}_{d}_{subgroup}")
                    model.Add(subgroup_count == sum(
                        x[s][r][stall][d]
                        for s in subgroup_societies
                        for stall in neighborhoods[r][n]
                    ))
                    subgroup_count_vars[(r, n, d, subgroup)] = subgroup_count

    for r in rooms:
        for n in neighborhoods[r]:
            for d in days:
                majority_var = model.NewIntVar(0, len(neighborhoods[r][n]), f"majority_subgroup_{r}_{n}_{d}")
                model.AddMaxEquality(majority_var, [subgroup_count_vars[(r, n, d, sg)] for sg in all_subgroups])
                objective_terms.append(subgroup_clustering_bonus * majority_var)

    return objective_terms

# --- Soft Constraint #3: Room Compactness ---
def category_room_compactness_objective(model, x, societies, society_to_category, rooms, days):
    objective_terms = []
    all_categories = list(set(society_to_category[s] for s in societies))

    category_roomday_counts = {}

    for cat in all_categories:
        cat_societies = [s for s in societies if society_to_category[s] == cat]
        for r in rooms:
            for d in days:
                count_var = model.NewIntVar(0, len(cat_societies), f"catcount_{cat}_{r}_{d}")
                model.Add(count_var == sum(
                    x[s][r][stall][d]
                    for s in cat_societies
                    for stall in rooms[r]
                ))
                category_roomday_counts[(cat, r, d)] = count_var

    category_day_max_in_room = {}

    for cat in all_categories:
        for d in days:
            max_var = model.NewIntVar(0, len([s for s in societies if society_to_category[s] == cat]), f"catmax_{cat}_{d}")
            model.AddMaxEquality(max_var, [category_roomday_counts[(cat, r, d)] for r in rooms])
            category_day_max_in_room[(cat, d)] = max_var

            # Normal compactness reward
            objective_terms.append(category_compactness_bonus * max_var)

            # Super-bonus if all together
            cat_size = len([s for s in societies if society_to_category[s] == cat])
            all_together = model.NewBoolVar(f"all_{cat}_together_{d}")
            model.Add(max_var == cat_size).OnlyEnforceIf(all_together)
            model.Add(max_var != cat_size).OnlyEnforceIf(all_together.Not())
            objective_terms.append(all_together_bonus * all_together)

    return objective_terms


# --- Soft Constraint #4: Preferred Neighbours ---
def preferred_neighbors_objective(model, x, societies, preferred_neighbors, rooms, neighborhoods, days):
    objective_terms = []
    society_in_neigh = {}

    for s in societies:
        for r in rooms:
            for n in neighborhoods[r]:
                for d in days:
                    neighbor_stalls = neighborhoods[r][n]
                    var = model.NewBoolVar(f"in_neigh_{s}_{r}_{n}_{d}")
                    model.Add(sum(x[s][r][stall][d] for stall in neighbor_stalls) >= 1).OnlyEnforceIf(var)
                    model.Add(sum(x[s][r][stall][d] for stall in neighbor_stalls) == 0).OnlyEnforceIf(var.Not())
                    society_in_neigh[(s, r, n, d)] = var

    for soc1, neighbors in preferred_neighbors.items():
        for soc2 in neighbors:
            if soc2 not in societies or soc1 not in societies:
                continue
            for r in rooms:
                for n in neighborhoods[r]:
                    for d in days:
                        var1 = society_in_neigh[(soc1, r, n, d)]
                        var2 = society_in_neigh[(soc2, r, n, d)]
                        both_here = model.NewBoolVar(f"preferred_{soc1}_{soc2}_{r}_{n}_{d}")
                        model.AddBoolAnd([var1, var2]).OnlyEnforceIf(both_here)
                        model.AddBoolOr([var1.Not(), var2.Not()]).OnlyEnforceIf(both_here.Not())
                        objective_terms.append(preferred_neighbor_bonus * both_here)
    return objective_terms

def finalize_objective(model, objective_terms):
    model.Maximize(sum(objective_terms))
