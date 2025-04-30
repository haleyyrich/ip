# utils.py

def flatten(list_of_lists):
    """Flatten a list of lists into a single list."""
    return [item for sublist in list_of_lists for item in sublist]

def precompute_stall_to_neighborhood(neighborhoods):
    """Precompute a mapping (room, stall) -> neighborhood number."""
    stall_to_neigh = {}
    for room, neigh_dict in neighborhoods.items():
        for neigh_num, stalls in neigh_dict.items():
            for stall in stalls:
                stall_to_neigh[(room, stall)] = neigh_num
    return stall_to_neigh

def get_adjacent_neighborhood_pairs(room_neighborhoods):
    """Get neighborhood adjacency pairs (n, n+1) based on their number."""
    n_list = sorted(room_neighborhoods.keys())
    return [(n_list[i], n_list[i+1]) for i in range(len(n_list) - 1)]

def build_society_to_category(categories):
    """Create a lookup: society -> category."""
    return {society: category for category, society_list in categories.items() for society in society_list}

def build_society_to_subgroup(subgroup_dicts):
    """Create a lookup: society -> subgroup."""
    society_to_subgroup = {}
    for subgroup_dict in subgroup_dicts:
        for subgroup, societies in subgroup_dict.items():
            for society in societies:
                society_to_subgroup[society] = subgroup
    return society_to_subgroup

def sort_assignments(assignments, days_order):
    """Sort assignments nicely by day, room, and neighborhood."""
    return sorted(assignments, key=lambda x: (days_order.index(x[0]), x[1], x[2]))

def print_assignments(assignments, days_order):
    """Print assignments by day, room, and neighborhood."""
    current_day = None
    current_room = None
    current_neighborhood = None

    for day, room, neighborhood, stall, society, category, subgroup, is_fallback in sorted(assignments, key=lambda x: (days_order.index(x[0]), x[1], x[2], x[3])):
        if day != current_day:
            print(f"\n {day}")
            current_day = day
            current_room = None
        if room != current_room:
            print(f"  {room}:")
            current_room = room
            current_neighborhood = None
        if neighborhood != current_neighborhood:
            print(f"    Neighborhood {neighborhood}:")
            current_neighborhood = neighborhood

        fallback_tag = " (fallback)" if is_fallback else ""
        print(f"      Stall {stall}: {society} ({category} | {subgroup}){fallback_tag}")
