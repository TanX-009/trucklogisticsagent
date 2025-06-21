import sqlite3
from uuid import uuid4


DB_PATH = "logistics.db"


def insert_lead(transports_goods, route_from, route_to, transport_mode):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO logistics_leads (transports_goods, route_from, route_to, transport_mode)
        VALUES (?, ?, ?, ?)
    """,
        (transports_goods, route_from, route_to, transport_mode),
    )
    conn.commit()
    conn.close()


def insert_partial_lead(
    transports_goods=None, route_from=None, route_to=None, transport_mode=None
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO logistics_leads (transports_goods, route_from, route_to, transport_mode)
        VALUES (?, ?, ?, ?)
    """,
        (transports_goods, route_from, route_to, transport_mode),
    )
    conn.commit()
    conn.close()
    return "Lead saved successfully."


def create_customer() -> str:
    customer_id = str(uuid4())
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (customer_id) VALUES (?)", (customer_id,))
    conn.commit()
    conn.close()
    return customer_id


def insert_transports_goods(customer_id: str, transports_goods: bool):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO transports_goods (customer_id, transports_goods)
        VALUES (?, ?)
    """,
        (customer_id, transports_goods),
    )
    conn.commit()
    conn.close()
    return (
        f"Inserted {customer_id}, {transports_goods} into transports_goods successfully"
    )


def insert_transport_route(customer_id: str, route_from: str, route_to: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO transport_route (customer_id, route_from, route_to)
        VALUES (?, ?, ?)
    """,
        (customer_id, route_from, route_to),
    )
    conn.commit()
    conn.close()
    return f"Inserted {customer_id}, {route_from}, {route_to} into transport_route successfully"


def insert_transport_mode(customer_id: str, transport_mode: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO transport_mode (customer_id, transport_mode)
        VALUES (?, ?)
    """,
        (customer_id, transport_mode),
    )
    conn.commit()
    conn.close()
    return f"Inserted {customer_id}, {transport_mode} into transport_mode successfully"


def insert_transport_weight(customer_id: str, weight_kg: float):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO transport_weight (customer_id, weight_kg)
        VALUES (?, ?)
    """,
        (customer_id, weight_kg),
    )
    conn.commit()
    conn.close()
    return f"Inserted {customer_id}, {weight_kg} into transport_weight successfully"
