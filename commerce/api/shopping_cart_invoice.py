import frappe
import requests
import json
import sys
from frappe import _

from api_integration.validation import success_format, error_format

""" contoh item = [
	{"item_code" :"X","qty":1,"uom":2000}
]

customer = customer

"""
@frappe.whitelist(allow_guest=False)
def create_shopping_cart_invoice_by_item():
	try:
		post = json.loads(frappe.request.data.decode('utf-8'))
		
		# Check data
		if "platform" in post:
			platform = post["platform"] or "Website"
		else:
			platform = "Website"

		if "item" in post:
			if not post["item"]:
				frappe.throw(_("Please insert item"))

		customer_name = get_customer()
		if not customer_name:
			frappe.throw(_("Customer not found"))			


		# Create item
		item_to_write = post["item"]
		list_item_to_write = []
		for item_i in item_to_write:
			if "item_code" in item_i:
				list_item_to_write = item_i["item_code"]
		# list_item_to_write = [ x["item_code"] for x in item_to_write if "item_code" in x ]

		if not list_item_to_write:
			frappe.throw(_("Sorry something went wrong, please try again later."))
		
		# Create item to append
		sql_result = frappe.db.sql("""SELECT parent as item_code,conversion_factor,uom 
		FROM `tabUOM Conversion Detail` 
		WHERE parent IN (%(list_item_to_write)s) """,{
			"list_item_to_write" : list_item_to_write
		},as_dict=True)
		result_item = sql_list_to_dict_two_key(sql_result,"item_code","uom")

		shopping_cart_item = []
		for item in item_to_write:
			key_itemcode_itemuom = item["item_code"] + "_" + item["uom"]
			conv_uom = result_item[key_itemcode_itemuom]["conversion_factor"]
			shopping_cart_item.append({
				"item_code" : item["item_code"],
				"qty" : float(item["qty"]),
				"uom" : item["uom"],
				"conversion_uom" : conv_uom
			})

		print(shopping_cart_item)

		# Insert to Shopping Cart Invoice
		customer_info = get_customer_group()
		doc = frappe.get_doc({
			"doctype": "Shopping Cart Invoice",
			"platform" : platform,
			"customer" : customer_name,
			"items": shopping_cart_item,
			"customer_group" : customer_info[0],
			"price_list" : customer_info[1]
		})
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		return success_format(doc)
	except:
		frappe.log_error(frappe.get_traceback(),"Error: API create_shopping_cart_invoice_by_item")
		return error_format(sys.exc_info())

# Helper create shopping cart invoice

def get_customer():
	customer_name = frappe.get_value("Customer",{"email_id" : frappe.session.user},"name")
	return customer_name

def get_customer_group():
	customer_group = frappe.get_value("Customer",{"email_id": frappe.session.user },"customer_group")
	default_price_list = ""
	if customer_group:
		fga_customer_group = frappe.get_all("Customer Group",fields="default_price_list",filters=[["name","=",customer_group]])
		if len(fga_customer_group)>0:
			default_price_list = fga_customer_group[0]["default_price_list"]
	return customer_group,default_price_list

def sql_list_to_dict_two_key(sql_item,key1,key2):
	some_dict= {}
	for item in sql_item:
		identifier = item.get(key1)+"_"+item.get(key2)
		some_dict[identifier] = item
	return some_dict