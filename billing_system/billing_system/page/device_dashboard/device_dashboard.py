import frappe
import json
from frappe import _

@frappe.whitelist(allow_guest=True)  # Allow public access without authentication
def receive_mikrotik_data():
    """
    This method receives data from Mikrotik's webhook and processes it.
    """
    try:
        # Get JSON data from the request
        data = frappe.request.get_json()
        
        # Check if data is received
        if data:
            print(data)
            # For now, simply return the data (you can also process it as needed)
            frappe.publish_realtime(event="mikrotik_data", message=data)
            return {"status": "success", "message": "Data received", "data": data}
        else:
            return {"status": "error", "message": "No data received"}

    except Exception as e:
        frappe.log_error(message=str(e), title="Mikrotik Webhook Error")
        return {"status": "error", "message": str(e)}
