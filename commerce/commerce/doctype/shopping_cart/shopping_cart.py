# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from commerce.helper import randomString
import math
class ShoppingCart(Document):
	def before_save(self):
		self.add_sales_person()
		self.check_and_add_same_item()
	
	def on_update(self):
		self.update_sales_person_to_customer()

# -- Function

	def get_uom_conversion_factor(self):
		if self.uom and not self.conversion_uom:
			fga = frappe.get_all("UOM Conversion Detail",fields="conversion_factor",filters=[["uom","=",self.uom],["parent","=",self.item]])
			if len(fga) > 0:
				self.conversion_uom = fga[0]["conversion_factor"]
			else:
				self.conversion_uom = 1

	def check_and_add_same_item(self):
		# Ini function ketika add tapi sama maka tambah qty.
		
		map_list_item = {}
		list_item_uom = []
		to_get_min_mult_qty = []
		# Ini ketika item ada di item list DAN uom nya sama dengan indexUom item sebelumnya 
		for index,item in enumerate(self.shopping_cart_item):
			temp_item_uom = generate_unique(item.get("item"), item.get("uom"))
			if not item.get("unique_id"):
				item.unique_id = randomString(20)
			
			if temp_item_uom not in list_item_uom:
				
				list_item_uom.append(temp_item_uom)
				to_get_min_mult_qty.append(item.get("item"))
				map_list_item[temp_item_uom] = {
					"item" : item.get("item"),
					"qty" : item.get("qty"),
					"uom" : item.get("uom"),
					"weight_per_unit" : item.get("weight_per_unit"),
					"unique_id" : item.get("unique_id"),
					"is_selected" : item.get("is_selected"),
					"conversion_uom" : item.get("conversion_uom"),
					}
			else:
				map_list_item[temp_item_uom]["qty"] = map_list_item[temp_item_uom]["qty"] + item.get("qty")
			
			# 	list_map_item_qty[item.get("item")]
			# 	list_unique_id.append(item.get("unique_id"))
			# 	list_is_checked.append(item.get("is_selected"))
			# 	list_item_uom.append(item.get)
			# 	list_item_uom.append(item.get("item")+"___"+item.get("uom"))
			
			# else:
			# 	l_index = list_item.index(item.get("item"))
			# 	list_qty_item[l_index] = list_qty_item[l_index] + item.get("qty")
		
		fga_uom_conv_detail = frappe.get_all("UOM Conversion Detail",fields="*",filters=[["parent","IN",to_get_min_mult_qty],["parenttype","=","Item"]])
		mapped_item_uom = uom_conv_detail_list_to_map(fga_uom_conv_detail)
		for item in list_item_uom:
			temp_item_uom = generate_unique(map_list_item[item].get("item"), map_list_item[item].get("uom"))
			# Untuk qty
			if map_list_item[item]["qty"] < mapped_item_uom[temp_item_uom]["minimal_qty"]:
				map_list_item[item]["qty"] = mapped_item_uom[temp_item_uom]["minimal_qty"]

			if mapped_item_uom[temp_item_uom]["multiplication_qty"]:
				temp_factor = (map_list_item[item]["qty"] - mapped_item_uom[temp_item_uom]["minimal_qty"]) / mapped_item_uom[temp_item_uom]["multiplication_qty"];
				rounded = mapped_item_uom[temp_item_uom]["minimal_qty"] + math.ceil(temp_factor)  * mapped_item_uom[temp_item_uom]["multiplication_qty"]
				map_list_item[item]["qty"] = rounded
			# if map_list_item[item]["qty"] > mapped_item_uom[temp_item_uom]["minimal_qty"]:
			# 	min_order_qty + (x.ceil() * multiplication_qty);
			
			if map_list_item[item]["conversion_uom"] != mapped_item_uom[temp_item_uom]["conversion_factor"]:
				map_list_item[item]["conversion_uom"] = mapped_item_uom[temp_item_uom]["conversion_factor"]
		

		self.shopping_cart_item = []
		for idx,item in enumerate(list_item_uom):
			self.append("shopping_cart_item",{
				"idx" : idx+1,
				"unique_id" : map_list_item[item]["unique_id"],
				"qty": map_list_item[item]["qty"],
				"doctype": "Shopping Cart Item",
				"item": map_list_item[item]["item"],
				"weight_per_unit": map_list_item[item]["weight_per_unit"],
				"conversion_uom" : map_list_item[item]["conversion_uom"],
				"parenttype": "Shopping Cart",
				"is_selected": map_list_item[item]["is_selected"],
				"parentfield": "shopping_cart_item",
				"uom" : map_list_item[item]["uom"],
				"parent": self.name
			})


	def add_sales_person(self):
		if not self.sales_person and self.customer:
			doc_customer = frappe.get_doc("Customer",self.customer)
			if doc_customer.get("sales_team"):
				fetch_sales_person = doc_customer.sales_team[0].get("sales_person")
				if fetch_sales_person:
					self.sales_person = fetch_sales_person


	
	# On update

	def update_sales_person_to_customer(self):
		if self.get("sales_person"):
			frappe.db.sql("UPDATE `tabCustomer` SET selected_sales_person = %(sales_person)s WHERE name = %(customer)s",
			{	
				"sales_person" : self.get("sales_person"),
				"customer" : self.get("customer")
			})
			frappe.db.commit()


def generate_unique(id_satu, id_dua):
	return id_satu+"___"+id_dua


def uom_conv_detail_list_to_map(some_list):
	response = {}
	for item in some_list:
		key = generate_unique(item["parent"],item["uom"])
		response[key] = item
	return response


