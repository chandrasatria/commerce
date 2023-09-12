# -*- coding: utf-8 -*-
# Copyright (c) 2019, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

global_company = "Titan"

def validate(doc, method):
	doc.publish_start_date = doc.start_date
	doc.publish_end_date = doc.end_date
	if doc.pricing_rule:
		update_pricing_rule(doc)
	elif not doc.pricing_rule:
		create_pricing_rule(doc)
		


# ----------- END OF HOOKS -------------

def update_pricing_rule(doc):
	pr_doc = frappe.get_doc("Pricing Rule", doc.pricing_rule)
	pr_doc.min_amt = doc.min_amt
	pr_doc.max_amt = doc.max_amt
	pr_doc.start_date = doc.start_date
	pr_doc.end_date = doc.end_date
	pr_doc.rate_or_discount = doc.discount_type
	if doc.discount_type == "Discount Percentage":
		pr_doc.discount_percentage = doc.discount
		pr_doc.maximal_discount = doc.maximal_discount
	if doc.discount_type == "Discount Amount":
		pr_doc.discount_amount = doc.discount
	pr_doc.save(ignore_permissions=True)
	frappe.db.commit()



def create_pricing_rule(doc):
	pr_doc = frappe.get_doc({
		"apply_discount_on_rate": 0,
		"docstatus": 0,
		"priority": "20",
		"for_price_list": "Standard Selling",
		"mixed_conditions": 0,
		"apply_multiple_pricing_rules": 1,
		"rate_or_discount": doc.discount_type,
		"discount_percentage": doc.discount if doc.discount_type == "Discount Percentage" else 0.0,
		"title": doc.name,
		"margin_rate_or_amount": 0.0,
		"discount_amount": doc.discount if doc.discount_type == "Discount Amount" else 0.0,
		"apply_discount_on": "Grand Total",
		"company": global_company,
		"doctype": "Pricing Rule",
		"apply_on": "Item Group",
		"item_groups": [
		{
			"doctype": "Pricing Rule Item Group",
			"item_group": "All Item Groups",
		}
		],
		"max_amt": doc.max_amt,
		"min_qty": 0.0,
		"coupon_code_based": 0,
		"price_or_product_discount": "Price",
		"currency": "IDR",
		"buying": 0,
		"threshold_percentage": 0.0,
		"selling": 1,
		"applicable_for": "",
		"max_qty": 0.0,
		"validate_applied_rule": 0,
		"valid_from": doc.start_date,
		"valid_upto": doc.end_date,
		"disable": 0,
		"min_amt": doc.min_amt,
		"maximal_discount": doc.maximal_discount
	})
	pr_doc.insert(ignore_permissions=True)
	frappe.db.commit()
	doc.pricing_rule = pr_doc.name