# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe.realtime import publish_progress
from frappe import _

class FlashSale(Document):
	def on_update(self):
		self.update_all_item_flash_sale()

		# self.update_updated_margin_to_all_item()
		# if self.pricing_rule:
		# 	self.update_margin_and_valid_from_till()
		
	
	def update_all_item_flash_sale(self):
		
		fga_item = frappe.get_all("Item", fields="*", filters=[["flash_sale","=",self.name]])
		list_item_to_update = []
		idx_progress = 1
		for item in fga_item:
			percent = (idx_progress/len(fga_item)) * 100
			publish_progress(percent=percent, title=_("Updating Item"), doctype=self.doctype, docname=self.name, description=item["name"])
			idx_progress += 1
			# if item["item_price"]:
			# 	item_price_after_discount = self.self_calculate_discount_flash_sale_price(item["item_price"])
			# 	discount_amt = item["item_price"] - item_price_after_discount
			
			frappe.db.sql("""
			UPDATE `tabItem` SET flash_sale_valid_from = %(flash_sale_valid_from)s , flash_sale_valid_till = %(flash_sale_valid_till)s, flash_sale_maximal_discount = %(flash_sale_maximal_discount)s , flash_sale_discount_type = %(flash_sale_discount_type)s, flash_sale_apply_for_application = %(flash_sale_apply_for_application)s, flash_sale_apply_for_website = %(flash_sale_apply_for_website)s WHERE name = %(name)s
			""",{ "flash_sale_valid_from" : self.valid_from,
				"flash_sale_valid_till" : self.valid_till,
				"flash_sale_maximal_discount" : self.maximal_discount,
				"flash_sale_discount_type" : self.discount_type,
				"flash_sale_apply_for_application" : self.apply_for_application,
				"flash_sale_apply_for_website" : self.apply_for_website,
				"name" : item["name"]})

		publish_progress(percent=100, title=_("Updating Item"), doctype=self.doctype, docname=self.name, description="Finishing Up")
				
		# frappe.db.commit()
			# list_item_to_update.append(item["name"])
	
	
		
	def self_calculate_discount_flash_sale_price(self,price):
		disc = self.get("discount_percentage_or_amount") or 0
		disc = abs(disc)
		if self.discount_type == "Discount Percentage":
			if not disc:
				return price
			else:
				if self.maximal_discount:
					if (price * disc/100) > self.maximal_discount:
						return self.maximal_discount
					else:
						return (price * disc/100)
				else:
					return (price * disc/100)
		elif self.discount_type == "Discount Amount":
			return disc
		elif self.discount_type == "Override":
			return price - disc
		else:
			return 0

def update_empty_flash_sale(item_template):
		fga_item = frappe.get_all("Item", fields="*", or_filters=[["variant_of","=",item_template],["name","=",item_template]])
		list_item_to_update = []
		for item in fga_item:
			if not item["flash_sale"]:
				frappe.db.sql("UPDATE `tabItem` SET flash_sale = '' ,flash_sale_valid_from = null,flash_sale_valid_till = null, flash_sale_price = 0, discount_flash_sale = 0 WHERE name = '{item}'".format(item = item["name"]))
				
		frappe.db.commit()


def calculate_discount_flash_sale_price(price,flash_sale):
	
	doc_flash_sale = frappe.get_doc("Flash Sale",flash_sale)
	disc = doc_flash_sale.get("discount_percentage_or_amount") or 0
	disc = abs(disc)
	if doc_flash_sale.discount_type == "Discount Percentage":
		if not disc:
			return price
		else:
			if doc_flash_sale.maximal_discount:
				if (price * disc/100) > doc_flash_sale.maximal_discount:
					return doc_flash_sale.maximal_discount
				else:
					return (price * disc/100)
			else:
				return (price * disc/100)
	elif doc_flash_sale.discount_type == "Discount Amount":
		return disc
	elif doc_flash_sale.discount_type == "Override":
		print("asdf")
		return price - disc
	else:
		return 0


	# -------------------------------- BELOW HERE IS DEPRECIATED -------------------------
	# Cause we using calculate manual instead of pricing rule.

def update_margin_and_valid_from_till(self):
	doc_pr = frappe.get_doc("Pricing Rule", self.pricing_rule)
	doc_pr.valid_from = self.valid_from
	doc_pr.valid_upto = self.valid_till
	doc_pr.margin_rate_or_amount = self.margin
	doc_pr.save(ignore_permissions=True)
	frappe.db.commit()


def update_updated_margin_to_all_item(self):
	frappe.db.sql(""" UPDATE `tabItem` SET flash_sale_margin = %(margin)s WHERE flash_sale = %(flash_sale)s """ , 
	{"margin" : str(self.margin),
		"flash_sale": self.name})
	frappe.db.commit()


# Tidak dipake pake perhitungan sendiri
# Akan create jika ada item yang panggil fungsi ini
def create_or_update_pricing_rule(item_code,flash_sale):
	
	doc = frappe.get_doc("Flash Sale", flash_sale)
	# update semua item biar sama flash salenya
	parent_item_code = frappe.get_value("Item",item_code,"variant_of") or "nope_nope_nope"
	variant_item = frappe.get_all("Item", fields="name",or_filters=[["variant_of","LIKE",item_code],["name","LIKE",item_code],["name","LIKE",parent_item_code],["variant_of","LIKE",parent_item_code]])
	result_var = [item["name"] for item in variant_item]
	frappe.db.sql(""" UPDATE `tabItem` SET flash_sale = %(flash_sale)s WHERE name in %(result_var)s """ , 
		{
			"result_var" : result_var,
		 "flash_sale": flash_sale})
	frappe.db.commit()

	# get semua item flash sale
	all_item = frappe.db.sql(""" SELECT item_code FROM `tabItem` WHERE flash_sale = %(flash_sale)s """ , 
		{"flash_sale": flash_sale},as_dict=True)
	all_item_result = [item["item_code"] for item in all_item]

	if doc.pricing_rule:
		doc_pr = frappe.get_doc("Pricing Rule",doc.pricing_rule)
	else:
		pricing_rule_to_add = {
			"mixed_conditions": 0,
			"threshold_percentage": 0.0,
			"free_qty": 0.0,
			"items": [
			{
				"doctype": "Pricing Rule Item Code",
				"item_code": item_code,
			}
			],
			"rate_or_discount": "Discount Percentage",
			"selling": 1,
			"applicable_for": "",
			"docstatus": 0,
			"min_qty": 0.0,
			"coupon_code_based": 0,
			"apply_rule_on_other": "",
			"discount_percentage": 0.0,
			"buying": 0,
			"is_cumulative": 0,
			"title": doc.name,
			"discount_amount": 0.0,
			"min_amt": 0.0,
			"max_amt": 0.0,
			"apply_on": "Item Code",
			"rate": 0.0,
			"margin_rate_or_amount": 0.0,
			"apply_multiple_pricing_rules": 0,
			"apply_discount_on_rate": 0,
			"same_item": 0,
			"free_item_rate": 0.0,
			"max_qty": 0.0,
			"company": "Titan",
			"apply_discount_on": "Grand Total",
			"price_or_product_discount": "Price",
			"margin_type": "Percentage",
			"validate_applied_rule": 0,
			"owner": "Administrator",
			"valid_from": "2020-07-09",
			"priority": "20",
			"doctype": "Pricing Rule",
			"currency": "IDR",
			"disable": 0
		}
		doc_pr = frappe.get_doc(pricing_rule_to_add)
		doc_pr.insert()
		doc.pricing_rule = doc_pr.name
		doc.save(ignore_permissions=True)
		frappe.db.commit()

	
	doc_pr.items = []
	for item in all_item_result:
		print(item)
		doc_pr.append("items", {
			"item_code": item
		})
	doc_pr.save(ignore_permissions=True)
	frappe.db.commit()
	return True
	

def check_flash_sale(item,flash_sale):
	from commerce.helper import timediffInSeconds
	today = frappe.utils.now()
	doc_flash_sale = frappe.get_doc("Flash Sale",flash_sale)
	doc_item = frappe.get_doc("Item",item)
	checker = True
	if doc_item.get("flash_sale"):
		print(doc_item.get("flash_sale"))
		print(doc_flash_sale.name)
		if doc_item.flash_sale == doc_flash_sale.name:
			if (timediffInSeconds(doc_flash_sale.valid_from,today) > 0):
				print(timediffInSeconds(doc_flash_sale.valid_from,today))
				checker = False
			if (timediffInSeconds(doc_flash_sale.valid_till,today) < 0):
				print(timediffInSeconds(doc_flash_sale.valid_till,today))
				checker = False
			# TODO
			# if doc_flash_sale.quantity != 0:
			# 	all_buyed_item = frappe.db.sql("""SELECT scii.name FROM `tabShopping Cart Invoice Item` scii
			# 	LEFT JOIN `tabShopping Cart Invoice` sci ON scii.parent = sci.name WHERE scii.flash_sale = '{}' AND scii.docstatus = 1  """.format(flash_sale))
			# 	if len(all_buyed_item) > doc_flash_sale.quantity:
			# 		print(len(all_buyed_item))
			# 		print(doc_flash_sale.quantity)
			# 		checker = False
	else:
		checker = False
		
	return checker



# Digunakan sebelum memberikan flash sale jadi > PERHATIKAN!!!!
def check_qty_flash_sale(item, qty =0):
	checker =True
	check_item_exists = frappe.db.exists("Item", item)
	if not check_item_exists:
		checker = False
	doc_item = frappe.get_doc("Item", item)
	if doc_item.get("flash_sale"):
		doc_flash_sale = frappe.get_doc("Flash Sale", doc_item.flash_sale)
		all_buyed_item = frappe.db.sql("""SELECT SUM(scii.qty) as total_qty FROM `tabShopping Cart Invoice Item` scii 
		LEFT JOIN `tabShopping Cart Invoice` sci ON scii.parent = sci.name
		WHERE scii.flash_sale = %(flash_sale)s AND
		scii.item_code = %(item)s AND
		sci.docstatus = 1
		""",{"flash_sale" : doc_flash_sale.get("name"), "item" : doc_item.get("name")})
		print(all_buyed_item)
		print(doc_item.flash_sale_qty)
		if doc_item.flash_sale_qty > 0:
			if all_buyed_item[0][0]:
				if (all_buyed_item[0][0] + float(qty)) > doc_item.flash_sale_qty:
					print(len(all_buyed_item))
					print(doc_flash_sale.quantity)
					checker = False
	else:
		checker = False
	return checker
# Untuk check rule application/web dan 1 orang 1
def check_rule_flash_sale(flash_sale, platform):
	doc_flash_sale = frappe.get_doc("Flash Sale", flash_sale)
	if platform == "Application" and doc_flash_sale.apply_for_application == 1:
		print("ok")
	elif platform == "Website" and doc_flash_sale.apply_for_website == 1:
		print("ok")
	else:
		ket = ""
		if doc_flash_sale.apply_for_application == 1:
			ket = "Application"
		if doc_flash_sale.apply_for_website == 1:
			if ket:
				ket += " and "
			ket += "Website"
		return {"status" : 0 , "keterangan" : "Sorry, flash sale is only for transaction using {}".format(ket)}

	
	return {"status":1,"keterangan":"ok"}

# Untuk cek flash_sale_maximum_per_item and flash_sale_maximum_per_customer
def check_rule_flash_sale_maximum(flash_sale, customer, qty = 0):
	doc_flash_sale = frappe.get_doc("Flash Sale", flash_sale)
	all_buyed_item = frappe.db.sql("""SELECT SUM(scii.qty) as total_qty FROM `tabShopping Cart Invoice Item` scii 
		LEFT JOIN `tabShopping Cart Invoice` sci ON scii.parent = sci.name
		WHERE scii.flash_sale = %(flash_sale)s AND
		sci.customer = %(customer)s AND
		sci.docstatus = 1
		""",{"flash_sale" : doc_flash_sale.get("name"), "customer" : customer})
	print(all_buyed_item)
	if all_buyed_item[0][0]:
		if doc_flash_sale.flash_sale_maximum_per_item >0:
			if doc_flash_sale.flash_sale_maximum_per_item < qty + all_buyed_item[0][0]:
				# return {"status" : 0 , "keterangan" : "Sorry, maximum purchase of Flash Sale: {} transaction(s) per account".format(str(doc_flash_sale.flash_sale_maximum_per_item))}
				return {"status" : 0 , "keterangan" : "Sorry, you exceed the purchase quantity limit of this Flash Sale"}
	else:
		if doc_flash_sale.flash_sale_maximum_per_item < qty :
			return {"status" : 0 , "keterangan" : "Sorry, you exceed the purchase quantity limit of this Flash Sale"}
			# return {"status" : 0 , "keterangan" : "Sorry, maximum qty of Flash Sale Item: {} item(s) per account.".format(str(doc_flash_sale.flash_sale_maximum_per_item))}

	all_transaction = frappe.db.sql("""SELECT COUNT(sci.name) as total_transaction FROM `tabShopping Cart Invoice Item` scii 
		LEFT JOIN `tabShopping Cart Invoice` sci ON scii.parent = sci.name
		WHERE scii.flash_sale = %(flash_sale)s AND
		sci.customer = %(customer)s AND
		sci.docstatus = 1
		""",{"flash_sale" : doc_flash_sale.get("name"), "customer" : customer})
	print(all_transaction)
	if all_transaction:
		if doc_flash_sale.flash_sale_maximum_per_customer > 0:
			if doc_flash_sale.flash_sale_maximum_per_customer < all_transaction[0][0]:
				return {"status" : 0 , "keterangan" : "Sorry, you cannot participate in this Flash Sale. Because your Flash Sale transaction exceed the limit."}
				# return {"status" : 0 , "keterangan" : "Sorry, you exceed the purchase limit of Flash Sale. Maximum purchase : {} per account".format(str(doc_flash_sale.flash_sale_maximum_per_customer))}
	
	return {"status" : 1 , "keterangan" : "ok"}


