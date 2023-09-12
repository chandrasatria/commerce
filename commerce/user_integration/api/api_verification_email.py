import frappe
import json
import base64
import sys

from frappe import _

from api_integration.validation import success_format, error_format
from commerce.user_integration.controllers.verification_controller import create_verification_email

@frappe.whitelist(allow_guest=True)
def request_verification_email():
	""" ini dipanggil untuk minta verifikasi email"""
	try:
		# Pake frappe.req.data karena api web tidak bisa baca argument
		req = json.loads(frappe.request.data.decode("UTF-8"))
		if not req:
			frappe.log_error(frappe.get_traceback(),"Error: API Request Verification Email need args")
			return error_format(_("Something went wrong. Please try again in a few minutes"))
		email = req["email"] or ""

		if not email:
			return error_format(_("Please input a valid email."))

		fga_verification_email = frappe.get_all("Verification Email", fields = "name" , filters=[["is_used","=",1],["user","=",email]])
		fga_user = frappe.get_all("User",fields= "email, name",or_filters=[["name","=",email],["email","=",email]])
		if len(fga_user) <= 0:
			return error_format(_("Email not found, please check again your email."))
		if len(fga_verification_email) <= 0:
			create_verification_email(fga_user[0]["name"])
			return success_format(_("Thank you, request email verification success.\n Please check your email for confirmation."))
		else:
			return error_format(_("Your Email has been verified."))
		
	except:
		frappe.log_error(frappe.get_traceback(), "Error: Verification Email")
		return error_format(exceptions=_("Something went wrong. Please try again in a few minutes"))


@frappe.whitelist(allow_guest=True)
def validate_verification_email():
	"""ini dipanggil di website"""
	try:
		# Pake frappe.req.data karena api web tidak bisa baca argument
		req = json.loads(frappe.request.data.decode("UTF-8"))
		if not req:
			frappe.log_error(frappe.get_traceback(),"Error: API Verification Email need args")
			return error_format(_("Something went wrong. Please try again in a few minutes"))
		email = req["email"] or ""
		token = req["token"] or ""
		 
		if not token:
			frappe.log_error(frappe.get_traceback(),"Error: Verification Email need token")
			return error_format(_("Something went wrong. Please try again in a few minutes"))
		if not email:
			frappe.log_error(frappe.get_traceback(),"Error: Verification Email need email")
			return error_format(_("Something went wrong. Please try again in a few minutes"))


		fga_verification_email = frappe.get_all("Verification Email", fields = "name,is_used" , filters=[["token" , "=", token],["user","=",email]])
		if len(fga_verification_email) <= 0:
			frappe.log_error(frappe.get_traceback(),"Error: Verification Email not found")
			return error_format(_("Cannot find your request. Please contact administrator"))
		# Jika email belum digunakan -> save
		if fga_verification_email[0]["is_used"] == 0:
			doc = frappe.get_doc("Verification Email", fga_verification_email[0]["name"])
			doc.is_used = 1
			doc.save(ignore_permissions=True)
			frappe.db.commit()
			return success_format("Email has been successfully verified")

		return error_format("Your Email has been verified.")
		
	except:
		frappe.log_error(frappe.get_traceback(), "Error: Verification Email")
		return error_format(exceptions=_("Something went wrong. Please try again in a few minutes"))