# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

def error(log_message, log_title, err_message=None, err_title=None, raise_exception=False):
	if err_message is None:
		err_message = "Dont worry, please contact a developer to fix this issue. Thank you"
	if err_title is None:
		err_title = "Something went wrong"

	frappe.log_error(_(str(log_message)), _(str(log_title)))
	frappe.msgprint(msg=_(str(err_message)), title=_(str(err_title)), raise_exception=raise_exception, as_table=False, indicator="red", alert=False, primary_action=None, is_minimizable=None)