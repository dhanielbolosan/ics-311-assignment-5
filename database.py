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
        
        if cursor.execute('SELECT COUNT(*) from islands').fetchone()[0] == 0:
            seed_db(cursor)         
            
# seed database with data
def seed_db(cursor=None):
    if cursor is None:
        with connect_db() as cursor:
            seed_db(cursor)

            return
    
    islands_data = [
                ("Hawaii", 19.8987, -155.6659, 1400000, 500, 500),
                ("Rapanui", -27.1127, -109.3497, 8000, 10, 500),
                ("New Zealand", -40.9006, 174.886, 5000000, 1000, 500),
                ("Samoa", -13.759, -172.1046, 200000, 250, 500),
                ("Tonga", -21.179, -175.1982, 100000, 150, 500),
            ]

    cursor.executemany('''
                       INSERT INTO islands (name, latitude, longitude, population, canoes, canoe_capacity) VALUES (?, ?, ?, ?, ?, ?)
                    ''', islands_data)

    # quantity of each resource is in pounds
    # ex. 1000 kg of coffee in Hawaii
    resources_data = [
                (1, "Coffee", 1000),    # Hawaii
                (2, "Pineapple", 50),   # Rapanui
                (3, "Kiwi", 250),       # New Zealand
                (4, "Coconut", 100),    # Samoa
                (5, "Fish", 750)        # Tonga
            ]

    cursor.executemany('''
                       INSERT INTO resources (island_id, resource_name, quantity) VALUES (?, ?, ?)
                    ''', resources_data)
    
# reset database to initial state
def reset_db():
    with connect_db() as cursor:
        cursor.execute('DROP TABLE IF EXISTS resources')
        cursor.execute('DROP TABLE IF EXISTS islands')
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