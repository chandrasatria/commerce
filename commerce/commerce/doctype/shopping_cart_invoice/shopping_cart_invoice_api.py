import frappe

@frappe.whitelist(allow_guest=False)
def create_shopping_cart_invoice(list_shopping_cart_item=[]):
    item_to_write = frappe.get_all("Shopping Cart Invoice Item",fields="*",filters=[["name","in",list_shopping_cart_item]])
    list_item_to_write = []
    for item in item_to_write:
        list_item_to_write.append({
            "item_code" : item["item"],
            "qty" : item["qty"]
        })
        doc = frappe.get_doc({
            "doctype": "Shopping Cart Invoice",
            "customer" : get_customer(),
            "items": list_item_to_write
        })
        doc.save(ignore_permissions=True)
        item_to_write

def get_customer():
    customer_name = frappe.get_value("Customer",{"user_id" : frappe.session.user},"name")
    return customer_name