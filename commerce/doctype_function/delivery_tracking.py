
import frappe
from frappe import _
from frappe.model.document import Document

def after_insert(self,method):
    if self.status == "Delivered" and self.external_doctype == "Sales Invoice" and self.external_id:
        doc = frappe.get_doc(self.external_doctype,self.external_id)
        if doc.shipping_status == "Shipped":
            doc.shipping_status = "Completed"
            doc.save(ignore_permissions=True)