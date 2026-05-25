from langchain_core.tools import tool
from db_helper import search_complaint, register_pending_complaint

@tool
def search_complaint_tool(order_id: str) -> str:
    """
    Search for an existing complaint (processed or pending) by order ID.
    Returns a user‑friendly summary.
    """
    result = search_complaint(order_id)
    status = result.get("status")

    if status == "PROCESSED":
        return (
            f"✅ Complaint for order {result['order_id']} has been processed.\n"
            f"Decision: {result['decision']}\n"
            f"Reason: {result['reason']}\n"
            f"Delivery date: {result['delivery_date']}\n"
            f"Claim date: {result['claim_date']}\n"
            f"Days lapsed: {result['n_days_lapsed']}"
        )
    elif status == "PENDING":
        return (
            f"⏳ Complaint for order {result['order_id']} is pending review.\n"
            f"Submitted on: {result['created_at']}\n"
            f"Expected resolution within {result['TAT_days']} days (by {result['due_date']})."
        )
    elif status == "NOT_FOUND":
        return f"No complaint found for order ID {order_id}."
    else:  # ERROR
        return f"⚠️ {result.get('user_message', 'Technical error occurred.')}"

@tool
def register_pending_complaint_tool(order_id: str, complaint_raw_text: str) -> str:
    """
    Register a new complaint into the pending queue.
    """
    result = register_pending_complaint(order_id, complaint_raw_text)
    if result.get("status") == "SUCCESS":
        return (
            f"✅ Complaint for order {order_id} has been registered.\n"
            f"Registration time: {result['created_at']}\n"
            f"We will resolve it within {result['TAT_days']} days (by {result['due_date']})."
        )
    else:
        return f"⚠️ {result.get('user_message', 'Failed to register complaint.')}"

tools = [search_complaint_tool, register_pending_complaint_tool]