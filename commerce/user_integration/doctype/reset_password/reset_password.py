# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
# from commerce.user_integration.controllers import ResetPasswordController


class ResetPassword(Document):
	def before_save(self):
		pass

