import frappe
from frappe.utils.background_jobs import enqueue

def before_save(doc, method):
    if not doc.user:
        doc.user = frappe.session.user

def after_insert(doc,method):
    if doc.reference_doctype == "Item" and doc.reference_name:
        enqueue("commerce.doctype_function.log_document_view.enqueue_calculate_seen", item=doc.reference_name)


# Ini untuk nghitung dan ngasih last_view
def enqueue_calculate_seen(item):
    variant_of = ""
    doc_item = frappe.get_doc("Item", item)
    if doc_item.get("variant_of"):
        variant_of = doc_item.get("variant_of")
    if not doc_item.get("seen"):
            doc_item.seen = 0
    doc_item.seen += int(1)
    doc_item.last_seen = frappe.utils.now()
    doc_item.save(ignore_permissions =True)
    frappe.db.commit()

    if variant_of:
        doc_item = frappe.get_doc("Item", item)
        if not doc_item.get("seen"):
            doc_item.seen = 0
        doc_item.seen += int(1)
        doc_item.last_seen = frappe.utils.now()
        doc_item.save(ignore_permissions =True)
        frappe.db.commit()



