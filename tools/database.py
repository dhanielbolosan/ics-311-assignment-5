import sqlite3
from contextlib import contextmanager

# prevent repeating connection for every function
@contextmanager
def connect_db():
    conn = sqlite3.connect('islands.db')
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        conn.close()

# initialize database
def create_db():
    with connect_db() as cursor:
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS islands (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        latitude REAL,
                        longitude REAL,
                        population INTEGER,
                        canoes INTEGER,
                        canoe_capacity INTEGER
                        )
                    ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS resources (
                        id INTEGER PRIMARY KEY,
                        island_id INTEGER,
                        resource_name TEXT,
                        quantity INTEGER,
                        FOREIGN KEY (island_id) REFERENCES islands (id)
                        )
                    ''')
        
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS
                       experiences (
                       id INTEGER PRIMARY KEY,
                       island_id INTEGER,
                       experience_name TEXT,
                       time INTEGER,
                       FOREIGN KEY (island_id) REFERENCES islands (id)
                       )
                    ''')
        
        if cursor.execute('SELECT COUNT(*) from islands').fetchone()[0] == 0:
            seed_db(cursor)         
            
# seed database with data
def seed_db(cursor=None):
    if cursor is None:
        with connect_db() as cursor:
            seed_db(cursor)
            return
    
    if cursor.execute('SELECT COUNT(*) FROM resources').fetchone()[0] == 0:     # prevent duplication
        # https://en.wikipedia.org/wiki/Polynesia <- used for list of polynesian nations
        # https://en.wikipedia.org/wiki/H%C5%8Dk%C5%ABle%CA%BBa <- used for a reference of canoe capaicty  
        # [nation, latitude, longitude, population, canoes (1 canoe per 50 people), canoe capacity (4500 kg fixed)]
        islands_data = [
            ("American Samoa", -14.2710, -170.1322, 47000, 940, 4500),
            ("Cook Islands", -21.2367, -159.7777, 14000, 280, 4500),
            ("Easter Island", -27.1127, -109.3497, 8000, 160, 4500),
            ("French Polynesia", -17.6797, -149.4068, 280000, 5600, 4500),
            ("Hawaii", 19.8987, -155.6659, 1400000, 28000, 4500),
            ("New Zealand", -40.9006, 174.886, 5000000, 100000, 4500),
            ("Niue", -19.0544, -169.8672, 1800, 36, 4500),
            ("Norfolk Island", -29.0408, 167.9547, 2000, 40, 4500),
            ("Pitcairn Islands", -24.3768, -128.3242, 50, 1, 4500),
            ("Rotuma", -12.5025, 177.0724, 1600, 32, 4500),
            ("Samoa", -13.759, -172.1046, 220000, 4400, 4500),
            ("Tokelau", -9.2002, -171.8484, 2500, 50, 4500),
            ("Tonga", -21.179, -175.1982, 100000, 2000, 4500),
            ("Tuvalu", -7.1095, 177.6493, 10000, 200, 4500),
            ("Wallis and Futuna", -14.2938, -178.1165, 11000, 220, 4500)
        ]

        cursor.executemany('''
                           INSERT INTO islands (name, latitude, longitude, population, canoes, canoe_capacity) VALUES (?, ?, ?, ?, ?, ?)
                        ''', islands_data)

        # quantity of each resource is in kgs
        resources_data = [
            (1, "Taro", 8000),                  # American Samoa
            (1, "Breadfruit", 6000),
            (1, "Sea Grapes", 3000),
            (2, "Black Pearls", 500),           # Cook Islands
            (2, "Bananas", 15000),
            (2, "Coconut Oil", 8000),
            (3, "Obsidian Tools", 300),         # Easter Island
            (3, "Sweet Potatoes", 1500),
            (3, "Moai Stone Carvings", 100),
            (4, "Vanilla", 3000),               # French Polynesia
            (4, "Noni Juice", 20000),
            (4, "Mother-of-Pearl Shells", 3000),
            (5, "Coffee", 300000),              # Hawaii
            (5, "Pineapple", 250000),
            (5, "Kahelelani Shell Leis", 1000),
            (6, "Jade", 200),                   # New Zealand
            (6, "Kiwi", 50000),
            (6, "Flax", 30000),
            (7, "Honey", 5000),                 # Niue
            (7, "Coconuts", 8000),
            (7, "Limes", 3000),
            (8, "Pine Seeds", 3000),            # Norfolk Island
            (8, "Passionfruit", 2000),
            (8, "Guava", 4000),
            (9, "Arrow Root", 3000),            # Pitcairn Islands
            (9, "Sugarcane", 1500),
            (9, "Miro", 2500),
            (10, "Tava Root", 3000),            # Rotuma
            (10, "Yam Flour", 4000),
            (10, "Breadfruit Flour", 2000),
            (11, "Cocoa Beans", 20000),         # Samoa
            (11, "Tapa Cloth", 5000),
            (11, "Kava Roots", 10000),
            (12, "Pandanus Fruit", 3000),       # Tokelau
            (12, "Coconut Crab", 100),
            (12, "Driftwood Sculptures", 500),
            (13, "Casava", 3000),               # Tonga
            (13, "Mats", 6000),
            (13, "Sea Cucumbers", 4000),
            (14, "Sea Salt", 5000),             # Tuvalu    
            (14, "Pandanus Leaves", 3000),
            (14, "Taro Leaves", 2000),
            (15, "Root Vegetables", 5000),      # Wallis and Futuna
            (15, "Coral Jewelry", 100),
            (15, "Pigs", 3000),
        ]

        cursor.executemany('''
                           INSERT INTO resources (island_id, resource_name, quantity) VALUES (?, ?, ?)
                        ''', resources_data)
        
        # experiences of each island with time in hours
        experiences_data = [
            (1, "Taro Harvesting", 3),                      # American Samoa
            (1, "Dance Workshop", 2),
            (2, "Pearl Diving", 4),                         # Cook Islands
            (2, "Coconut Tasting", 3),
            (3, "Moai Tour", 5),                            # Easter Island
            (3, "Rapanui Dance", 2),
            (4, "Vanilla Tour", 3),                         # French Polynesia
            (4, "Lagoon Snorkeling", 4),
            (5, "Pineapple Tour", 4),                       # Hawaii
            (5, "Skydiving", 1),
            (6, "Maori Performance", 2),                    # New Zealand
            (6, "Mountain Hike", 8),
            (7, "Honey Harvesting", 3),                     # Niue
            (7, "Cave Exploration", 2),
            (8, "Garden Walk", 2),                          # Norfolk Island
            (8, "Bird Watching", 3),
            (9, "Wood Carving", 3),                         # Pitcairn Islands
            (9, "Island Hike", 4),
            (10, "Root Preparation", 3),                    # Rotuma
            (10, "Storytelling", 2),
            (11, "Cocoa Tour", 4),                          # Samoa
            (11, "Kava Ceremony", 2),
            (12, "Weaving Workshop", 3),                    # Tokelau
            (12, "Crab Habitat Tour", 2),
            (13, "Mats Weaving", 3),                        # Tonga
            (13, "Reef Snorkeling", 3),
            (14, "Salt Production", 2),                     # Tuvalu    
            (14, "Canoe Demo", 3),
            (15, "Jewelry Making", 3),                      # Wallis and Futuna
            (15, "Animal Sanctuary", 4),
        ]


        cursor.executemany('''
                           INSERT INTO experiences (island_id, experience_name, time) VALUES (?, ?, ?)
                        ''', experiences_data)

    
# reset database to initial state
def reset_db():
    with connect_db() as cursor:
        cursor.execute('DROP TABLE IF EXISTS resources')
        cursor.execute('DROP TABLE IF EXISTS islands')
        cursor.execute('DROP TABLE IF EXISTS experiences')
        create_db()
        seed_db(cursor)

    
# get island data
def get_islands_data():
    with connect_db() as cursor:
        cursor.execute('''
                    SELECT id, name, latitude, longitude, population, canoes, canoe_capacity FROM islands
                   ''')
        islands = []
        for row in cursor.fetchall():
            islands.append({
                'id': row[0],
                'name': row[1],
                'latitude': row[2],
                'longitude': row[3],
                'population': row[4],
                'canoes': row[5],
                'canoe_capacity': row[6]
            })
    return islands

# get resources data
def get_resources_data(island_id):
    with connect_db() as cursor:
        cursor.execute('''
                       SELECT resource_name, quantity FROM resources WHERE island_id = ?
                ''', (island_id,))
        resources = cursor.fetchall()
    return resources

# udpate island data
def update_island_data(island_id, population, canoes):
    with connect_db() as cursor:
        cursor.execute('''
                        UPDATE islands SET population = ?, canoes = ? WHERE id = ?
                    ''', (population, canoes, island_id))
        
# update resource data
def update_resource_data(island_id, resource_name, quantity):
    with connect_db() as cursor:
        cursor.execute('''
                        UPDATE resources SET quantity = ? WHERE island_id = ? AND resource_name = ?
                    ''', (quantity, island_id, resource_name))
        
# get experiences data
def get_experiences_data(island_id):
    with connect_db() as cursor:
        cursor.execute('''
                       SELECT experience_name, time FROM experiences WHERE island_id = ?
                ''', (island_id,))
        experiences = cursor.fetchall()
    return experiences

# update resource data
def update_experience_data(island_id, experience_name, time):
    with connect_db() as cursor:
        cursor.execute('''
                        UPDATE experiences SET quantity = ? WHERE island_id = ? AND experience_name = ?
                    ''', (time, island_id, experience_name))