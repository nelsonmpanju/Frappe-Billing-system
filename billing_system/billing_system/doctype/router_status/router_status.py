# Copyright (c) 2024, iota technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now_datetime
from frappe.model.document import Document

class RouterStatus(Document):
    pass

@frappe.whitelist(allow_guest=True)
def update_router_status():
    """Webhook function to update router status when new data is received."""
    try:
        # Parse incoming data (assuming it's JSON)
        data = frappe.local.form_dict

        # Extract the router name (or use another unique identifier if necessary)
        router_name = data.get('router_name')

        if not router_name:
            log_error("Router name is required", data)
            return {"status": "failed", "message": "Router name is required"}

        # Fetch the existing Router Status record for the given router
        router_status = frappe.get_doc("Router Status", {"router_name": router_name})

        if not router_status:
            log_error(f"Router status record not found for router: {router_name}", data)
            return {"status": "failed", "message": f"Router status record not found for router: {router_name}"}

        # Update the fields with the incoming data from the webhook
        router_status.active_users = data.get('activeUsers', router_status.active_users)
        router_status.uptime = data.get('uptime', router_status.uptime)
        router_status.cpu_load = data.get('cpuLoad', router_status.cpu_load)
        router_status.health = data.get('health', router_status.health)
        router_status.memory = data.get('memory', router_status.memory)
        router_status.hdd = data.get('hdd', router_status.hdd)
        router_status.tx_speed = data.get('tx_speed', router_status.tx_speed)
        router_status.rx_speed = data.get('rx_speed', router_status.rx_speed)

        # Set the last update timestamp
        router_status.last_update = now_datetime()

        # If the last update is older than 5 minutes, mark it as outdated
        time_diff = (now_datetime() - router_status.last_update).total_seconds() / 60.0
        router_status.outdated = 1 if time_diff > 5 else 0

        # Save the updated router status
        router_status.save(ignore_permissions=True)
        frappe.db.commit()  # Commit the transaction to save changes

        return {"status": "success", "message": "Router status updated successfully"}

    except Exception as e:
        # Log the error in the Error Log doctype
        log_error(str(e), data)
        return {"status": "failed", "message": "An error occurred while updating router status"}

def log_error(error_message, data):
    """Helper function to log errors into the Error Log doctype."""
    frappe.log_error(f"Error in update_router_status: {error_message}", "Router Status Webhook Error")
    # Log detailed error message and the incoming data for debugging
    frappe.get_doc({
        "doctype": "Error Log",
        "error": error_message,
        "method": "update_router_status",
        "stack_trace": frappe.get_traceback(),
        "context": str(data)
    }).insert(ignore_permissions=True)
