# constants.py

# Bonus Weights for Objective Function
required_power_bonus = 10000           # Strong bonus for required power societies placed at a power socket
normal_placement_bonus = 1             # Base reward for placing any society
preferred_neighbor_bonus = 10000       # Huge bonus for preferred neighbors placed nearby
subgroup_clustering_bonus = 10          # Bonus for grouping societies of the same subgroup in a neighborhood
category_compactness_bonus = 5          # Bonus for compacting a category into the same room
all_together_bonus = 25                 # Bonus if an entire category is in one room on one day
category_pure_bonus = 3                 # Bonus if a neighborhood is "pure" for a category

# Solver Settings
max_solver_time = 120           # Time limit for CP-SAT solver in seconds

# --- Main Societies Groupings ---

categories = {
    "Culture": [
        "Caledonian Society", "African Carribean Society", "Arab Society", "Bengali Society",
        "Indian Student Association", "Chinese Society", "East African Society", "Egyptian Society",
        "Filipino Society", "French Society", "Iranian Society", "Japanese Society", "Latin American Society",
        "Punjabi Society", "Singaporean Society", "Sudanese Society", "Tamil Society",
        "Thai Society", "Korean Society", "Malaysian Society", "Hong Kong Society", "Malaysian & Singaporean Society",
        "Welsh Society", "Nigerian Society", "North African Society", "Pakistani Society",
        "Taiwanese Society", "British Chinese Society", "Russian & Slavonic", "Sri Lankan",
        "Telugu Society", "Turkic Society", "Spanish, Latin American, and Portuguese Society"
    ],
    "Faith": [
        "Believers Loveworld", "Catholic", "Christian Union", "CICC Ignite", "First Love Society",
        "Jewish Society", "Leeds Orthodox Christian Society", "Leeds Sikh Society",
        "National Hindu Students Forum", "AhlulBayt Society", "Islamic Society",
        "Pensa Leeds", "Buddhist Meditation Society"
    ],
    "Political": [
        "Students for Global Health", "Students for Sensible Drug Policy", "Amnesty International",
        "Black Feminist Society", "Black Women's Project", "Enactus", "European Union Affairs Society",
        "Feminist Society", "Green Party Society", "Leeds Friends of Medicine San Frontiers",
        "Leeds Labour Society", "Palestine Solidarity Group", "Conservative Society"
    ],
    "Welfare": [
        "British Sign Language", "Commuters", "LGBT", "Mind Matters", "Neurodivergent",
        "SSAFE", "SASHA"
    ],
    "Volunteering": [
        "Community First Responders", "Conservation Volunteers", "Homed", "Heart Beats",
        "Leeds Marrow", "Leeds RAG", "Leeds RAG Fashion Show", "Uni Boob Team",
        "Music Impact in the Community", "Nightline", "St. John Ambulance",
        "Student Action for Refugees", "Teddy Bear Hospital", "The 93% Club"
    ],
    "Media": [
        "Her Campus", "Leeds Student Radio", "Lippy", "LSTV", "The Gryphon", "The Scribe"
    ],
    "Music and Performance": [
        "A Cappella", "Album Review", "Backstage", "Big Band", "BPM", "Jazz & Blues",
        "LAMMPS", "Musical Theatre", "Open Theatre", "Pantomime", "Performing Arts",
        "Spoken Word", "Stage Musicals", "Tealights", "The Arrhythmics",
        "Theatre Group", "Union Music Library"
    ],
    "Dance": [
        "Ballet", "Belly Dance", "Dance Expose", "Dancesport", "Freestyle Dance",
        "Heelz Dance", "Irish Dancing", "KPOP Dance", "Modern Dance", "Salsa",
        "Street Dance", "Swing Dance", "Vertical Fitness", "Vibes: Bollywood Dance"
    ],
    "General Interest": [
        "Anime & Manga", "Art", "AstroSoc", "Baking", "Book Club", 
        "Casual Kickabout", "Change Ringers", "Chess", "Coffee", "Comics & Graphic Novels", 
        "Cosy Games", "Cryptocurrency", "Debating", "DiceSoc", "Entrepreneurs", 
        "eSports", "Film", "Horror", "Rock & Alternative", "SwiftSoc", 
        "Poker", "Motorbike", "Magic the Gathering", "Nintendo & Pokemon", "PlantSoc", 
        "Quadball", "Real Ale", "Sci Fi & Fantasy", "Stitch & Bitch", "Trading & Investments", 
        "Vegetarian & Vegan", "Warhammer", "Wine", "Women in Leadership", "Yoga"
    ],
    "Academic": [
        "Access to Medicine", "Artificial Intelligence", "Aviation", "Barrister", "Brain Leeds",
        "LUBS", "CardioSoc", "Chemical Engineering", "Chemistry", "CivSoc", 
        "Classics", "Commercial Awareness", "CompSoc", "Consulting", "CRASHSoc",
        "Cutting Edge", "DentSoc", "DermSoc", "Design", "RocSoc",
        "Economics", "Endocrinology", "English", "EyeSoc", "Biological Sciences",
        "FAHACS", "FirstGen Medics", "Food Science & Nutrition", "Geography",
        "German", "History", "Human Resources", "International History", "International Business",
        "Italian", "Law", "Media", "Liberal Arts", "Linguistics", 
        "Mathematics", "MechEngSoc", "Medieval", "MedSoc", "Natural Sciences",
        "Neuroscience", "Nursing", "Philosophy", "Physics", "POLIS", 
        "PPE", "PPST", "Psychiatry", "Psychology",
        "ShockSoc", "SocCrimSoc", "Transport & Mobility", "Economic Geologists"
    ],
    "Outdoor": [
        "Canoe Club", "Caving", "Hiking", "Mountaineering", "Orienteering",
        "Sailing", "Scout & Guide", "Skate", "Skydiving", "Snowriders",
        "Sub Aqua", "Surf", "Wilderness Medicine"
    ],
    "Martial Arts": [
        "Aikido", "Boxing", "Brazilian Jiu Jitsu", "Daoist Taichi", "Hung Kuen",
        "Jiu Jitsu", "Judo", "Karate", "Kickboxing & Krav Maga", "Muay Thai",
        "Tae-Kwon-Do"
    ],
    "Sport": [
        "American Football", "Archery", "Association Football (m)", "Association Football (w)", "Athletics",
        "Badminton", "Barbell Club", "Basketball (m)", "Basketball (w)", "Cheerleading",
        "Cricket (m)", "Cricket (w)", "Cross Country", "Cycling", "Darts",
        "Development Netball", "Dodgeball", "Fencing", "Futsal (m)", "Futsal (w)",
        "Girls Training Together", "Golf", "Gymnastics", "Handball", "Hockey (m)",
        "Hockey (w)", "Horse Riding", "Ice Hockey", "Korfball", "Lacrosse (m)",
        "Lacrosse (w)", "Motorsport", "Netball", "Padel", "Pool & Snooker",
        "Rifle", "Rounders", "Roundnet", "Rowing", "Rugby League (m)",
        "Rugby League (w)", "Rugby Union (m)", "Rugby Union (w)", "Softball", "Squash & Racketball",
        "Swimming & Waterpolo", "Synchronised Swimming", "Table Tennis", "Tennis", "Touch Rugby",
        "Trampoline", "Triathlon", "Ultimate Frisbee", "Volleyball"
    ]
}

# --- Subgroups ---

academic_subgroups = {
    "Business & Economics": ["Commercial Awareness", "Consulting", "Economics", "LUBS", "International Business", "Economic Geologists", "Human Resources"],
    "Tech": ["Artificial Intelligence", "Chemical Engineering", "CompSoc", "Mathematics", "MechEngSoc", "Physics", "ShockSoc"],
    "Humanities": ["Classics", "Design", "English", "FAHACS", "History", "Liberal Arts", "Linguistics", "Media"],
    "Languages": ["German", "Italian", "Russian & Slavonic", "Spanish, Latin American, & Portuguese"],
    "Law & Politics": ["Barrister", "Law", "Philosophy", "POLIS", "PPE", "PPST", "SocCrimSoc"],
    "Medicine": ["Access to Medicine", "CardioSoc", "Cutting Edge", "DentSoc", "DermSoc", "Endocrinology", "EyeSoc", "FirstGen Medics", "MedSoc", "Neuroscience", "Psychiatry", "Nursing"],
    "Sciences": ["Biological Sciences", "Chemistry", "Food Science & Nutrition", "Geography", "Natural Sciences", "Psychology", "RocSoc"]
}

general_interest_subgroups = {
    "Books": ["Book Club", "Anime & Manga", "Comics & Graphic Novels", "Debating"],
    "Movies": ["Film", "Horror", "Sci Fi & Fantasy"],
    "Hobbies": ["Art", "AstroSoc", "Stitch & Bitch", "Yoga", "Motorbike", "Change Ringers", "PlantSoc", "Quadball", "Casual Kickabout"],
    "Finance": ["Economics", "Entrepreneurs", "Trading & Investments", "Cryptocurrency"],
    "Gaming": ["Cosy Games", "Chess", "DiceSoc", "Magic the Gathering", "Nintendo & Pokemon", "Poker", "Warhammer", "eSports"],
    "Food": ["Baking", "Coffee", "Real Ale", "Vegetarian & Vegan", "Wine"],
    "Music": ["SwiftSoc", "Rock & Alternative"]
}

sports_subgroups = {
    "Team Sports": ["American Football", "Basketball (m)", "Basketball (w)", "Netball", "Rugby League (m)", "Rugby League (w)", "Rugby Union (m)", "Rugby Union (w)", "Hockey (m)", "Hockey (w)", "Association Football (m)", "Association Football (w)", "Cricket (m)", "Cricket (w)", "Futsal (m)", "Futsal (w)", "Ultimate Frisbee", "Roundnet", "Touch Rugby", "Ice Hockey", "Korfball", "Softball", "Volleyball"],
    "Individual Sports": ["Archery", "Athletics", "Badminton", "Barbell Club", "Darts", "Table Tennis", "Squash & Racketball", "Tennis"],
    "Aquatic & Outdoor": ["Rowing", "Swimming & Waterpolo", "Triathlon", "Horse Riding", "Cycling", "Golf", "Synchronised Swimming"],
    "Racquet Sports": ["Badminton", "Squash & Racketball", "Tennis", "Padel", "Table Tennis"],
    "Other": ["Girls Training Together", "Gymnastics", "Trampoline", "Rounders", "Motorsport", "Pool & Snooker"]
}

# --- Conflict and Constraints ---

conflict_societies = {
    "Green Party Society": {"Leeds Labour Society", "Conservative Society"},
    "Leeds Labour Society": {"Green Party Society", "Conservative Society"},
    "Conservative Society": {"Leeds Labour Society", "Green Party Society"},
    "Jewish Society": {"Palestine Solidarity Group"},
    "Palestine Solidarity Group": {"Jewish Society"},
}

required_power_societies = {
    "LSTV", "Leeds Student Radio", "The Gryphon", "Backstage", "Union Music Library",
    "Stage Musicals", "Performing Arts", "Salsa", "Dance Expose",
    "Jazz & Blues", "Big Band"
}

preferred_neighbors = {
    "CompSoc": ["DiceSoc", "eSports", "Artificial Intelligence"],
    "Media": ["The Gryphon", "LSTV", "Leeds Student Radio"],
    "Backstage": ["LSTV"],
    "Psychology": ["Neuroscience", "Psychiatry"],
    "French Society": ["Spanish, Latin American, & Portuguese", "German", "Italian"],
}

# --- Layout ---
days = ["Monday", "Tuesday", "Wednesday"]

rooms = {
    "Room 1": list(range(1, 34)),
    "Room 2": list(range(1, 49)),
    "Room 3": list(range(1, 98))
}

# Other Settings
power_stalls = {
    "Room 1": {1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15},
    "Room 2": set(),
    "Room 3": {2, 3, 6, 7, 8, 9, 53, 54, 57, 58, 92, 93, 95, 96}
}

neighborhoods = {
    "Room 1": {
        1: [1,2,3,4,22,23,24],
        2: [5,6,7,8,9,10,11,25,26,27,28,29,30],
        3: [12,13,14,15,31,32,33],
        4: [16,17,18,19,20,21]
    },
    "Room 2": {
        5: [1,2,3,4,5,6,19,20,21,22,23,24],
        6: [7,8,9,10,11,12,13,14,15,16,17,18],
        7: [25,26,27,28,29,30,43,44,45,46,47,48],
        8: [31,32,33,34,35,36,37,38,39,40,41,42]
    },
    "Room 3": {
        9: [1,2,3,4],
        10: [5,6,7,8,9,10,11,12],
        11: [13,14,15,16],
        12: [17,18,19,20,21,22,23],
        13: [24,25,26,27,28,29,30],
        14: [31,32,33,34,35,36,37],
        15: [38,39,40,41,42,48,49,50,51],
        16: [43,44,45,46,47],
        17: [52,53,54,55,56,57,58,59],
        18: [60,61,62,63,64,65,66,67,68],
        19: [69,70,71,72,73,74,75,76,77],
        20: [78,79,80,81,82,83,84,85,86],
        21: [87,88,89,90],
        22: [91,92,93,94,95,96,97]
    }
}

# Debugging Options
PRINT_ASSIGNMENTS = True                # Whether to print detailed assignment results
PRINT_FALLBACK_ASSIGNMENTS = True        # Whether to print fallback assignments
