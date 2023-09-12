# -*- coding: utf-8 -*-
# Copyright (c) 2021, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import os
from frappe import _

from commerce.user_integration.doctype.user_integration_settings.reset_password_generate_v1 import load_notification, load_html


class UserIntegrationSettings(Document):
	# Untuk reset Password
	def generate_notification(self):
		fga_notification = frappe.get_all("Notification",filters=[["name","=","Reset Password"]])
		if len(fga_notification) > 0:
			doc = frappe.get_doc("Notification", fga_notification[0]["name"])
			doc.message = load_notification(self)
			doc.save(ignore_permissions=True)
		else:
			fga_user = frappe.get_all("Email Account", filters=[["default_outgoing" ,"=",1]],fields="name")
			if len(fga_user) <= 0 :
				frappe.throw(_("Please set up email account first."))
			doc = frappe.get_doc({ "__newname" : "Reset Password",
				"enabled": 1,
				"channel": "Email",
				"subject": "Reset Password",
				"document_type": "Reset Password",
				"is_standard": 0,
				"event": "New",
				"days_in_advance": 0,
				"sender": fga_user[0]["name"],
				"condition": "",
				"message": load_notification(self),
				"attach_print": 0,
				"doctype": "Notification",
				"recipients": [{
				"email_by_document_field": "user",
				"doctype": "Notification Recipient"
				}]
			})
			doc.save(ignore_permissions=True)
		frappe.msgprint(_("Successfully create/update notifications"))
	
def soft_parse(some_value):
	some_value = some_value.replace(" ", "%20")
	return some_value
		

