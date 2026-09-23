from mcp.server import MCPServer

mcp = MCPServer("Order Support Server")

# Fake Database

ORDERS = {
    "ORD-101": {
        "customer": "John",
        "product": "Laptop",
        "price": 1200,
        "status": "delivered",
        "days_since_delivery": 5,
    },

    "ORD-102": {
        "customer": "Emma",
        "product": "Headphones",
        "price": 150,
        "status": "delivered",
        "days_since_delivery": 35,
    },

    "ORD-103": {
        "customer": "David",
        "product": "Monitor",
        "price": 400,
        "status": "shipped",
        "days_since_delivery": 0,
    },
}


SUPPORT_NOTES = []

@mcp.tool()
def get_order_status(order_id: str) -> dict:
    """ Get information about an order. """

    order = ORDERS.get(order_id)

    if not order:
        return {
            "found": False,
            "message": f"Order {order_id} not found."
        }

    return {
        "found": True,
        "order_id": order_id,
        **order
    }


@mcp.tool()
def check_refund_eligibility(order_id) -> dict:
    """
    Check whether an order can be refunded.

    Refund policy:
    - Order must already be delivered.
    - Refund request must be within 30 days.
    """

    order = ORDERS.get(order_id)

    if not order:
        return {
            "eligible": False,
            "reason": f"Order not found."
        }

    if order["status"] != "delivered":
        return {
            "eligible": False,
            "reason": f"Order  has not been delivered yet."
        }

    if order["days_since_delivery"] > 30:
        return {
            "eligible": False,
            "reason": f"Refund request must be within 30 days."
        }

    return {
        "eligible": True,
        "refund_amount": order["price"],
        "reason": "Refund eligible."
    }


@mcp.tool()
def create_suppport_note(order_id: str, note: str) -> dict:
    """ Create a support note for an order. """

    if order_id not in ORDERS:
        return {
            "success": False,
            "message": f"Order {order_id} not found."
        }

    support_note = {
        "order_id": order_id,
        "note": note,
    }

    SUPPORT_NOTES.append(support_note)

    return {
        "success": True,
        "message": "Support note created successfully."
    }


if __name__ == "__main__":
    mcp.run()

