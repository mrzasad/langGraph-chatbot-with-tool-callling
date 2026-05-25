from langchain_core.tools import tool
from db_helper import search_complaint, register_pending_complaint

@tool
def search_complaint_tool(order_id: str) -> str:
    """
    Search for an existing complaint in the processed or pending queue using the order ID.
    Use this when the customer asks about a specific complaint or order status.
    """
    result = search_complaint(order_id)
    status = result.get("status")
    
    if status == "PROCESSED":
        return f"✅ COMPLAINT FOUND (PROCESSED):\nOrder: {result['order_id']}\nDecision: {result['decision']}\nReason: {result['reason']}\nDelivery: {result['delivery_date']}\nClaim: {result['claim_date']}\nDays Lapsed: {result['n_days_lapsed']}"
    elif status == "PENDING":
        return f"⏳ COMPLAINT FOUND (PENDING):\nOrder: {result['order_id']}\nSubmitted: {result['created_at']}\nStatus: Under review. Will be resolved within {result['TAT_days']} days (by {result['due_date']})."
    elif status == "NOT_FOUND":
        return f"❌ NO COMPLAINT FOUND for order ID: {order_id}"
    else:
        return f"⚠️ ERROR: {result.get('user_message', 'Technical issue')}"

@tool
def register_pending_complaint_tool(order_id: str, complaint_raw_text: str) -> str:
    """
    Register a new complaint into the pending queue.
    Use this when the customer wants to file or register a new complaint.
    """
    result = register_pending_complaint(order_id, complaint_raw_text)
    if result.get("status") == "SUCCESS":
        return f"✅ COMPLAINT REGISTERED SUCCESSFULLY:\nOrder: {order_id}\nRegistered at: {result['created_at']}\nResolution within: {result['TAT_days']} days (by {result['due_date']})"
    else:
        return f"⚠️ REGISTRATION FAILED: {result.get('user_message', 'Unknown error')}"

tools = [search_complaint_tool, register_pending_complaint_tool]