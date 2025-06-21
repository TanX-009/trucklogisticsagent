from database import (
    insert_transport_weight,
    insert_transports_goods,
    insert_transport_route,
    insert_transport_mode,
    truck_status,
)


def get_truck_status(truck_code: str) -> str:
    return truck_status(truck_code)


get_truck_status_tool = {
    "type": "function",
    "function": {
        "name": "get_truck_status",
        "description": "Get status of truck from database",
        "parameters": {
            "type": "object",
            "required": ["truck_code"],
            "properties": {
                "truck_code": {"type": "string", "description": "The truck code"},
            },
        },
    },
}


available_functions = {
    "get_truck_status": get_truck_status,
}

enquiry_agent_tools = [get_truck_status_tool]

enquiry_agent_tool_kit = {
    "tools": enquiry_agent_tools,
    "available_functions": available_functions,
}


# leadfinder agent tools


insert_transports_goods_tool = {
    "type": "function",
    "function": {
        "name": "insert_transports_goods",
        "description": "Record whether the customer currently transports goods.",
        "parameters": {
            "type": "object",
            "required": ["customer_id", "transports_goods"],
            "properties": {
                "customer_id": {"type": "string"},
                "transports_goods": {"type": "boolean"},
            },
        },
    },
}

insert_transport_route_tool = {
    "type": "function",
    "function": {
        "name": "insert_transport_route",
        "description": "Record the source and destination of goods transport.",
        "parameters": {
            "type": "object",
            "required": ["customer_id", "route_from", "route_to"],
            "properties": {
                "customer_id": {"type": "string"},
                "route_from": {"type": "string"},
                "route_to": {"type": "string"},
            },
        },
    },
}

insert_transport_mode_tool = {
    "type": "function",
    "function": {
        "name": "insert_transport_mode",
        "description": "Record the mode of transport used by the customer (own, partner, service).",
        "parameters": {
            "type": "object",
            "required": ["customer_id", "transport_mode"],
            "properties": {
                "customer_id": {"type": "string"},
                "transport_mode": {
                    "type": "string",
                    "enum": ["own", "partner", "service"],
                },
            },
        },
    },
}

insert_transport_weight_tool = {
    "type": "function",
    "function": {
        "name": "insert_transport_weight",
        "description": "Record the amount of goods (in kg) transported by the customer.",
        "parameters": {
            "type": "object",
            "required": ["customer_id", "weight_kg"],
            "properties": {
                "customer_id": {"type": "string"},
                "weight_kg": {
                    "type": "number",
                    "description": "Weight in kilograms (kg)",
                },
            },
        },
    },
}

available_functions = {
    "insert_transports_goods": insert_transports_goods,
    "insert_transport_route": insert_transport_route,
    "insert_transport_mode": insert_transport_mode,
    "insert_transport_weight": insert_transport_weight,
}

leadfinder_agent_tools = [
    insert_transports_goods_tool,
    insert_transport_route_tool,
    insert_transport_mode_tool,
    insert_transport_weight_tool,
]
leadfinder_agent_tool_kit = {
    "tools": leadfinder_agent_tools,
    "available_functions": available_functions,
}
