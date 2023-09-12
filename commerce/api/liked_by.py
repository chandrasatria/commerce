import frappe
from api_integration.validation import success_format, error_format
from frappe import _

# https://erp.wijayasuperstore.com/api/method/frappe.desk.like.toggle_like

@frappe.whitelist(allow_guest=False)
def toggle_like_api():
    import json
    req = json.loads(frappe.request.data.decode("UTF-8"))
    doctype =req["doctype"]
    name = req["name"]
    add = req["add"] or "Yes"
    from frappe.desk.like import toggle_like
    try:
        resp = toggle_like(doctype=doctype,name=name, add=add)
        return success_format(resp)
    except:
        frappe.log_error(frappe.get_traceback(),"Error: toggle_like_api")
        return error_format(_("Something went wrong. Please try again in a few minutes"))
        
    
    