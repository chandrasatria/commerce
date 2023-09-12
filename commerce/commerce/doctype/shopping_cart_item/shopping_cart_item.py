# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ShoppingCartItem(Document):
	def validate(self):
		pass
		# self.change_to_min_order_quantity()
		# self.get_uom_conversion_factor()

	def change_to_min_order_quantity(self):
		if self.get("item") and self.get("qty"):
			if frappe.db.exists("Item",self.get("item")):
				if not self.get("uom"):
					uom_item = frappe.get_value("Item",self.get("item"),"uom")
					# self.uom = uom_item
					fga_uom_conversion_detail = frappe.get_all("UOM Conversion Detail",fields="minimal_qty, name",filters=[["parent","=",self.get("item")],["uom","=",self.get("uom")]])
					if len(fga_uom_conversion_detail) > 0:
						min_order_quantity_item = fga_uom_conversion_detail[0]["minimal_qty"]

				min_order_quantity_item = frappe.get_value("Item",self.get("item"),"min_order_qty")
				
				if min_order_quantity_item > self.get("qty"):
					print(min_order_quantity_item)
					if self.get("parent"):
						fga_sci = frappe.get_all("Shopping Cart Item", fields="name",filters=[["parent","=",self.get("parent")],["item","=",self.get("item")]])
						if len(fga_sci) == 0:
							self.qty = min_order_quantity_item
				

	def get_uom_conversion_factor(self):
		if self.uom and not self.conversion_uom:
			fga = frappe.get_all("UOM Conversion Detail",fields="conversion_factor",filters=[["uom","=",self.uom],["parent","=",self.item]])
			if len(fga) > 0:
				self.conversion_uom = fga[0]["conversion_factor"]
			else:
				self.conversion_uom = 1


