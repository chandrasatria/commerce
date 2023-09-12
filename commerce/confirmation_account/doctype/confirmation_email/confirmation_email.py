# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class ConfirmationEmail(Document):
	def before_insert(self):
		if not self.full_name and self.email: 
			self.full_name = find_full_name(self.email)
		self.key_request = create_random_code()
		self.expired_at = calculate_expired_time()

	def on_update(self):
		if self.used:
			self.update_data_on_other_doctype()

# ----------- end of hooks -----------------

	def update_data_on_other_doctype(self):
		try:
			confirmation_account_settings = frappe.get_single("Confirmation Account Settings")
			doctype_to_update = confirmation_account_settings.confirmation_doctype_update
			confirmation_field_lookup = confirmation_account_settings.confirmation_field_lookup
			field_to_update = confirmation_account_settings.confirmation_field_update

			sql_check = frappe.db.sql("SELECT name FROM `tab{doctype_to_update}` WHERE {confirmation_field_lookup} = '{self_email}' ".format(
				doctype_to_update = doctype_to_update,
				confirmation_field_lookup = confirmation_field_lookup,
				self_email = self.email
			))
			if len(sql_check) > 0 and len(sql_check) < 2:
				frappe.db.sql("UPDATE `tab{doctype_to_update}` SET {field_to_update} = '1' WHERE {confirmation_field_lookup} = '{self_email}' ".format(
					doctype_to_update = doctype_to_update,
					field_to_update = field_to_update,
					confirmation_field_lookup = confirmation_field_lookup,
					self_email = self.email
				))
				frappe.db.commit()
				print("Success.")
			else:
				print("Entry appear multiple times.")
		except:
			frappe.throw(_("Invalid field/document to change. Please contact admin."))
			


# ----------- function -------------

def find_full_name(email_id):
	full_name = ""
	if not email_id:
		return full_name
	try:
		fga_customer = frappe.get_all("Customer",filters=[["email_id", "=",email_id]],fields="name,customer_name")
		if len(fga_customer) > 0:
			full_name = fga_customer[0]["customer_name"]
	except:
		pass

	try:
		fga_user = frappe.get_all("User",filters=[["email", "=",email_id]],fields="name,full_name")
		if len(fga_user) > 0:
			full_name = fga_user[0]["full_name"]
	except:
		pass

	return full_name


def create_random_code():
	from commerce.confirmation_account.helper import randomString
	isNotInserted=True
	while isNotInserted:
		random_string = randomString(12)
		check_ce = frappe.get_all("Confirmation Email", filters={"key_request":random_string} ,fields="*")
		if len(check_ce) == 0:
			isNotInserted = False
	return random_string
	
def calculate_expired_time():
	import datetime
	from commerce.confirmation_account.helper import strToDatetime, timeStrToTimeDelta

	confirmation_account_settings = frappe.get_single("Confirmation Account Settings")
	if confirmation_account_settings:
		deltaTime = timeStrToTimeDelta(confirmation_account_settings.get("confirmation_email_expire"))
		expired = (strToDatetime(frappe.utils.now()) + deltaTime)
	else:
		expired = (datetime.datetime.now() + datetime.timedelta(hours=2))
	return expired

