
import frappe
from frappe import _
from frappe.model.document import Document

def after_insert(doc, method):
	doc_sc = frappe.get_doc("Shopping Cart",doc.parent)
	doc_sc.save(ignore_permissions=True)

