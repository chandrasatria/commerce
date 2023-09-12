import frappe
import json
import base64
import sys

from frappe import _

from commerce.user_integration.validation import success_format, error_format


# Define the field and parameter
from commerce.user_integration.setting import doctype_user,user_field,password_field,field_user_customer_profile_picture

def get_user_by_session(session_user = ""):
	if not session_user:
		session_user = frappe.session.user
	if frappe.db.exists("User", session_user):
		return True
	else:
		return False

def get_user_custom_by_session(session_user = ""):
	if not session_user:
		session_user = frappe.session.user
	val = frappe.get_value(doctype_user,{user_field : session_user}, "name")
	if val:
		return val
# ini harus disesuaikan field dan filter mana yang ngga langsung insert
def filter_convert_to_dict(param):
	# custom here
	just_param = ["customer_name", "bio", "mobile_number"]
	some_dict = {}
	for item in just_param:
		some_dict[item] = param.get(item,"")
	return some_dict


@frappe.whitelist(allow_guest=False)
def edit_profile(**all_param):
	from frappe.utils.password import get_decrypted_password
	session_user = frappe.session.user
	# session_user = "antok@mailinator.com"

	if not session_user or session_user == "Guest":
		return error_format(_("Please login first."))

	user_custom = get_user_custom_by_session(session_user)
	if not user_custom:
		return error_format(_("User not found."))

	# Check here too
	new_email = all_param.get("email","")
	if new_email:
		if new_email != session_user:
			return error_format(_("Email cannot be changed for security reasons."))

	try:
		doc = frappe.get_doc("Customer",user_custom)
		p = filter_convert_to_dict(all_param)
		doc.update(p)
		doc.save(ignore_permissions=True)
		frappe.db.commit()
	except:
		return error_format(sys.exc_info())
	return success_format(_("Profile has been successfully changed."))


	# frappe.db.commit()
@frappe.whitelist(allow_guest=True)
def check_param(**all_param):
	return all_param


@frappe.whitelist(allow_guest=False)
def upload_profile_picture():
	"""ini akan jadi private"""
	try:
		from commerce.user_integration.helper import upload_base64_set_profile_picture
		import hashlib
		import time
		session_user = frappe.session.user
		user_custom = get_user_custom_by_session(session_user)

		post = json.loads(frappe.request.data.decode('utf-8'))
		image_name = "img_"+str(user_custom)+"_"+str(frappe.utils.now())[-5:]+".png"
		
		result = upload_base64_set_profile_picture(image_name,post["file_data"],doctype_user,user_custom,field_user_customer_profile_picture, is_private=1)
		# Change User Profile Picture
		
		if result != "Something went wrong":
			frappe.db.sql("UPDATE `tabUser` SET user_image = '{}' WHERE name = '{}' ".format(result.get("file_url"),frappe.session.user))
		# result = upload_base64_set_profile_picture(image_name,post["file_data"],doctype_user,user_custom,field_user_customer_profile_picture, is_private=1)
		return success_format(result)
	except:
		frappe.log_error(frappe.get_traceback(), "Error: Upload Profile Picture")
		return error_format(exceptions=_("Something went wrong. Please try again in a few minutes"))


@frappe.whitelist(allow_guest=False)
def upload_profile_picture_cb():
	session_user = frappe.session.user
	data = json.loads(frappe.request.data.decode('utf-8'))
	return data['filedata']
		