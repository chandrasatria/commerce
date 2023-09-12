
import frappe
from frappe import _
from frappe.model.document import Document

def before_save(self,method):
    if not self.valid_from:
        self.valid_from = frappe.utils.now()

def on_update(self, method):
    pass
    # NOTE ini karena sudah ngga pake master data item_price di Doctype Item 
    # if not self.customer:
    #     doc = frappe.get_doc("Item", self.item_code)
    #     doc.item_price = self.price_list_rate
    #     doc.save(ignore_permissions=True)
    #     frappe.db.commit()
        # frappe.msgprint("{}".format(self.item_code))
        # if doc.variant_of:
        #     doc_parent = frappe.get_doc("Item", doc.variant_of)
        #     sql = frappe.db.sql("SELECT min(item_price) as min_ip FROM `tabItem` WHERE variant_of = '{}' ".format(doc.variant_of),as_dict=True)
        #     if len(sql) > 0: 
        #         doc_parent.item_price = sql[0]["min_ip"]
        #         doc_parent.save(ignore_permissions=True)
            # frappe.get_all("Item",fields="item_price",filters=[["variant_of","=",doc.variant_of]])
        
