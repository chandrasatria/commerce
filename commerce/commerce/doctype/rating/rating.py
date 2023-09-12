# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class Rating(Document):
	def before_save(self):
		self.validate_field()
		self.add_missing_customer()
	
	def on_update(self):
		if self.item:
			self.recalculate_all_rating()
		self.check_rate_sales_invoice()


	def recalculate_all_rating(self):
		all_rating_sql = frappe.db.sql("SELECT SUM(rating) as sr, COUNT(name) as cn FROM `tabRating` WHERE item = '{}'".format(self.item),as_dict = True)
		if len(all_rating_sql) >0 :
			sr = all_rating_sql[0]["sr"]
			cn = all_rating_sql[0]["cn"]
			average = sr/cn
			frappe.db.sql("UPDATE `tabItem` SET total_rating = {}, rating = {} WHERE name = '{item}' ".format(cn,average,item = self.item))
			frappe.db.commit()

	def check_rate_sales_invoice(self):
		if self.sales_invoice:
			all_item_code = frappe.db.sql("SELECT item_code FROM `tabSales Invoice Item` WHERE parent = '{}' ".format(self.sales_invoice),as_dict = True)
			all_rated_item_code = frappe.db.sql("SELECT item FROM `tabRating` WHERE sales_invoice = '{}' ".format(self.sales_invoice),as_dict = True)
			if len(all_item_code) <= len(all_rated_item_code):
				frappe.db.sql("UPDATE `tabSales Invoice` SET rated = 1 WHERE name = '{sales_invoice}' ".format(sales_invoice = self.sales_invoice))
				frappe.db.commit()



	def validate_field(self):
		if self.rating:
			if self.rating < 1 or self.rating > 6:
				frappe.throw(_("Rating only from 1 until 5."))

	def add_missing_customer(self):
		if self.get("sales_invoice") and not self.get("customer"):
			customer = frappe.get_value("Sales Invoice",self.sales_invoice,"customer")
			if customer:
				self.customer = customer