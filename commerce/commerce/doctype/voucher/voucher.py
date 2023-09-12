# -*- coding: utf-8 -*-
# Copyright (c) 2019, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
import re
import sys

from commerce.commerce.doctype.voucher.voucher_helper import randomString,randomStringInt,generate_code,generate_code_bc,upload_base64,strToDate,strToTimedelta
from api_integration.validation import success_format,error_format

import collections


class Voucher(Document):
	pass

# SECTION HOOKS
def before_insert(self,method):
	if not self.batch_code:
		frappe.throw(_("Please enter some Batch Code first."))


def validate(self, method):
	if self.voucher_claim_type == "Promo Voucher" and not self.voucher_code:
		frappe.throw(_("Please enter some Voucher Code first."))
	# STUB Validate
	if self.start_date>self.end_date:
		frappe.throw("<b>End Date</b> must be greater than <b>Start Date</b>")
	if self.publish_start_date>self.publish_end_date:
		frappe.throw("<b>End Date</b> must be greater than <b>Start Date</b>")


@frappe.whitelist()
def before_save(self,method):
	if not self.voucher_id:
		while True:
			v_id = randomString(10)
			fga = frappe.get_all("Voucher",fields="*",filters=[["voucher_id","=",v_id]])
			if len(fga) == 0:
				self.voucher_id = v_id
				break

	while True:
		v_id = randomString(10)
		fga = frappe.get_all("Voucher",fields="*",filters=[["voucher_next_id","=",v_id]])
		if len(fga) == 0:
			self.voucher_next_id = v_id
			break
	
	array_bc = parse_text_to_array(self.batch_code,self.used_code)
	if array_bc["status"] == 0:
		if array_bc["duplicates"]:
			frappe.throw("Sorry there are multiple code in batch code <br>"+str(array_bc["duplicates"]))
		else:
			frappe.throw("Something wrong :(")
	count = 0
	self.batch_code = ""
	if len(array_bc["code_batch_split"])>0:
		self.next_code = array_bc["code_batch_split"][0]
		self.voucher_next_id = v_id
		for cbs in array_bc["code_batch_split"]:
			if cbs != "":
				count+=1
				self.batch_code += cbs
				self.batch_code += ","
		if not self.used_code:
			self.voucher_claimed = 0
	self.voucher_left = count
	self.maximum_voucher_quota = count+self.voucher_claimed


def after_insert(self,method):
	# STUB After Insert
	qrname = "qr"+self.voucher_id+".jpg"
	brname = "br"+self.voucher_id+".jpg"

	# barqrcode = isi dari qrcode/barcodenya nya
	barqrcode = self.name

	# qrcodebase64 itu qrcode yang sudah jadi base64
	qrcodebase64 = generate_code(barqrcode)
	sfqr = upload_base64(qrname, qrcodebase64,"Voucher", self.name, "qr_code")

	# barcode garis
	barcodebase64 = generate_code_bc(barqrcode)
	sfbc = upload_base64(brname, barcodebase64,"Voucher", self.name, "barcode")
	self.reload()

# !SECTION 
# SECTION JS

@frappe.whitelist()
def add_random_voucher(amount, prefix, batch_code):
	prefix_length = len(prefix)
	fga = frappe.get_all("Voucher",fields="name",filters=[["prefix","=",prefix]])
	if len(fga)==0:
		if batch_code:
			parse = parse_text_to_array(batch_code)
			if parse["status"] == 1:
				code_arr = parse["code_batch_split"]
			else:
				return {"status" : 3, "data":"There are some batch code that duplicates"}
		else:
			code_arr = []
		index = 0
		for item in code_arr:
			if prefix not in item[:prefix_length] and item!="":
				code_arr[index]= str(prefix)+str(item)
			index+=1
		for x in range(0, int(amount)):
			code_arr.append(prefix+str(randomStringInt(length = 10)))
		return {"status" : 1, "data":code_arr}
	else:
		return {"status" : 2, "data":"Prefix is duplicate"}


# !SECTION 
def parse_text_to_array(string,used_string=""):
	# print(string)
	# print("-------")
	# print(used_string)
	duplicates = []
	code_batch_split = string.replace("\n",",")
	code_batch_split = re.sub(r',+',",", code_batch_split)
	if (code_batch_split[:1]==","):
		code_batch_split = code_batch_split[1:]
	code_batch_split = code_batch_split.split(",")
	if used_string:
		used_batch_split = used_string.split(",")
		duplicates +=  [x for x in code_batch_split if x in used_batch_split and x != ""]
	duplicates +=  [item for item, count in collections.Counter(code_batch_split).items() if count > 2 and item != ""]
	# remove_duplicate

	while "" in code_batch_split:
  		code_batch_split.remove("")
	if len(duplicates)>0:
		return {"status": 0, "keterangan" : "Duplicates found" , "code_batch_split" : code_batch_split , "duplicates" : duplicates}
	else:
		return {"status": 1, "code_batch_split" : code_batch_split}

def check_rule_customer(voucher,customer):
	now = frappe.utils.now()
	fga_voucher = frappe.get_all("Voucher",fields="quota_interval, quota_customer_per_interval , maximum_redemption_per_day", filters={"name":voucher})
	if len(fga_voucher)==0:
		return {"status": 0, "keterangan" : "Sorry, Voucher is not found"}
	fga_customer = frappe.get_all("Customer", fields = "*", filters={"name":customer})
	if len(fga_customer) == 0:
		return {"status": 0, "keterangan" : "Sorry, Customer is not found"}
	return {"status": 1, "keterangan" : "ok"}

# def claim_voucher(voucher, customer, using_system = 0):

# 	# Check Rule
# 	# TODO Rule
# 	rule_response = check_rule(voucher)

# 	# Change Voucher
# 	if rule_response["status"] == 0:
# 		return rule_response
# 	doc_voucher = frappe.get_doc("Voucher",voucher)
# 	v_id = doc_voucher.voucher_id
# 	next_code = doc_voucher.next_code
# 	next_code_split = doc_voucher.next_code+","
# 	doc_voucher.batch_code = doc_voucher.batch_code.replace(next_code_split,",")
# 	if not doc_voucher.used_code:
# 		doc_voucher.used_code = ""
# 	doc_voucher.used_code+= next_code_split
# 	if not doc_voucher.voucher_claimed:
# 		doc_voucher.voucher_claimed = 0
# 	doc_voucher.voucher_claimed+=1
# 	doc_voucher.next_code = ""
# 	if using_system == 1:
# 		doc_voucher.using_system = 1
# 	doc_voucher.save(ignore_permissions=True)

# {"items":[{"item_code":"STO-ITEM-2019-00047","stock_qty":2}],"customer":"CUST-2019-00025","plc_conversion_rate":1,"company":"TOURANGGA","transaction_date":"2020-01-21","update_stock":0,"coupon_code":"PAYDAY"}}
# untuk mengambil discount dari sales invoice ke pricing rule
def check_pricing_rule(sales_invoice,pricing_rule):
	doc_si = frappe.get_doc("Sales Invoice", sales_invoice)
	doc_pr = frappe.get_doc("Pricing Rule", pricing_rule)

	total_amount = 0.0
	for item in doc_si.items:
		total_amount += float(item.price_list_rate * item.qty)

	if total_amount<doc_pr.min_amt :
		return {"status" : 0, "reason" : "Total Amount is smaller than Minimum Amount"}
	if total_amount>doc_pr.max_amt:
		return {"status" : 0, "reason" : "Total Amount is larger than Maximum Amount"}
	item_status= []
	item_discount = []
	total_discount = 0.0
	for item in doc_si.items:
		if doc_pr.apply_on == "Item Code":
			pass
		if doc_pr.apply_on == "Item Group":
			if not any(d.item_group == item.item_group for d in doc_pr.item_groups):
				item_status.append({"name":item.name,"reason":"Not in item group"})
			# for d in doc_pr.item_groups:
			# 	print(str(d))
		if doc_pr.min_qty > item.qty:
			item_status.append({"name":item.name,"reason":"Need more qty"})
		if doc_pr.max_qty < item.qty and doc_pr.max_qty != 0 :
			item_status.append({"name":item.name,"reason":"Too much qty"})
		if strToDate(doc_pr.valid_upto) < strToDate(item.creation) and strToDate(item.creation) < strToDate(doc_pr.valid_from):
			item_status.append({"name":item.name,"reason":"Not Valid Date"})
		if not any(d["name"] == item.name for d in item_status):
			if doc_pr.rate_or_discount == "Discount Percentage":
				discount_price = float(item.price_list_rate * item.qty)*(doc_pr.discount_percentage/100.00)
				price_after_discount = item.price_list_rate - discount_price
				total_discount+= discount_price
			elif doc_pr.rate_or_discount == "Discount Amount":
				discount_price = doc_pr.discount_amount
				price_after_discount = item.price_list_rate - discount_price
				total_discount+= discount_price
			item_discount.append({"name":item.name,"price": item.price_list_rate,"qty":item.qty ,"discount_price":discount_price, "price_after_discount":price_after_discount})
	
	return {"status" : 1, "item_status" : item_status, "item_discount" : item_discount , "total_discount":total_discount ,"total_amount" :total_amount}
	# print(item_status)
	# print(item_discount)
	# print(total_discount)
	
	
	
# /: untuk mengurangkan stock voucher dan memasukkannya ke Doctype My Voucher
# Dipakai di API my_voucher sebagai (shortcut)
@frappe.whitelist()
def claim_voucher(voucher, customer,using_system=0):
	next_code,voucher_next_id,doc_voucher = function_claim_code(voucher,customer)
	if next_code == 0 and voucher_next_id:
		return {"status" : 0, "keterangan" : voucher_next_id}
	# Insert My Voucher
	doc_my_voucher = frappe.get_doc({
		"doctype": "My Voucher",
		"voucher": voucher,
		"voucher_code" : next_code,
		"customer": customer,
		"status" : "Claimed",
		"claimed_on" : frappe.utils.now(),
		"voucher_id" :  voucher_next_id,
		"start_date": doc_voucher.start_date,
		"end_date" : doc_voucher.end_date,
		"using_system" : using_system
	})
	doc_my_voucher.insert(ignore_permissions=True)
	frappe.db.commit()

	return {"status" :1 , "keterangan" : next_code , "my_voucher_id": doc_my_voucher.name}

def function_claim_code(voucher, customer):
# Check Rule
	# TODO Rule
	fga_voucher = frappe.get_all("Voucher",fields="start_date, end_date, start_time, end_time", filters={"name":voucher})
	if len(fga_voucher)==0:
		return 0,(_("Sorry, Voucher is not found")),None
	rule_response = check_rule_time(voucher)
	# check time Voucher
	if rule_response["status"] == 0:
		return rule_response["status"],(_("Cannot claim now.")),None

	rule_response = check_quantity(voucher,customer)
	if rule_response["status"] == 0:
		return rule_response["status"],(_(rule_response["keterangan"])),None
	
	doc_voucher = frappe.get_doc("Voucher",voucher)
	if doc_voucher.voucher_left == 0:
		frappe.throw("Voucher telah habis")
	# for my voucher
	next_code = doc_voucher.next_code
	voucher_next_id = doc_voucher.voucher_next_id
	# change existing
	doc_voucher.next_code = ""
	doc_voucher.voucher_next_id = ""
	voucher_batch_code = doc_voucher.batch_code.split(",")
	doc_voucher.batch_code = ""
	for item_code in voucher_batch_code:
		if item_code != next_code:
			doc_voucher.batch_code += item_code+","
	if not doc_voucher.used_code:
		doc_voucher.used_code = ""
	doc_voucher.used_code += str(voucher_batch_code[0])+","
	doc_voucher.voucher_left = doc_voucher.voucher_left-1
	doc_voucher.voucher_claimed = doc_voucher.voucher_claimed+1
	print(doc_voucher.batch_code)
	print(doc_voucher.next_code)
	doc_voucher.save(ignore_permissions=True)
	frappe.db.commit()

	return next_code,voucher_next_id,doc_voucher

# @frappe.whitelist()
# def claim_voucher(voucher, customer):
# 	# Check Rule
# 	# TODO Rule
# 	rule_response = check_rule_time(voucher)
# 	# Change Voucher
# 	if rule_response["status"] == 0:
# 		return rule_response
# 	doc_voucher = frappe.get_doc("Voucher",voucher)
# 	next_code = doc_voucher.next_code
# 	next_code_split = ","+doc_voucher.next_code+","
# 	doc_voucher.batch_code = doc_voucher.batch_code.replace(next_code_split,",")
# 	if not doc_voucher.used_code:
# 		doc_voucher.used_code = ""
# 	doc_voucher.used_code+= next_code_split
# 	if not doc_voucher.voucher_claimed:
# 		doc_voucher.voucher_claimed = 0
# 	doc_voucher.voucher_claimed+=1
# 	doc_voucher.next_code = ""
# 	doc_voucher.save(ignore_permissions=True)

# 	# Insert My Voucher
# 	doc_my_voucher = frappe.get_doc({
# 		"doctype": "My Voucher",
# 		"voucher": voucher,
# 		"voucher_code" : next_code,
# 		"customer": customer,
# 		"status" : "Acquired",
# 		"claimed_on" : frappe.utils.now(),
# 		"voucher_id" :  doc_voucher.voucher_next_id
# 	})
# 	doc_my_voucher.insert(ignore_permissions=True)
# 	frappe.db.commit()

# 	return {"status" :1 , "keterangan" : "ok"}

# !SECTION 


@frappe.whitelist()
def try_voucher(voucher_code,customer="", tipe = "Internal"):
	"""untuk cek rule"""
	using_specific_my_voucher = 0
	if customer:
		doc_customer = frappe.get_all("Customer", fields="*", filters={"name":customer})
		if len(doc_customer) == 0:
			doc_customer = frappe.get_all("Customer", fields="*",filters=[["email","=",customer]])
			if len(doc_customer) == 0:
				return {"status" : 0,"keterangan" : "Sorry, Customer {} is not found".format(customer), "data" : ""}

	doc_voucher = frappe.get_all("Voucher",fields="*", filters=[["voucher_code","=",voucher_code],["voucher_claim_type","!=","My Voucher"]])
	if len(doc_voucher) == 0:
		if customer:
			voucher_ = frappe.get_all("My Voucher", filters = [["customer","=",doc_customer[0]["name"]],["voucher_code","=", voucher_code],["status","=","Claimed"]],  fields = "voucher")
			using_specific_my_voucher = 1
		else:
			voucher_ = frappe.get_all("My Voucher", filters = [["voucher_code","=", voucher_code],["status","=","Claimed"]],  fields = "voucher")
			using_specific_my_voucher = 1
		if len(voucher_) == 0:
			return {"status" : 0,"keterangan" : "Sorry, Voucher Code not Found or can't be used."}
		doc_voucher = frappe.get_all("Voucher",fields= "*", filters=[["name","=",voucher_[0]["voucher"]]])
		if len(doc_voucher) == 0:
			return {"status" : 0,"keterangan" : "Sorry, Voucher Code not Found"}
	# elif doc_voucher[0]["voucher_type"] != tipe:
	# 	return {"status" : 0,"keterangan" : "voucher tidak sesuai"}

	rule_response = check_rule_time(doc_voucher[0]["name"])
	if rule_response["status"] == 0:
		return {"status" : 0,"keterangan" : "Sorry, Voucher cannot be used now", "data" : ""}
	
	rule_response = check_quantity(doc_voucher[0]["name"], doc_customer[0]["name"])
	if rule_response["status"] == 0:
		return {"status" : 0,"keterangan" : "Sorry, Voucher is exceed rule quantity", "data" : ""}
	# TODO check rule Customer
	
	return {"status": 1 , "data" : doc_voucher }



# Dipakai du sales_invoice.py (sementara)
# NOTE ini bakal diganti karena tidak sesuai dengan validasi pricing_rule
@frappe.whitelist()
def try_pricing_rule(pricing_rule):
	doc_pricing_rule = frappe.get_doc("Pricing Rule", pricing_rule)
	if not doc_pricing_rule:
		return {"status" : 0 , "reason": "Pricing rule not found"}
	if doc_pricing_rule.disable == 1:
		return {"status" : 0 , "reason": "Discount is disabled"}
	if doc_pricing_rule.rate_or_discount == "Discount Percentage":
		return {"status" : 1 , "reason": "", "discount_on" : "Grand Total", "additional_discount_percentage": doc_pricing_rule.discount_percentage ,"discount_amount" : ""}
	elif doc_pricing_rule.rate_or_discount == "Discount Amount":
		return {"status" : 1 , "reason": "", "discount_on" : "Grand Total", "additional_discount_percentage": "" ,"discount_amount" : doc_pricing_rule.discount_amount}
	else:
		return {"status" : 0 , "reason": "Under development"}

# Ini memakai erpnext
def voucher_pricing_rule_validate_function(args,voucher_code, customer = frappe.session.user):
	from erpnext.accounts.doctype.pricing_rule.pricing_rule import apply_pricing_rule
	# post = json.loads(frappe.request.data.decode('utf-8'))
	null = None
	# args = {"items":[{"doctype":"Sales Invoice Item","name":"New Sales Invoice Item 2","child_docname":"New Sales Invoice Item 2","item_code":"STO-ITEM-2020-00004","item_group":"Trip Plan","brand":null,"qty":1,"stock_qty":1,"uom":"Nos","stock_uom":"Nos","parenttype":"Sales Invoice","parent":"New Sales Invoice 1","warehouse":"Stores - T","price_list_rate":30000,"conversion_factor":1,"margin_type":"","margin_rate_or_amount":0}],"customer_group":"All Customer Groups","territory":"All Territories","currency":"IDR","conversion_rate":1,"price_list":"Standard Selling","price_list_currency":"IDR","plc_conversion_rate":1,"company":"TOURANGGA","transaction_date":"2020-01-21","ignore_pricing_rule":0,"doctype":"Sales Invoice","name":"New Sales Invoice 1","is_return":0,"update_stock":0}
	# voucher_code = "Flight 15"
	try_voucher_response = try_voucher(voucher_code, customer = customer)
	# frappe.throw(str(try_voucher_response))
	if try_voucher_response["status"] == 0:
		return {"status" : 0, "data":try_voucher_response["keterangan"]}
		# return error_format(try_voucher_response["keterangan"])
	# args = {"items":[{"doctype":"Sales Invoice Item","name":"4a48644c9a","child_docname":"4a48644c9a","item_code":"STO-ITEM-2020-00013","item_group":"Vehicle","qty":1,"stock_qty":1,"uom":"Pcs","stock_uom":"Pcs","parenttype":"Sales Invoice","parent":"ACC-SINV-2020-00021","warehouse":"Stores - T","price_list_rate":250000,"conversion_factor":1,"margin_type":"","margin_rate_or_amount":0}],"customer":"CUST-2020-00014","customer_group":"All Customer Groups","territory":"All Territories","currency":"IDR","conversion_rate":1,"price_list":"Standard Selling","price_list_currency":"IDR","plc_conversion_rate":1,"company":"TOURANGGA","transaction_date":"2020-02-25","ignore_pricing_rule":0,"doctype":"Sales Invoice","name":"ACC-SINV-2020-00021","is_return":0,"update_stock":0}

	response = apply_pricing_rule(args = args)
	if response:
		print(response)
	doc_voucher = frappe.get_all("Voucher",fields="*", filters=[["voucher_code","=",voucher_code]])
	if len(doc_voucher)==0:
		doc_my_voucher = frappe.get_all("My Voucher",fields="voucher", filters=[["voucher_code","=",voucher_code]])
		doc_voucher = frappe.get_all("Voucher",fields="*", filters=[["name","=",doc_my_voucher[0]["voucher"]]])
		if len(doc_voucher)==0:
			return {"status" : 0, "data":"Voucher not found"}
		# return error_format("Voucher not found")
	if "pricing_rules" in response[0]:
		if response[0]["pricing_rules"]:
			
			if doc_voucher[0]["pricing_rule"] not in response[0]["pricing_rules"]:
				
				return {"status" : 0, "data":"Voucher not found or mismatch condition"}
				# return frappe.throw(_("Voucher not found or mismatch condition."))
			else:
				doc = frappe.get_doc("Pricing Rule",doc_voucher[0]["pricing_rule"])
				new_response = recreate_apply_pricing_rule(response[0], doc.name)
				new_response["maximal_discount"] = doc.maximal_discount
				return {"status" : 1, "data":new_response}
		else:
			return {"status" : 0, "data":"Pricing Rule not found"}
			# return frappe.throw(_("Pricing Rule not found"))
	else:
		return {"status" : 0, "data":"Voucher not found or mismatch condition."}
		# return frappe.throw(_("Voucher not found or mismatch condition."))

def voucher_pricing_rule_validate_function_without_check(args,voucher_code, customer = frappe.session.user):
	from erpnext.accounts.doctype.pricing_rule.pricing_rule import apply_pricing_rule
	null = None
	try_voucher_response = try_voucher(voucher_code, customer = customer)
	response = apply_pricing_rule(args = args)
	if response:
		print(response)
	doc_voucher = frappe.get_all("Voucher",fields="*", filters=[["voucher_code","=",voucher_code]])
	if len(doc_voucher)==0:
		doc_my_voucher = frappe.get_all("My Voucher",fields="voucher", filters=[["voucher_code","=",voucher_code]])
		doc_voucher = frappe.get_all("Voucher",fields="*", filters=[["name","=",doc_my_voucher[0]["voucher"]]])
		if len(doc_voucher)==0:
			return {"status" : 0, "data":"Voucher not found"}
	if "pricing_rules" in response[0]:
		if response[0]["pricing_rules"]:
			if doc_voucher[0]["pricing_rule"] not in response[0]["pricing_rules"]:
				
				return {"status" : 0, "data":"Voucher not found or mismatch condition"}
				# return frappe.throw(_("Voucher not found or mismatch condition."))
			else:
				doc = frappe.get_doc("Pricing Rule",doc_voucher[0]["pricing_rule"])
				new_response = recreate_apply_pricing_rule(response[0], doc.name)
				new_response["maximal_discount"] = doc.maximal_discount
				# response[0]["maximal_discount"] = doc.maximal_discount
				return {"status" : 1, "data":new_response}
		else:
			return {"status" : 0, "data":"Pricing Rule not found"}
			# return frappe.throw(_("Pricing Rule not found"))
	else:
		return {"status" : 0, "data":"Voucher not found or mismatch condition."}
		# return frappe.throw(_("Voucher not found or mismatch condition."))


def recreate_apply_pricing_rule(pricing_rule_response, pricing_rule_name):

	pr_doc = frappe.get_doc("Pricing Rule", pricing_rule_name)
	recreate_response = {
	"parenttype": "",
	"discount_percentage": pr_doc.discount_percentage,
	"validate_applied_rule": pr_doc.validate_applied_rule,
	"margin_rate_or_amount": pr_doc.margin_rate_or_amount,
	"child_docname": "",
	"price_or_product_discount": pr_doc.price_or_product_discount,
	"parent": "",
	"margin_type": pr_doc.margin_type,
	"discount_amount_on_rate": [],
	"discount_percentage_on_rate": [],
	"pricing_rule_for": pr_doc.rate_or_discount,
	"pricing_rules": pr_doc.name,
	"serial_no": "",
	"has_pricing_rule": 1
	}
	return recreate_response

@frappe.whitelist()
def voucher_pricing_rule_validate(args, voucher_code):
	try:
		response_voucher = voucher_pricing_rule_validate_function(args, voucher_code)
		if response_voucher["status"] == 0:
			return error_format(response_voucher["data"])
		else:
			return success_format(response_voucher["data"])

	except:
		return error_format(sys.exc_info()[1])
	
	# except:
	# 	return error_format(sys.exc_info()[1])

# SECTION Rule
def check_quantity(voucher,customer):
	now = frappe.utils.today()
	fga_voucher = frappe.get_all("Voucher",fields="*", filters={"name":voucher})
	if len(fga_voucher)<1:
		return {"status": 0, "keterangan" : "Sorry, Voucher is not found"}
	fga_customer = frappe.get_all("Customer", fields="*",filters={"name":customer})
	if len(fga_customer)<1:
		return {"status": 0, "keterangan" : "Sorry, Customer not found"}

	can_claim=1

	if(fga_voucher[0]["quota_type"]=="Once"):
		count = frappe.db.sql("SELECT COUNT('name') as c FROM `tabMy Voucher` WHERE voucher = '{}' AND status='Applied' AND customer = '{}'".format(fga_voucher[0]["name"],fga_customer[0]["name"]),as_dict=True)
		if(count[0]["c"]>0):
			can_claim = 0
	elif(fga_voucher[0]["quota_type"]=="Daily"):
		count = frappe.db.sql("SELECT COUNT('name') as c FROM `tabMy Voucher` WHERE voucher = '{}' AND status='Applied' AND customer = '{}' AND YEAR(creation) = YEAR('{today}') AND MONTH(creation) = MONTH('{today}') AND DAY(creation) = DAY('{today}')".format(fga_voucher[0]["name"],fga_customer[0]["name"],today=now),as_dict=True)
		if fga_voucher[0]["quota_amount"] != 0:
			if count[0]["c"] >= int(fga_voucher[0]["quota_amount"]):
				can_claim = 0
	elif(fga_voucher[0]["quota_type"]=="Monthly"):
		count = frappe.db.sql("SELECT COUNT('name') as c FROM `tabMy Voucher` WHERE voucher = '{}' AND status = 'Applied' AND customer = '{}' AND YEAR(creation) = YEAR('{today}') AND MONTH(creation) = MONTH('{today}') ".format(fga_voucher[0]["name"],fga_customer[0]["name"],today=now),as_dict=True)
		if fga_voucher[0]["quota_amount"] != 0:
			if count[0]["c"] >= int(fga_voucher[0]["quota_amount"]):
				can_claim = 0
	if can_claim==0:
		return {"status": 0, "keterangan" : "Sorry, cannot claim voucher. Quota maximum."}
	return {"status": 1, "data" : "ok"}

def check_rule_time(voucher):
	now = frappe.utils.now()
	fga_voucher = frappe.get_all("Voucher",fields="start_date, end_date, start_time, end_time", filters={"name":voucher})
	if len(fga_voucher)==0:
		return {"status": 0, "keterangan" : "Sorry, Voucher is not found"}
	if fga_voucher[0]["start_date"]:
		if strToDate(fga_voucher[0]["start_date"]) > strToDate(now[:10]):
			return {"status": 0, "keterangan" : "Sorry, Voucher is not yet started"}
	if fga_voucher[0]["end_date"]:
		if strToDate(fga_voucher[0]["end_date"]) < strToDate(now[:10]):
			return {"status": 0, "keterangan" : "Sorry, Voucher is expired"}
	if fga_voucher[0]["start_time"] != "00:00:00":
		if strToTimedelta(fga_voucher[0]["start_time"]) > strToTimedelta(now[11:]):
			return {"status": 0, "keterangan" : "Sorry, Voucher is not claimable at this time"}
	if fga_voucher[0]["end_time"] != "23:59:59":
		if strToTimedelta(fga_voucher[0]["end_time"]) < strToTimedelta(now[11:]):
			return {"status": 0, "keterangan" : "Sorry, Voucher is not claimable at this time"}
	return {"status": 1, "keterangan" : "ok"}
