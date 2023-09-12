# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class VerificationController():

	def check_multi_store(self, store, supplier):
		pass

# End of controller

def create_verification_email(user):
	if user:
		doc = frappe.get_doc({
			"user": user,
			"is_used": 0,
			"doctype": "Verification Email"
		})
		doc.save(ignore_permissions = True)
		frappe.db.commit()
		return doc
	return ""
		