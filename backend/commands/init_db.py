import sqlite3

# Create or connect to the database
conn = sqlite3.connect("logistics.db")
cursor = conn.cursor()

# Create the table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS trucks (
        truck_code TEXT PRIMARY KEY,
        truck_status TEXT NOT NULL
    )
    """
)

cursor.executescript(
    """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS transports_goods (
        customer_id TEXT PRIMARY KEY,
        transports_goods BOOLEAN,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    CREATE TABLE IF NOT EXISTS transport_route (
        customer_id TEXT PRIMARY KEY,
        route_from TEXT,
        route_to TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    CREATE TABLE IF NOT EXISTS transport_mode (
        customer_id TEXT PRIMARY KEY,
        transport_mode TEXT CHECK(transport_mode IN ('own', 'partner', 'service')),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    CREATE TABLE IF NOT EXISTS transport_weight (
        customer_id TEXT PRIMARY KEY,
        weight_kg REAL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    """
)

# Dummy data
data = [
    ("T001", "loading"),
    ("T002", "intransit"),
    ("T003", "delivered"),
    ("T004", "delayed"),
    ("T005", "at_warehouse"),
    ("T006", "intransit"),
    ("T007", "loading"),
    ("T008", "under_maintenance"),
    ("T009", "delivered"),
    ("T010", "awaiting_dispatch"),
]

# Insert data
cursor.executemany(
    "INSERT OR REPLACE INTO trucks (truck_code, truck_status) VALUES (?, ?)", data
)

# Commit and close
conn.commit()
conn.close()

print("logistics.db created and populated.")
