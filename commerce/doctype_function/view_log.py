import frappe

def after_insert(self, method):
    if self.get("reference_doctype") == "Item":
        if self.get("reference_name"):
            update_item_last_seen_and_qty(self.get("reference_name"), frappe.utils.now())
            variant_parent = get_parent_item(self.get("reference_name"))
            if variant_parent:
                update_item_last_seen_and_qty(variant_parent, frappe.utils.now())
        
def get_parent_item(item):
    variant_of = frappe.get_value("Item",item,"variant_of")
    return variant_of

def update_item_last_seen_and_qty(item, now):
    frappe.db.sql("""UPDATE `tabItem` SET last_seen = '{now}', seen = seen+1 WHERE name = %(item)s """.format(now=now),{"item" : item})
    frappe.db.commit()