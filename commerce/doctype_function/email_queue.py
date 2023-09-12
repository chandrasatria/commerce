import frappe

def after_insert(doc,method):
    try:
        from frappe.email.doctype.email_queue.email_queue import send_now
        send_now(doc.name)
    except:
        frappe.log_error(frappe.get_traceback(),"Error: Email Queue Send Now")