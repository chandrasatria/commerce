import frappe
import requests
import json
import sys
from frappe import _

from api_integration.validation import success_format, error_format
# from api_integration.api_integration.request import record_api


@frappe.whitelist(allow_guest=True)
def getVersion():
	return frappe.utils.change_log.get_versions()['titan']['version']


# SECTION Ongkir (shipping fee)

@frappe.whitelist(allow_guest=False)
def get_province():
	api_key = frappe.get_single("Titan Settings").get("titan_istore_api_key")
	headers = {"API-KEY" : api_key}
	r = requests.get("https://titanistore.com/backend/api/mobile/v1/master/province",headers=headers)
	print(r.text)
	if r.status_code == 200:
		res = r.json()
		response = []
		for item in res["result"]["data"]:
			response_dict={}
			response_dict["id"] = item["id"]
			response_dict["name"] = item["nama"]
			response.append(response_dict)
		
		return success_format(response)
	else:
		return error_format(response)

@frappe.whitelist(allow_guest=False)
def get_city(province=1):
	api_key = frappe.get_single("Titan Settings").get("titan_istore_api_key")
	headers = {"API-KEY" : api_key}
	r = requests.get("https://titanistore.com/backend/api/mobile/v1/master/city?province={}".format(province),headers=headers)
	print(r.text)
	if r.status_code == 200:
		res = r.json()
		response = []
		for item in res["result"]["data"]:
			response_dict={}
			response_dict["id"] = item["id"]
			response_dict["province_id"] = item["id_provinsi"]
			response_dict["name"] = item["nama"]
			response.append(response_dict)
		
		return success_format(response)
	else:
		return error_format(response)


@frappe.whitelist(allow_guest=False)
def get_district(city=1):
	api_key = frappe.get_single("Titan Settings").get("titan_istore_api_key")
	headers = {"API-KEY" : api_key}
	r = requests.get("https://titanistore.com/backend/api/mobile/v1/master/district?city={}".format(city),headers=headers)
	print(r.text)
	if r.status_code == 200:
		res = r.json()
		response = []
		for item in res["result"]["data"]:
			response_dict={}
			response_dict["sicepat"] = item["kode_sicepat"]
			response_dict["jne"] = item["kode_jne"]
			response_dict["name"] = item["nama"]
			response_dict["id_kota"] = item["id_kota"]
			response_dict["id_kecamatan"] = item["id_kecamatan_asli"]
			response.append(response_dict)
		
		return success_format(response)
	else:
		return error_format(response)

# !SECTION

# SECTION Shopping Cart

@frappe.whitelist(allow_guest=False)
def create_shopping_cart_invoice(shopping_cart="",platform="Website"):
	try:
		# post = json.loads(frappe.request.data.decode('utf-8'))
		# item_to_write = frappe.get_all("Shopping Cart Item",fields="*",filters=[["unique_id","in",post["list_shopping_cart_item"]]])
		# print(item_to_write)
		if not shopping_cart:
			shopping_cart = frappe.session.user
		print(shopping_cart)
		if not frappe.get_value("Shopping Cart", shopping_cart, "name"):
			return error_format("Shopping Cart not found.")
		else:
			fga_shopping_cart = frappe.get_all("Shopping Cart",fields="name,sales_person",filters=[["name","=",shopping_cart]])
		item_to_write = frappe.get_list("Shopping Cart Item",fields="*",filters=[["parent","=", shopping_cart ],["is_selected","=",1]])
		if not item_to_write:
			return error_format("Please select an item.")
		list_item_to_write = []
		print(item_to_write)
		for item in item_to_write:
			# Ini update jika conversion uom e 0 maka jadi 1
			if item["conversion_uom"] == 0:
				item["conversion_uom"] = 1
			list_item_to_write.append({
				"item_code" : item["item"],
				"qty" : item["qty"],
				"uom" : item["uom"],
				"conversion_uom" : item["conversion_uom"]
			})

		
		customer_info = get_customer_group()
		doc = frappe.get_doc({
			"doctype": "Shopping Cart Invoice",
			"platform" : platform,
			"sales_person" : fga_shopping_cart[0]["sales_person"],
			"customer" : get_customer(),
			"items": list_item_to_write,
			"customer_group" : customer_info[0],
			"price_list" : customer_info[1]
		})
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		return success_format(doc)
	except:
		frappe.log_error(frappe.get_traceback(),"Error: api create_shopping_cart_invoice")
		return error_format(sys.exc_info())

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

	


@frappe.whitelist(allow_guest=False)
def shopping_cart_pay(shopping_cart_invoice):
	frappe.log_error(frappe.get_traceback(),"Error: list_all_delivery")
	return success_format("Maaf silahkan kontak admin mengenai hal ini")
	doc_shopping_cart_invoice = frappe.get_doc("Shopping Cart Invoice",shopping_cart_invoice)
	if doc_shopping_cart_invoice.get("sales_invoice"):
		doc_voucher = frappe.get_doc("Sales Invoice", doc_shopping_cart_invoice.get("sales_invoice") )
		return success_format(doc_voucher)
	data_item=[]
	for item in doc_shopping_cart_invoice.get("items"):
		data_item.append({ 
			"item_code":item.get("item_code"),
			"qty": item.get("qty"),
			"stock_uom": "Nos",
			"uom": "Nos",
			"conversion_factor": 1.0,
			"stock_qty": item.get("qty"),
			"doctype": "Sales Invoice Item"
			})

	data_taxes_and_charges = []
	
	# STUB Shipping fee
	if doc_shopping_cart_invoice.get("shipping_fee"):
		shipping_fee_account = frappe.get_value("Sales Taxes and Charges Settings","Sales Taxes and Charges Settings","shipping_fee_account")
		if not shipping_fee_account:
			frappe.throw("Please set up Sales Taxes and Charges Settings.")
		data_taxes_and_charges.append({       
			"charge_type": "Actual",
			"account_head": shipping_fee_account,
			"description": "Shipping Fee",
			"cost_center": "Main - T",
			"tax_amount": doc_shopping_cart_invoice.get("shipping_fee"),
			"doctype": "Sales Taxes and Charges"
		})
	# STUB Payment Fee
	if doc_shopping_cart_invoice.get("payment_fee"):
		admin_fee_account = frappe.get_value("Sales Taxes and Charges Settings","Sales Taxes and Charges Settings","admin_fee_account")
		if not admin_fee_account:
			frappe.throw("Please set up Sales Taxes and Charges Settings.")
		data_taxes_and_charges.append({       
			"charge_type": "Actual",
			"account_head": admin_fee_account,
			"description": "Payment Fee",
			"cost_center": "Main - T",
			"tax_amount": doc_shopping_cart_invoice.get("payment_fee"),
			"doctype": "Sales Taxes and Charges"
		})

	data = {
		"naming_series": "ACC-SINV-.YYYY.-",
		"company": doc_shopping_cart_invoice.get("company"),
		"posting_date": frappe.utils.now(),
		"customer":  doc_shopping_cart_invoice.get("customer"),
		"due_date":  doc_shopping_cart_invoice.get("posting_date"),
		"currency": "IDR",
		"conversion_rate": 1.0,
		"selling_price_list": "Standard Selling",
		"price_list_currency": "IDR",
		"plc_conversion_rate": 1.0,
		"notes" :  doc_shopping_cart_invoice.get("note"),
		"items": data_item,
		"taxes" : data_taxes_and_charges,
		"doctype": "Sales Invoice"
	}

	if doc_shopping_cart_invoice.get("total_discount"):
		data.update({       
			"apply_discount_on": "Grand Total",
			"discount_amount": doc_shopping_cart_invoice.get("total_discount"),
		})

	doc = frappe.get_doc(data)
	doc.save(ignore_permissions=True)
	if doc.grand_total != doc_shopping_cart_invoice.grand_total:
		return error_format(_("Kesalahan pada server. Silahkan coba lagi beberapa saat"))
	frappe.db.commit()
	frappe.db.sql("UPDATE `tabShopping Cart Invoice` SET sales_invoice = '{sales_invoice}' WHERE name = '{shopping_cart_invoice}' "
	.format(sales_invoice = doc.name, shopping_cart_invoice = shopping_cart_invoice))
	frappe.db.commit()

	doc_to_unpaid = frappe.get_doc("Sales Invoice",doc.name)
	doc_to_unpaid.docstatus = 1
	doc_to_unpaid.save(ignore_permissions =True)
	frappe.db.commit()
	return doc_to_unpaid
	# return success_format(doc_to_unpaid)
	# except:
	#     return error_format(sys.exc_info())

# !SECTION
@frappe.whitelist(allow_guest=False)
def check_voucher():
	from commerce.voucher.doctype.my_voucher.my_voucher import check_valid_my_voucher
	# Ini ga mungkin terjadi kalo by sistem

	req = frappe.request.data.decode("UTF-8")
	import json
	req = json.loads(req)
	voucher = req.get("voucher", None)
	shopping_cart_invoice = req.get("shopping_cart_invoice", None)
	if not voucher:
		return error_format(_("Voucher need to be filled."))
	if not shopping_cart_invoice:
		return error_format(_("Shopping Cart Invoice need to be filled."))

	try:
		shopping_cart_invoice = frappe.get_value("Shopping Cart Invoice",{"name" : shopping_cart_invoice},"name")
		if not shopping_cart_invoice:
			return error_format(_("Shopping Cart not found. Please create another shopping cart"))
		doc_shopping_cart_invoice = frappe.get_doc("Shopping Cart Invoice", shopping_cart_invoice)
		# 

		# Check voucher by voucher_code,name dan di my voucher
		if not voucher:
			return error_format(_("Please fill the voucher code."))
		voucher_post = voucher
		voucher_found = False
		using_my_voucher = False

		voucher = frappe.get_value("Voucher", {"name": voucher_post} , "name")
		voucher_found = True if voucher else False

		if not voucher_found:	
			voucher = frappe.get_value("Voucher", {"voucher_code" : voucher_post},"name")
			voucher_found = True if voucher else False

		if not voucher_found:
			my_voucher_check = check_valid_my_voucher(voucher_post,doc_shopping_cart_invoice.customer)
			print(my_voucher_check)
			if my_voucher_check.get("status") == 1:
				using_my_voucher = True
				voucher_found = True
				my_voucher = my_voucher_check.get("keterangan")
				voucher = my_voucher_check.get("doc").get("name")
			else:
				return error_format(_(my_voucher_check.get("keterangan")))
		
		if using_my_voucher == True:
			doc_shopping_cart_invoice.voucher_code = voucher_post
			doc_shopping_cart_invoice.my_voucher = my_voucher

		doc_shopping_cart_invoice.voucher = voucher
		doc_shopping_cart_invoice.voucher_check_rule()
		doc_shopping_cart_invoice.voucher_check_item()
		doc_shopping_cart_invoice.save()
		frappe.db.commit()
		return success_format(doc_shopping_cart_invoice)
	except:
		frappe.log_error(frappe.get_traceback(),"Error: api check_voucher")
		return error_format(sys.exc_info())

	
	

	
@frappe.whitelist(allow_guest=False)
def change_status_sales_invoice(name, shipping_status,reason =""):
	try:
		if frappe.db.exists("Sales Invoice", name):
			doc = frappe.get_doc("Sales Invoice", name)
			doc.shipping_status = shipping_status
			doc.reason = reason
			doc.save(ignore_permissions=True)
			frappe.db.commit()
			return success_format(doc)
		else:
			return error_format(_("Sales Invoice not found"))
	except:
		frappe.log_error(frappe.get_traceback(),"Error: api change_status_sales_invoice")
		return error_format(_("Maaf ada kesalahan pada server"))


@frappe.whitelist(allow_guest=False)
def check_all_flash_sale():
	from commerce.commerce.doctype.flash_sale.flash_sale import check_flash_sale
	user = frappe.session.user
	checker = True
	doc_exists = frappe.db.exists("Shopping Cart", user)
	if doc_exists:
		doc = frappe.get_doc("Shopping Cart", user)
		for item in doc.shopping_cart_item:
			item_flash_sale = frappe.get_value("Item", item.item,"flash_sale")
			if item_flash_sale:
				if not check_flash_sale(item.get("item"),item_flash_sale):
					checker = False
	return success_format(checker)