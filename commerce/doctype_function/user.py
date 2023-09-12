# -*- coding: utf-8 -*-
# Copyright (c) 2019, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document



def on_update(doc, method):
	if doc.name:
		fga_customer = frappe.get_all("Customer", fields="name",filters=[["email_id","=",doc.name]])
		if len(fga_customer) > 0 :
			customer_doc = frappe.get_doc("Customer",fga_customer[0]["name"])
			contact_doc = frappe.get_doc("Contact",customer_doc.get("customer_primary_contact")) 
			if doc.mobile_no:
				contact_doc.mobile_no = doc.mobile_no
				contact_doc.phone_nos = []
				contact_doc.append("phone_nos",{"phone" : doc.mobile_no , "is_primary_mobile_no" : 1})
			if doc.full_name and doc.first_name:
				# TODO sementara cepet-cepet
				contact_doc.first_name = doc.first_name
				customer_doc.customer_name = doc.full_name
				
				
			customer_doc.mobile_no = doc.mobile_no
			contact_doc.save(ignore_permissions=True)
			customer_doc.save(ignore_permissions=True)