# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class VoucherGiveaway(Document):
	def on_update(self):
		from commerce.voucher.doctype.voucher.voucher import claim_voucher

		if self.docstatus == 1:
			if not self.voucher:
				frappe.throw(_("Please fill the voucher first."))
			for item in self.voucher_giveaway_customer:
				claim_voucher(voucher = self.voucher, customer = item.customer )
