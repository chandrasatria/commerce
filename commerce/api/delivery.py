import frappe
from delivery_integration.api.delivery import get_delivery
from api_integration.validation import success_format, error_format
from frappe import _

@frappe.whitelist(allow_guest= False)
def list_all_delivery():
	try:
		req = frappe.request.data.decode("UTF-8")
		import json
		req = json.loads(req)
		address = req.get("address", None)
		shopping_cart_invoice = req.get("shopping_cart_invoice", None)
		if not address:
			return error_format(_("Address need to be filled."))
		if not shopping_cart_invoice:
			return error_format(_("Shopping Cart Invoice need to be filled."))

		if not frappe.db.exists("Address",address):
			return error_format(_("Maaf terjadi kesalahan."))
		if not frappe.db.exists("Shopping Cart Invoice",shopping_cart_invoice):
			return error_format(_("Maaf terjadi kesalahan."))
		store_settings = frappe.get_single("Store Settings")
		if not store_settings.get("from_territory"):
			return error_format(_("Maaf terjadi kesalahan. Silahkan hubungi admin."))

		doc_address = frappe.get_doc("Address",address)
		item_to_check = []
		
		doc_shopping_cart_item = frappe.get_doc("Shopping Cart Invoice",shopping_cart_invoice)

		to_territory = ""
		if doc_address:
			to_territory = doc_address.get("subdistrict_delivery")
			if not to_territory:
				to_territory = doc_address.get("district_delivery")
				if not to_territory:
					to_territory = doc_address.get("city_delivery")
		
		if not to_territory:
			return error_format(_("Maaf alamat pengiriman tidak ditemukan, silahkan ganti alamat anda."))

		for item in doc_shopping_cart_item.get("items"):
			map_item = concate_item(item)
			item_to_check.append(map_item)
			
		get_delivery_args = {
			"to_territory" : to_territory,
			"supplier_item" : [{
				"supplier"			: store_settings.get("company"),
				"from_territory"	: store_settings.get("from_territory"),
				"item"				: item_to_check
			}]
		}

		import requests
		import json
		url = store_settings.get("base_url")+'api/method/delivery_integration.api.delivery.get_delivery'
		data_response = requests.post(url, json = get_delivery_args)
		if data_response.status_code == 200:
			dict_resp = json.loads(data_response.text)
			if dict_resp.get("message").get("data"):
				if len(dict_resp.get("message").get("data")) > 0:
					if dict_resp["message"]["data"][0].get("available_delivery"):
						return success_format(dict_resp["message"]["data"][0]["available_delivery"])
				else:
					return error_format(_("Maaf pengiriman ke tempat anda tidak didukung, silahkan ganti alamat atau hubungi kami."))
			return error_format(_("Maaf pengiriman ke tempat anda tidak didukung, silahkan ganti alamat atau hubungi kami."))
		return error_format(_("Maaf pengiriman ke tempat anda tidak didukung, silahkan ganti alamat atau hubungi kami."))
	except:
		frappe.log_error(frappe.get_traceback(),"Error: list_all_delivery")
		return error_format(_("Maaf ada kesalahan pada server"))


def concate_item(item):
	item_weight = 0
	if item.get("weight_uom") == "Gram":
		item_weight = int(item.get("weight_per_unit"))*int(item.get("qty"))*int(item.get("conversion_uom"))/1000
	elif item.get("weight_uom") == "Kilogram":
		item_weight = int(item.get("weight_per_unit"))*int(item.get("qty"))*int(item.get("conversion_uom"))
	else:
		item_weight = int(item.get("weight_per_unit"))*int(item.get("qty"))*int(item.get("conversion_uom"))
	map_item = {
		"item_name"		: item.get("item_name","-"),
		"item_weight"	: item_weight,
		"length"		: 0,
		"width"			: 0,
		"height"		: 0,
		"qty"           : item.get("qty")
	}
	return map_item
