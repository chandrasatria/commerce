# -*- coding: utf-8 -*-
# Copyright (c) 2021, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RequestSalesPersonChange(Document):
	def before_save(self):
		self.add_customer_user_from_session()


# ------ Custom Function
	def add_customer_user_from_session(self):
		if not self.customer and not self.user:
			self.user = frappe.session.user
		if not self.customer and self.user:
			self.customer = get_customer(self.user)
		if self.customer and not self.user:
			self.user = get_user(self.customer)


def get_user(user):
	user_name = frappe.get_value("Customer",user,"email_id")
	return user_name

def get_customer(user):
	customer_name = frappe.get_value("Customer",{"email_id" : user},"name")
	return customer_name