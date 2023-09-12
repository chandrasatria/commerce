import frappe
import datetime
import json
from api_integration.validation import success_format, error_format

@frappe.whitelist(allow_guest=True)
def verify_email(key, email):
	fga_confirmation_email = frappe.get_all("Confirmation Email", filters=[["key_request","=",key], ["email" , "=", email]] ,fields="*")
	nowcheck = datetime.datetime.now()

    # Check validasi
	if(nowcheck > fga_confirmation_email[0]["expired_at"]):
		return error_format("Your request has expired")
	if(fga_confirmation_email[0]["used"] == 1):
		return error_format("Your request has been used, your email has been verified")

    # Update field > will trigger update confirmation email
	doc = frappe.get_doc("Confirmation Email",fga_confirmation_email[0]["name"])
	doc.used = 1
	doc.save(ignore_permissions=True)
	frappe.db.commit()

	return success_format("Email Verified")