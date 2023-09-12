import frappe
import json
import string
import sys
from api_integration.validation import success_format, error_format
from frappe import _

@frappe.whitelist(allow_guest=False)
def get_all_payment_method_commerce(total, can_cod = 0):
	from xendit.payment_methods import get_all_payment_method
	final_response = ""
	response = get_all_payment_method(total)
	# print(response)
	can_delete_cod_category = 0
	if response.get("data"):
		if can_cod == 0:
			for item in response.get("data"):
				if item == "COD":
					can_delete_cod_category = 1
			if can_delete_cod_category==1:
				response["data"].pop("COD")
				response["data"]["availability"] = [item for item in response["data"]["availability"] if item["item"] != "COD"]
			final_response = response["data"]
		else:
			final_response = response["data"]
		return success_format(final_response)
	else:
		return response