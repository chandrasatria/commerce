# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MyVoucher(Document):
	pass


def apply_my_voucher(my_voucher_name = "" , my_voucher_unique_code = ""):
	today = frappe.utils.now()
	fga = frappe.get_all("My Voucher", or_filters=[["name","=",my_voucher_name],["voucher_code","=",my_voucher_unique_code]], fields="name")
	if len(fga)>0:
		doc = frappe.get_doc("My Voucher",fga[0]["name"])
		doc.status = "Applied"
		doc.applied_on = today
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		return {"status" : 1}
	else:
		return {"status" : 0}


def expire_voucher():
	now = frappe.utils.now()[:10]
	frappe.db.sql("UPDATE `tabMy Voucher` SET status = 'Expired' WHERE status = 'Claimed' AND start_date < '{}' ".format(now))
	# d = frappe.db.sql("SELECT * FROM `tabMy Voucher` WHERE status = 'Claimed' AND start_date < '{}' ".format(now))
	# print(str(d))
	frappe.db.commit()

def check_valid_my_voucher(voucher_code, customer, voucher="%"):
	""" status 1 artinya my voucher masih bisa digunakan """
	fga = frappe.get_all("My Voucher",filters=[["voucher_code","=",voucher_code]], or_filters = [["voucher","LIKE",voucher]],fields="name,voucher,status")
	if len(fga) > 0:
		if fga[0]["status"] == "Applied" or fga[0]["status"] == "Expire":
			return {"status" : 0, "keterangan": "Voucher can't be used anymore."}
		doc = frappe.get_doc("Voucher", fga[0]["voucher"])
		return {"doc":doc, "status": 1, "keterangan" : fga[0]["name"]}
	else:
		return {"status" : 0, "keterangan": "Voucher not found"}
