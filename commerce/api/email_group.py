import frappe
from api_integration.validation import success_format, error_format
from frappe import _

@frappe.whitelist(allow_guest=True)
def subscribe_email_group():
    import json
    ignore_permissions= False
    req = json.loads(frappe.request.data.decode("UTF-8"))
    if req:
        email_list = req["email_list"] or ""
        name = req["name"] or ""
        if not email_list:
            return error_format(_("Email Address cannot be empty."))
        from frappe.email.doctype.email_group.email_group import add_subscribers
        if not name:
            fga_email_group = frappe.get_all("Email Group",fields="name")
            if len(fga_email_group)>0:
                name = fga_email_group[0]["name"]
        if not name:
            frappe.log_error(frappe.get_traceback(),"Error Email Group not set")
            return error_format(_("Something went wrong. Please try again in a few minutes"))
        
        resp_check_email = check_email(email_list)
        if not resp_check_email:
            return error_format(_("Please input a valid Email Address"))

        try:
            resp_add_subsribers = add_subscribers(name=name, email_list=email_list)
            return success_format(resp_add_subsribers)
        except:
            frappe.log_error(frappe.get_traceback(),"Error: API When adding Subscriber")
            return error_format(_("Something went wrong. Please try again in a few minutes"))
    return error_format(_("Please input email_list and name"))
        
# Helper

def check_email(email):
    import re
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return True
    else:
        return False
    
    