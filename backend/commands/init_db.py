import sqlite3

# Create or connect to the database
conn = sqlite3.connect("truck_status.db")
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

print("truck_status.db created and populated.")
