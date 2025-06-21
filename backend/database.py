import sqlite3
from uuid import uuid4


DB_PATH = "logistics.db"


def truck_status(truck_code: str) -> str:
    """
    Get status of truck from database

    Args:
      truck_code (str): The truck code

    Returns:
      str: Current status of the truck
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT truck_status FROM trucks WHERE UPPER(truck_code) = ?",
        (truck_code.strip().upper(),),
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    return "No status found for this truck."


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


def get_all_truck_statuses():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT truck_code, truck_status FROM trucks")
    rows = cursor.fetchall()
    conn.close()
    return [{"truck_code": code, "truck_status": status} for code, status in rows]


def get_transport_details(customer_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT transports_goods FROM transports_goods WHERE customer_id = ?",
        (customer_id,),
    )
    transports_goods = cursor.fetchone()

    cursor.execute(
        "SELECT route_from, route_to FROM transport_route WHERE customer_id = ?",
        (customer_id,),
    )
    route = cursor.fetchone()

    cursor.execute(
        "SELECT transport_mode FROM transport_mode WHERE customer_id = ?",
        (customer_id,),
    )
    mode = cursor.fetchone()

    cursor.execute(
        "SELECT weight_kg FROM transport_weight WHERE customer_id = ?", (customer_id,)
    )
    weight = cursor.fetchone()

    conn.close()

    return {
        "customer_id": customer_id,
        "transports_goods": transports_goods[0] if transports_goods else None,
        "route_from": route[0] if route else None,
        "route_to": route[1] if route else None,
        "transport_mode": mode[0] if mode else None,
        "weight_kg": weight[0] if weight else None,
    }


def get_all_transport_details():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT 
        c.customer_id,
        tg.transports_goods,
        tr.route_from,
        tr.route_to,
        tm.transport_mode,
        tw.weight_kg
    FROM customers c
    LEFT JOIN transports_goods tg ON c.customer_id = tg.customer_id
    LEFT JOIN transport_route tr ON c.customer_id = tr.customer_id
    LEFT JOIN transport_mode tm ON c.customer_id = tm.customer_id
    LEFT JOIN transport_weight tw ON c.customer_id = tw.customer_id
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append(
            {
                "customer_id": row[0],
                "transports_goods": row[1],
                "route_from": row[2],
                "route_to": row[3],
                "transport_mode": row[4],
                "weight_kg": row[5],
            }
        )
    return result
