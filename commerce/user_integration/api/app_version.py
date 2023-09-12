import frappe
import sys
from commerce.user_integration.validation import success_format, error_format

@frappe.whitelist(allow_guest=True) 
def app_version():
	try:
		doc = frappe.get_doc("App Version","App Version")
		return success_format(doc)

	except:
		return error_format(sys.exc_info())