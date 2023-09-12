import frappe
import json
import base64
import sys
import datetime

from frappe import _

from commerce.user_integration.validation import success_format, error_format


# Define the field and parameter
from commerce.user_integration.setting import doctype_user,user_field,password_field,field_user_customer,change_password_store

@frappe.whitelist(allow_guest=True)
def is_login():
	return frappe.session.user

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

# Ini untuk reset password biasa
@frappe.whitelist(allow_guest=False)
def change_password_by_old_password(old_password, new_password, confirm_password = ""):
	from frappe.utils.password import get_decrypted_password
	session_user = frappe.session.user
	# session_user = "antok@mailinator.com"

	if not session_user or session_user == "Guest":
		return error_format(_("Please login first."))

	user_custom = get_user_custom_by_session(session_user)
	if not user_custom:
		return error_format(_("User not found."))

	if confirm_password:
		if new_password != confirm_password:
			return error_format(_("New Password didn't match."))
	

	password_user_custom = get_decrypted_password(doctype_user, user_custom, fieldname=password_field, raise_exception=False)
	if password_user_custom != old_password:
		return error_format(_("Old Password didn't match."))
	
	doc = frappe.get_doc("User", session_user)
	doc.new_password = new_password
	doc.save(ignore_permissions=True)
	frappe.db.commit()

	doc_user_custom = frappe.get_doc(doctype_user, user_custom)
	doc_user_custom.update({password_field : new_password})
	doc_user_custom.save(ignore_permissions=True)
	frappe.db.commit()
	return success_format(_("password has been successfully changed."))
	


@frappe.whitelist(allow_guest=True)
def post_ping_guest():
	post = json.loads(frappe.request.data.decode('utf-8'))
	return post

# Reset Password | Doctype Reset Password
# using deeplink and email


import frappe
import json
import base64
import sys

import datetime


from commerce.user_integration.helper import strToDatetime, randomString,randomString

# Maaf tidak sempat ubah ke controller #antz
@frappe.whitelist(allow_guest=True)
def request_reset_password():

	# NOTE >>> Ini custom untuk WSS saja, hapus sampai sini
	post = json.loads(frappe.request.data.decode('utf-8'))
	customer_list = frappe.get_all(doctype_user,filters=[[user_field,"=",post[user_field]]], fields="{},name,register_via".format(user_field))
	
	if len(customer_list) == 0:
		return success_format(_("Mohon periksa email untuk pembaruan kata sandi."))

	
	if customer_list[0]["register_via"] != "Frappe":
		return error_format(_("Please login via {}.".format(customer_list[0]["register_via"])))
	
	# end here

	# NOTE >>> lalu uncomment disini
	# NOTE Jangan lupa add Notification
	# post = json.loads(frappe.request.data.decode('utf-8'))
	# customer_list = frappe.get_all(doctype_user,filters=[[user_field,"=",post[user_field]]], fields="{},name".format(user_field))
	
	# if len(customer_list) == 0:
	# 	return error_format("Customer Email tidak ditemukan")

	isNotInserted=True
	while isNotInserted:
		random_string = randomString(12)
		checkrpr = frappe.get_all("Reset Password", filters={"key_request":random_string} ,fields="*")
		if len(checkrpr) == 0:
			isNotInserted = False
	expired = (strToDatetime(frappe.utils.now()) + datetime.timedelta(hours=2))
	# expired = (datetime.datetime.now() + datetime.timedelta(hours=2))
	doc = frappe.get_doc({
		'doctype': 'Reset Password',
		field_user_customer : customer_list[0]["name"],
		'user': customer_list[0][user_field],
		'key_request': random_string,
		'expired_on': expired,
		'is_used' : 0
	})
	doc.insert(ignore_permissions=True)
	frappe.db.commit()
	doc.key_request = ""
	return success_format(_("Mohon periksa email untuk pembaruan kata sandi."))

@frappe.whitelist(allow_guest=True)
def reset_password():
	# post["user"]
	# post["key"]
	# post["password"]
	post = json.loads(frappe.request.data.decode('utf-8'))
	reset_password_list = frappe.get_all("Reset Password", filters=[["user","=",post["user"]],["key_request","=",post["key"]]] ,fields="*")
	nowcheck = datetime.datetime.now()
	if(len(reset_password_list)==0):
		return error_format(_("Your request is not valid. Please check again the email."))
	if(nowcheck > reset_password_list[0]["expired_on"]):
		return error_format("Your request has expired")
	if(reset_password_list[0]["is_used"] == 1):
		return error_format("Your request has been used")

	doc = frappe.get_doc("Reset Password",reset_password_list[0]["name"])
	doc.is_used = 1
	doc.save(ignore_permissions=True)
	frappe.db.commit()
	#change password to user
	docuser = frappe.get_doc("User",reset_password_list[0]["user"])
	docuser.new_password=post["password"]
	docuser.save(ignore_permissions=True)
	frappe.db.commit()

	if change_password_store == 1:
		fga = frappe.get_all(doctype_user,fields="name",filters=[[user_field,"=",post["user"]]])
		doc_customer = frappe.get_doc(doctype_user, fga[0]["name"])
		doc_customer.password = post["password"]
		doc_customer.save(ignore_permissions=True)
		frappe.db.commit()		

	return success_format("Password changed")
				
@frappe.whitelist(allow_guest=False)
def change_password():
	if frappe.request.data is None:
		return "Forbidden"
	user_id = get_user_id_by_session()
	data_user = []
	data_user = frappe.db.sql("SELECT user FROM `tabCustomer User` WHERE name='{}'".format(user_id),as_dict=True)
	if (len(data_user) > 0):
		data = json.loads(frappe.request.data)
		try:
			check_password(data_user[0]['user'],data['old_pwd'])
		except frappe.AuthenticationError:
			return error_format("Old Password wrong")
		new_user = {
			"new_password":data['new_pwd']
		}

		doc = frappe.get_doc("User",data_user[0]['user'])
		doc.flags.ignore_permissions = True
		doc.update(new_user)
		doc.save()
		frappe.db.commit()

		return success_format(doc)
	return error_format("User not found")



@frappe.whitelist(allow_guest=True)
def get_style_reset_password():
	doc = frappe.get_single("Application Info")
	return success_format(doc)


@frappe.whitelist(allow_guest=False)
def download_html():
	from commerce.user_integration.doctype.user_integration_settings.reset_password_generate_v1 import load_html
	user_integration_settings = frappe.get_single("User Integration Settings")
	html_data = load_html(user_integration_settings)
	import os
	frappe.local.response.filename = os.path.basename("reset_password.html")
	frappe.local.response.filecontent = html_data
	frappe.local.response.type = "download"




