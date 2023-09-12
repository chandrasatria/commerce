import frappe
import sys
from frappe.auth import get_logged_user
from commerce.commerce.api.validation import success_format, error_format
from frappe.core.doctype.user.user import generate_keys
from frappe.utils import get_request_session


@frappe.whitelist()
def get_global_token():
	try:
		global_token = frappe.get_doc("Global Token Setting","Global Token Setting")
		return success_format(global_token)
	except:
		return error_format(sys.exc_info())

@frappe.whitelist()
def get_basic_token(usr):
	try: 
		if usr:
			user = frappe.get_doc("User",usr)
			secret_key = generate_keys(usr)
			token = str("{}:{}".format(user.api_key, secret_key['api_secret']))
			return success_format({'token': token })
		else:
			return error_format(frappe._("User not found"))
	except:
		return error_format(sys.exc_info())

@frappe.whitelist()
def test_translation():
	return frappe._("User not found")



